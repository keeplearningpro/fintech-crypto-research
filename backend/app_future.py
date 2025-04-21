import streamlit as st
import pandas as pd
import numpy as np
import datetime
import altair as alt

st.set_page_config(page_title="Crypto Future Predictions", layout="wide")
st.title("🔮 Predicting the Future of Crypto Transactions")

st.markdown("""
This app uses historical data from GitHub to forecast transaction trends and fees for Bitcoin and Ethereum.
""")

# ---- USER DROPDOWNS ----
past_years = st.selectbox("Select how many years of historical data to use", [2, 5, 10], index=2)
future_years = st.selectbox("Select how many years to forecast into the future", [1, 2, 3, 4, 5], index=2)

if future_years >= past_years:
    st.error("Future prediction years must be less than historical data years.")
    st.stop()

# ---- Load Data from GitHub ----
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

# ---- Filter by historical period ----
cutoff = pd.Timestamp.now(tz="UTC") - pd.DateOffset(years=past_years)
btc_df = btc_df[btc_df["month"] >= cutoff]
eth_df = eth_df[eth_df["month"] >= cutoff]

# ---- RESAMPLE AND PREDICT ----
def prepare_and_predict(df, fee_col, future_years):
    df = df.set_index("month").resample("M").sum()
    df = df.reset_index()
    df['t'] = np.arange(len(df))

    def forecast(col):
        coeffs = np.polyfit(df['t'], df[col], 1)
        future_t = np.arange(len(df), len(df) + future_years * 12)
        return coeffs[0] * future_t + coeffs[1]

    future_months = pd.date_range(df['month'].iloc[-1] + pd.offsets.MonthBegin(1),
                                  periods=future_years * 12, freq='MS')
    pred_tx = forecast("transaction_count")
    pred_fee = forecast(fee_col)

    future_df = pd.DataFrame({
        'month': future_months,
        'Predicted Transactions': pred_tx,
        'Predicted Fees': pred_fee
    }).set_index("month")
    return df.set_index("month"), future_df

btc_past, btc_future = prepare_and_predict(btc_df, "total_fee_btc", future_years)
eth_past, eth_future = prepare_and_predict(eth_df, "total_fee_eth", future_years)

# ---- Altair Bubble Line Charts ----

# --- Bitcoin Forecast: Transactions ---
st.subheader(f"📊 Bitcoin Forecast - Transactions (Next {future_years} Years)")
btc_tx_base = alt.Chart(btc_future.reset_index()).encode(
    x='month:T',
    y='Predicted Transactions:Q',
    tooltip=['month:T', 'Predicted Transactions']
)
btc_tx_chart = btc_tx_base.mark_line(color='orange') + btc_tx_base.mark_circle(color='orange', size=60)
st.altair_chart(btc_tx_chart.properties(width='container', height=300), use_container_width=True)

# --- Bitcoin Forecast: Fees ---
st.subheader(f"📊 Bitcoin Forecast - Fees (Next {future_years} Years)")
btc_fee_base = alt.Chart(btc_future.reset_index()).encode(
    x='month:T',
    y='Predicted Fees:Q',
    tooltip=['month:T', 'Predicted Fees']
)
btc_fee_chart = btc_fee_base.mark_line(color='darkorange') + btc_fee_base.mark_circle(color='darkorange', size=60)
st.altair_chart(btc_fee_chart.properties(width='container', height=300), use_container_width=True)

# --- Ethereum Forecast: Transactions ---
st.subheader(f"📊 Ethereum Forecast - Transactions (Next {future_years} Years)")
eth_tx_base = alt.Chart(eth_future.reset_index()).encode(
    x='month:T',
    y='Predicted Transactions:Q',
    tooltip=['month:T', 'Predicted Transactions']
)
eth_tx_chart = eth_tx_base.mark_line(color='green') + eth_tx_base.mark_circle(color='green', size=60)
st.altair_chart(eth_tx_chart.properties(width='container', height=300), use_container_width=True)

# --- Ethereum Forecast: Fees ---
st.subheader(f"📊 Ethereum Forecast - Fees (Next {future_years} Years)")
eth_fee_base = alt.Chart(eth_future.reset_index()).encode(
    x='month:T',
    y='Predicted Fees:Q',
    tooltip=['month:T', 'Predicted Fees']
)
eth_fee_chart = eth_fee_base.mark_line(color='darkgreen') + eth_fee_base.mark_circle(color='darkgreen', size=60)
st.altair_chart(eth_fee_chart.properties(width='container', height=300), use_container_width=True)
