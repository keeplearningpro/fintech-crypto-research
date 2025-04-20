import streamlit as st
import pandas as pd

# Load datasets
bc_file_path = "https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/bitcoin.csv"
etc_file_path = "https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/etherium.csv"
bc_daily_file_path = "https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/bitcoin-daily.csv"
etc_daily_file_path = "https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/etherium-daily.csv"

btc_df = pd.read_csv(bc_file_path)
eth_df = pd.read_csv(etc_file_path)
btc_daily_df = pd.read_csv(bc_daily_file_path)
eth_daily_df = pd.read_csv(etc_daily_file_path)

# Convert date columns
btc_df['month'] = pd.to_datetime(btc_df['month'])
eth_df['month'] = pd.to_datetime(eth_df['month'])
btc_daily_df['transaction_date'] = pd.to_datetime(btc_daily_df['transaction_date'])
eth_daily_df['transaction_date'] = pd.to_datetime(eth_daily_df['transaction_date'])

# Calculate average fees
btc_df['avg_fee_btc'] = btc_df['total_fee_btc'] / btc_df['transaction_count']
eth_df['avg_fee_eth'] = eth_df['total_fee_eth'] / eth_df['transaction_count']

# Title
st.set_page_config(page_title="Crypto Analytics Dashboard", layout="wide")
st.title("📊 Crypto Transaction Analysis Dashboard")

# 1. Bitcoin transaction volume
st.subheader("Bitcoin Transaction Volume Over 10 Years")
st.line_chart(btc_df.set_index("month")[["transaction_count"]])

# 2. Bitcoin total fees
st.subheader("Bitcoin Total Transaction Fees (BTC)")
st.line_chart(btc_df.set_index("month")[["total_fee_btc"]])

# 3. Bitcoin Average Fee Per Transaction
st.subheader("Bitcoin Average Fee Per Transaction (BTC)")
st.line_chart(btc_df.set_index("month")[["avg_fee_btc"]])

# 4. Ethereum transaction volume
st.subheader("Ethereum Transaction Volume Over 10 Years")
st.line_chart(eth_df.set_index("month")[["transaction_count"]])

# 5. Ethereum Total Gas Fees (ETH)
st.subheader("Ethereum Total Gas Fees (ETH)")
st.line_chart(eth_df.set_index("month")[["total_fee_eth"]])

# 6. Ethereum Average Fee Per Transaction
st.subheader("Ethereum Average Fee Per Transaction (ETH)")
st.line_chart(eth_df.set_index("month")[["avg_fee_eth"]])

# 7. Compare BTC vs ETH Average Fees
st.subheader("BTC vs ETH Average Transaction Fee Comparison")
fee_comparison_df = pd.DataFrame({
    "Bitcoin Avg Fee (BTC)": btc_df.set_index("month")["avg_fee_btc"],
    "Ethereum Avg Fee (ETH)": eth_df.set_index("month")["avg_fee_eth"]
})
st.line_chart(fee_comparison_df)

# 8. Daily Transactions Comparison
st.subheader("Daily Transactions: Bitcoin vs Ethereum")
daily_tx_df = pd.DataFrame({
    "Bitcoin": btc_daily_df.set_index("transaction_date")["daily_transaction_count"],
    "Ethereum": eth_daily_df.set_index("transaction_date")["daily_transaction_count"]
})
st.line_chart(daily_tx_df)
