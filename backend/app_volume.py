import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crypto Transaction Volume & Fees", layout="wide")
st.title("📊 Cryptocurrency Transaction Visualizer")

st.markdown("""
This dashboard allows you to explore:
- Monthly and daily transaction volume for Bitcoin and Ethereum
- Total and average transaction fees
- Fee comparisons over time
""")

years = st.selectbox("Select how many years of data to visualize", [10, 5, 2])

@st.cache_data
def load_data():
    btc_df = pd.read_csv("https://raw.githubusercontent.com/your-username/your-repo/main/data/bitcoin.csv")
    eth_df = pd.read_csv("https://raw.githubusercontent.com/your-username/your-repo/main/data/ethereum.csv")
    btc_daily_df = pd.read_csv("https://raw.githubusercontent.com/your-username/your-repo/main/data/bitcoin-daily.csv")
    eth_daily_df = pd.read_csv("https://raw.githubusercontent.com/your-username/your-repo/main/data/ethereum-daily.csv")

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

# Plot 1
st.subheader("Bitcoin Monthly Transaction Volume")
fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(btc_df['month'], btc_df['transaction_count'], marker='o')
ax1.set_title("Bitcoin Transaction Volume Over Time")
ax1.set_xlabel("Month")
ax1.set_ylabel("Transactions")
ax1.grid(True)
st.pyplot(fig1)

# Plot 2
st.subheader("Bitcoin Total Transaction Fees")
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(btc_df['month'], btc_df['total_fee_btc'], marker='o', color='purple')
ax2.set_title("Bitcoin Total Fees (BTC)")
ax2.set_xlabel("Month")
ax2.set_ylabel("Total Fees")
ax2.grid(True)
st.pyplot(fig2)

# Plot 3
st.subheader("Bitcoin Average Fee Per Transaction")
fig3, ax3 = plt.subplots(figsize=(12, 6))
ax3.plot(btc_df['month'], btc_df['avg_fee_btc'], marker='o', color='darkblue')
ax3.set_title("Bitcoin Average Fee Per Transaction")
ax3.set_xlabel("Month")
ax3.set_ylabel("Average Fee (BTC)")
ax3.grid(True)
st.pyplot(fig3)

# Plot 4
st.subheader("Ethereum Monthly Transaction Volume")
fig4, ax4 = plt.subplots(figsize=(12, 6))
ax4.plot(eth_df['month'], eth_df['transaction_count'], marker='o', color='green')
ax4.set_title("Ethereum Transaction Volume Over Time")
ax4.set_xlabel("Month")
ax4.set_ylabel("Transactions")
ax4.grid(True)
st.pyplot(fig4)

# Plot 5
st.subheader("Ethereum Total Gas Fees")
fig5, ax5 = plt.subplots(figsize=(12, 6))
ax5.plot(eth_df['month'], eth_df['total_fee_eth'], marker='o', color='red')
ax5.set_title("Ethereum Total Fees (ETH)")
ax5.set_xlabel("Month")
ax5.set_ylabel("Total Fees")
ax5.grid(True)
st.pyplot(fig5)

# Plot 6
st.subheader("Ethereum Average Fee Per Transaction")
fig6, ax6 = plt.subplots(figsize=(12, 6))
ax6.plot(eth_df['month'], eth_df['avg_fee_eth'], marker='o', color='darkred')
ax6.set_title("Ethereum Average Fee Per Transaction")
ax6.set_xlabel("Month")
ax6.set_ylabel("Average Fee (ETH)")
ax6.grid(True)
st.pyplot(fig6)

# Plot 7
st.subheader("BTC vs ETH Average Fee Comparison")
fig7, ax7 = plt.subplots(figsize=(12, 6))
ax7.plot(btc_df['month'], btc_df['avg_fee_btc'], label='Bitcoin Avg Fee (BTC)', color='blue')
ax7.plot(eth_df['month'], eth_df['avg_fee_eth'], label='Ethereum Avg Fee (ETH)', color='orange')
ax7.set_title("BTC vs ETH Average Fee Comparison")
ax7.set_xlabel("Month")
ax7.set_ylabel("Avg Fee")
ax7.legend()
ax7.grid(True)
st.pyplot(fig7)

# Plot 8
st.subheader("Daily Transactions: Bitcoin vs Ethereum")
fig8, ax8 = plt.subplots(figsize=(14, 7))
ax8.plot(btc_daily_df['transaction_date'], btc_daily_df['daily_transaction_count'], label='Bitcoin', color='blue', alpha=0.7)
ax8.plot(eth_daily_df['transaction_date'], eth_daily_df['daily_transaction_count'], label='Ethereum', color='orange', alpha=0.7)
ax8.set_title("Daily Transactions: Bitcoin vs Ethereum")
ax8.set_xlabel("Date")
ax8.set_ylabel("Number of Transactions")
ax8.legend()
ax8.grid(True)
st.pyplot(fig8)
