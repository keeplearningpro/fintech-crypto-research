import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crypto Volume & Fees", layout="wide")
st.title("📈 Transaction Volume & Fees Over Time")

# User input
years = st.selectbox("Select how many years of data to visualize", [10, 5, 2])

@st.cache_data
def load_data():
    btc = pd.read_csv("https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/bitcoin_monthly_data.csv")
    eth = pd.read_csv("https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/ethereum_monthly_data.csv")
    btc['month'] = pd.to_datetime(btc['month'])
    eth['month'] = pd.to_datetime(eth['month'])
    btc['avg_fee'] = btc['total_fee_btc'] / btc['transaction_count']
    eth['avg_fee'] = eth['total_fee_eth'] / eth['transaction_count']
    return btc, eth

btc_df, eth_df = load_data()
cutoff = pd.Timestamp.today() - pd.DateOffset(years=years)
btc_df = btc_df[btc_df['month'] >= cutoff]
eth_df = eth_df[eth_df['month'] >= cutoff]

# Plot
st.subheader("Transaction Volume")
st.line_chart({
    "Bitcoin": btc_df.set_index("month")["transaction_count"],
    "Ethereum": eth_df.set_index("month")["transaction_count"]
})

st.subheader("Total Fees")
st.line_chart({
    "Bitcoin": btc_df.set_index("month")["total_fee_btc"],
    "Ethereum": eth_df.set_index("month")["total_fee_eth"]
})

st.subheader("Average Fee per Transaction")
st.line_chart({
    "Bitcoin": btc_df.set_index("month")["avg_fee"],
    "Ethereum": eth_df.set_index("month")["avg_fee"]
})
