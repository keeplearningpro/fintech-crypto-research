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
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# ---- SQL QUERIES ----
today = datetime.datetime.today()
start_date = today - pd.DateOffset(years=past_years)

btc_query = f"""
SELECT TIMESTAMP_TRUNC(block_timestamp, MONTH) AS month,
       COUNT(*) AS transaction_count,
       SUM(fee) AS total_fee_btc
FROM `bigquery-public-data.crypto_bitcoin.transactions`
WHERE block_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 YEAR)
GROUP BY month
ORDER BY month
"""

eth_query = f"""
SELECT TIMESTAMP_TRUNC(block_timestamp, MONTH) AS month,
       COUNT(*) AS transaction_count,
       SUM(CAST(gas_price AS NUMERIC) * receipt_gas_used) / POW(10, 18) AS total_fee_eth
FROM `bigquery-public-data.crypto_ethereum.transactions`
WHERE block_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 YEAR)
GROUP BY month
ORDER BY month
"""

@st.cache_data(ttl=86400)
def load_data():
    btc_df = client.query(btc_query).to_dataframe()
    eth_df = client.query(eth_query).to_dataframe()

    eth_df["total_fee_eth"] = eth_df["total_fee_eth"].astype(float)
    btc_df["total_fee_btc"] = btc_df["total_fee_btc"].astype(float)
    return btc_df, eth_df

btc_df, eth_df = load_data()

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
st.subheader("📈 Historical Data: Bitcoin")
st.line_chart(btc_past[['transaction_count', 'total_fee_btc']])

st.subheader("📊 Forecast: Bitcoin (Next {} Years)".format(future_years))
st.line_chart(btc_future)

st.subheader("📈 Historical Data: Ethereum")
st.line_chart(eth_past[['transaction_count', 'total_fee_eth']])

st.subheader("📊 Forecast: Ethereum (Next {} Years)".format(future_years))
st.line_chart(eth_future)
