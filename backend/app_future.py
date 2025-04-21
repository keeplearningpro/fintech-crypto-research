import streamlit as st
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.oauth2 import service_account
import datetime

st.set_page_config(page_title="Crypto Future Predictions", layout="wide")
st.title("🔮 Predicting the Future of Crypto Transactions")

st.markdown("""
This app uses historical data from BigQuery to forecast transaction trends and fees for Bitcoin and Ethereum.
""")

# ---- USER DROPDOWNS ----
past_years = st.selectbox("Select how many years of historical data to use", [2, 5, 10], index=2)
future_years = st.selectbox("Select how many years to forecast into the future", [1, 2, 3, 4, 5], index=2)

if future_years >= past_years:
    st.error("Future prediction years must be less than historical data years.")
    st.stop()

# ---- BIGQUERY AUTH ----
#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gcp_service_account"],
#    scopes=["https://www.googleapis.com/auth/cloud-platform"],
#)
#client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# ---- SQL QUERIES ----
#today = datetime.datetime.today()
#start_date = today - pd.DateOffset(years=past_years)

#btc_query = f"""
#SELECT TIMESTAMP_TRUNC(block_timestamp, MONTH) AS month,
#       COUNT(*) AS transaction_count,
#       SUM(fee) AS total_fee_btc
#FROM `bigquery-public-data.crypto_bitcoin.transactions`
#WHERE DATE(block_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
#GROUP BY month
#ORDER BY month
#"""

#eth_query = f"""
#SELECT TIMESTAMP_TRUNC(block_timestamp, MONTH) AS month,
#       COUNT(*) AS transaction_count,
#       SUM(CAST(gas_price AS NUMERIC) * receipt_gas_used) / POW(10, 18) AS total_fee_eth
#FROM `bigquery-public-data.crypto_ethereum.transactions`
#WHERE DATE(block_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
#GROUP BY month
#ORDER BY month
#""" 



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
today = pd.Timestamp.today()
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

# ---- DISPLAY ----
#st.subheader("📈 Historical Data: Bitcoin")
#st.line_chart(btc_past[['transaction_count', 'total_fee_btc']])

#st.subheader("📊 Forecast: Bitcoin (Next {} Years)".format(future_years))
#st.line_chart(btc_future)

#st.subheader("📈 Historical Data: Ethereum")
#st.line_chart(eth_past[['transaction_count', 'total_fee_eth']])

#st.subheader("📊 Forecast: Ethereum (Next {} Years)".format(future_years))
#st.line_chart(eth_future)


# ---- DISPLAY ----
st.subheader("📈 Bitcoin: Historical Transactions")
st.line_chart(btc_past[['transaction_count']])

st.subheader("💰 Bitcoin: Historical Fees (BTC)")
st.line_chart(btc_past[['total_fee_btc']])

st.subheader(f"📊 Bitcoin Forecast (Next {future_years} Years)")
fig1, ax1 = plt.subplots()
ax1.plot(btc_future.index, btc_future["Predicted Transactions"], color="orange", label="Predicted Transactions")
ax1.plot(btc_future.index, btc_future["Predicted Fees"], color="darkorange", linestyle='--', label="Predicted Fees")
ax1.set_title("Bitcoin Forecast")
ax1.set_ylabel("Volume / Fees")
ax1.legend()
st.pyplot(fig1)

st.subheader("📈 Ethereum: Historical Transactions")
st.line_chart(eth_past[['transaction_count']])

st.subheader("💰 Ethereum: Historical Fees (ETH)")
st.line_chart(eth_past[['total_fee_eth']])

st.subheader(f"📊 Ethereum Forecast (Next {future_years} Years)")
fig2, ax2 = plt.subplots()
ax2.plot(eth_future.index, eth_future["Predicted Transactions"], color="green", label="Predicted Transactions")
ax2.plot(eth_future.index, eth_future["Predicted Fees"], color="darkgreen", linestyle='--', label="Predicted Fees")
ax2.set_title("Ethereum Forecast")
ax2.set_ylabel("Volume / Fees")
ax2.legend()
st.pyplot(fig2)
