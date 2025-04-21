import streamlit as st
import pandas as pd
import numpy as np
import datetime
import altair as alt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="Crypto Future Predictions", layout="wide")
st.title("🔮 Predicting the Future of Bitcoin and Ethereum Transactions")

st.markdown("""
This app uses historical data from BigQuery public datasets to forecast transaction trends and fees for Bitcoin and Ethereum.
""")

# ---- USER DROPDOWNS ----
#past_years = st.selectbox("Select how many years of historical data to use", [2, 5, 10], index=2)
#future_years = st.selectbox("Select how many years to forecast into the future", [1, 2, 3, 4, 5], index=2)
#model_choice = st.radio("Select prediction model", ["Linear Regression", "Holt-Winters Smoothing"])

past_years = st.slider("Select how many years of historical data to use",min_value=1,max_value=15,value=10)
future_years = st.slider("Select how many years to forecast into the future",min_value=1,max_value=5,value=3)
# Center aligned radio buttons using columns
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    model_choice = st.radio(
        "Select prediction model",
        ["Linear Regression", "Holt-Winters Smoothing"],
        horizontal=True
    )


if future_years >= past_years:
    st.error("Future prediction years must be less than historical data years.")
    st.stop()

# ---- LOAD DATA ----
@st.cache_data(ttl=86400)
def load_data():
    btc_url = "https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/bitcoin-future.csv"
    eth_url = "https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/ethereum-future.csv"
    btc_df = pd.read_csv(btc_url, parse_dates=["month"])
    eth_df = pd.read_csv(eth_url, parse_dates=["month"])
    btc_df["total_fee_btc"] = btc_df["total_fee_btc"].astype(float)
    eth_df["total_fee_eth"] = eth_df["total_fee_eth"].astype(float)
    return btc_df, eth_df

btc_df, eth_df = load_data()
cutoff = pd.Timestamp.now(tz="UTC") - pd.DateOffset(years=past_years)
btc_df = btc_df[btc_df["month"] >= cutoff]
eth_df = eth_df[eth_df["month"] >= cutoff]

# ---- FORECAST FUNCTIONS ----
def forecast_with_linear(df, column, steps):
    df = df.copy()
    df["t"] = np.arange(len(df))
    coeffs = np.polyfit(df["t"], df[column], 1)
    future_t = np.arange(len(df), len(df) + steps)
    return coeffs[0] * future_t + coeffs[1]

def forecast_with_holt_winters(df, column, steps, seasonal_periods=12):
    model = ExponentialSmoothing(df[column], trend='add', seasonal='add', seasonal_periods=seasonal_periods).fit()
    return model.forecast(steps)

def prepare_and_predict(df, fee_col, future_years, model_type):
    df = df.set_index("month").resample("M").sum()
    df = df.reset_index()
    steps = future_years * 12

    if model_type == "Linear Regression":
        future_tx = forecast_with_linear(df, "transaction_count", steps)
        future_fee = forecast_with_linear(df, fee_col, steps)
    else:
        future_tx = forecast_with_holt_winters(df, "transaction_count", steps)
        future_fee = forecast_with_holt_winters(df, fee_col, steps)

    future_months = pd.date_range(df['month'].iloc[-1] + pd.offsets.MonthBegin(1), periods=steps, freq='MS')
    future_df = pd.DataFrame({
        'month': future_months,
        'Predicted Transactions': future_tx,
        'Predicted Fees': future_fee
    }).set_index("month")

    return df.set_index("month"), future_df

btc_past, btc_future = prepare_and_predict(btc_df, "total_fee_btc", future_years, model_choice)
eth_past, eth_future = prepare_and_predict(eth_df, "total_fee_eth", future_years, model_choice)

# ---- CHARTS ----
def plot_bubble_line(df, x_col, y_col, color):
    base = alt.Chart(df.reset_index()).encode(
        x=f'{x_col}:T',
        y=f'{y_col}:Q',
        tooltip=[f'{x_col}:T', f'{y_col}:Q']
    )
    return base.mark_line(color=color) + base.mark_circle(color=color, size=60)

# ---- DISPLAY ----
st.subheader(f"📊 Bitcoin Transactions Forecast For Next {future_years} Years Using {model_choice}")
st.altair_chart(plot_bubble_line(btc_future, 'month', 'Predicted Transactions', 'orange').properties(height=300), use_container_width=True)

st.subheader(f"📊 Bitcoin Fees Forecast For Next {future_years} Years Using {model_choice}")
st.altair_chart(plot_bubble_line(btc_future, 'month', 'Predicted Fees', 'darkorange').properties(height=300), use_container_width=True)

st.subheader(f"📊 Ethereum Transactions Forecast For Next {future_years} Years Using {model_choice}")
st.altair_chart(plot_bubble_line(eth_future, 'month', 'Predicted Transactions', 'green').properties(height=300), use_container_width=True)

st.subheader(f"📊 Ethereum Fees Forecast For Next {future_years} Years Using {model_choice}")
st.altair_chart(plot_bubble_line(eth_future, 'month', 'Predicted Fees', 'darkgreen').properties(height=300), use_container_width=True)
