import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crypto Transaction Volume & Fees", layout="wide")
st.title("📊 Transaction Volume & Fees: Bitcoin vs Ethereum")

years = st.selectbox("Select how many years of data to visualize", [10, 5, 2])

@st.cache_data
def load_data():
    btc_url = "https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/bitcoin.csv"
    eth_url = "https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/ethereum.csv"
    btc_daily_url = "https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/bitcoin-daily.csv"
    eth_daily_url = "https://raw.githubusercontent.com/keeplearningpro/fintech-crypto-research/main/data/ethereum-daily.csv"

    btc_df = pd.read_csv(btc_url)
    eth_df = pd.read_csv(eth_url)
    btc_daily_df = pd.read_csv(btc_daily_url)
    eth_daily_df = pd.read_csv(eth_daily_url)

    btc_df['month'] = pd.to_datetime(btc_df['month'])
    eth_df['month'] = pd.to_datetime(eth_df['month'])
    btc_daily_df['transaction_date'] = pd.to_datetime(btc_daily_df['transaction_date'])
    eth_daily_df['transaction_date'] = pd.to_datetime(eth_daily_df['transaction_date'])

    btc_df['avg_fee_btc'] = btc_df['total_fee_btc'] / btc_df['transaction_count']
    eth_df['avg_fee_eth'] = eth_df['total_fee_eth'] / eth_df['transaction_count']

    btc_daily_df.sort_values('transaction_date', inplace=True)
    eth_daily_df.sort_values('transaction_date', inplace=True)

    return btc_df, eth_df, btc_daily_df, eth_daily_df

btc_df, eth_df, btc_daily_df, eth_daily_df = load_data()

cutoff = pd.Timestamp.today() - pd.DateOffset(years=years)
btc_df = btc_df[btc_df['month'] >= cutoff]
eth_df = eth_df[eth_df['month'] >= cutoff]
btc_daily_df = btc_daily_df[btc_daily_df['transaction_date'] >= cutoff]
eth_daily_df = eth_daily_df[eth_daily_df['transaction_date'] >= cutoff]

# 1. Bitcoin transaction volume
st.subheader("Bitcoin Transaction Volume")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(btc_df['month'], btc_df['transaction_count'], marker='o')
ax.set_xlabel("Month")
ax.set_ylabel("Number of Transactions Per Month")
ax.set_title("Bitcoin Transaction Volume Over Time")
ax.grid(True)
st.pyplot(fig)

# 2. Bitcoin total fees
st.subheader("Bitcoin Total Fees")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(btc_df['month'], btc_df['total_fee_btc'], marker='o', color='purple')
ax.set_xlabel("Month")
ax.set_ylabel("Total Fees in BTC")
ax.set_title("Bitcoin Total Transaction Fees")
ax.grid(True)
st.pyplot(fig)

# 3. Bitcoin average fee per transaction
st.subheader("Bitcoin Average Fee per Transaction")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(btc_df['month'], btc_df['avg_fee_btc'], marker='o', color='darkblue')
ax.set_xlabel("Month")
ax.set_ylabel("Avg Fee (BTC)")
ax.set_title("Bitcoin Average Fee Per Transaction")
ax.grid(True)
st.pyplot(fig)

# 4. Ethereum transaction volume
st.subheader("Ethereum Transaction Volume")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(eth_df['month'], eth_df['transaction_count'], marker='o', color='green')
ax.set_xlabel("Month")
ax.set_ylabel("Number of Transactions Per Month")
ax.set_title("Ethereum Transaction Volume Over Time")
ax.grid(True)
st.pyplot(fig)

# 5. Ethereum total fees
st.subheader("Ethereum Total Fees")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(eth_df['month'], eth_df['total_fee_eth'], marker='o', color='red')
ax.set_xlabel("Month")
ax.set_ylabel("Total Gas Fees in ETH")
ax.set_title("Ethereum Total Gas Fees")
ax.grid(True)
st.pyplot(fig)

# 6. Ethereum average fee per transaction
st.subheader("Ethereum Average Fee per Transaction")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(eth_df['month'], eth_df['avg_fee_eth'], marker='o', color='darkred')
ax.set_xlabel("Month")
ax.set_ylabel("Avg Fee (ETH)")
ax.set_title("Ethereum Average Fee Per Transaction")
ax.grid(True)
st.pyplot(fig)

# 7. Compare BTC vs ETH Average Fee
st.subheader("Bitcoin vs Ethereum Average Fee Comparison")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(btc_df['month'], btc_df['avg_fee_btc'], label='Bitcoin Avg Fee (BTC)', color='blue')
ax.plot(eth_df['month'], eth_df['avg_fee_eth'], label='Ethereum Avg Fee (ETH)', color='orange')
ax.set_xlabel("Month")
ax.set_ylabel("Avg Fee")
ax.set_title("BTC vs ETH Average Transaction Fee")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# 8. Daily transactions comparison
st.subheader("Daily Transactions: Bitcoin vs Ethereum")
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(btc_daily_df['transaction_date'], btc_daily_df['daily_transaction_count'], label='Bitcoin', color='blue', alpha=0.7)
ax.plot(eth_daily_df['transaction_date'], eth_daily_df['daily_transaction_count'], label='Ethereum', color='orange', alpha=0.7)
ax.set_xlabel("Date")
ax.set_ylabel("Number of Transactions")
ax.set_title("Daily Transactions: Bitcoin vs Ethereum")
ax.legend()
ax.grid(True)
st.pyplot(fig)
