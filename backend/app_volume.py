import streamlit as st
import pandas as pd

# Set Streamlit page config (only once at the top)
st.set_page_config(page_title="Crypto Analytics Dashboard", layout="wide")
st.title("📊 Bitcoin & Ethereum Transaction Analysis Dashboard")

# User input: Horizontal scroll bar (slider)
years = st.slider("Select how many years of data to visualize", min_value=1, max_value=10, value=5)

@st.cache_data
def load_data():
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
    
    # Calculate average fees (handle division by zero)
    btc_df['avg_fee_btc'] = btc_df['total_fee_btc'] / btc_df['transaction_count'].replace(0, pd.NA)
    eth_df['avg_fee_eth'] = eth_df['total_fee_eth'] / eth_df['transaction_count'].replace(0, pd.NA)
    
    return btc_df, eth_df, btc_daily_df, eth_daily_df

# Load data
btc_df, eth_df, btc_daily_df, eth_daily_df = load_data()

# Filter based on selected years
cutoff = pd.Timestamp.today() - pd.DateOffset(years=years)
btc_df = btc_df[btc_df['month'] >= cutoff]
eth_df = eth_df[eth_df['month'] >= cutoff]
btc_daily_df = btc_daily_df[btc_daily_df['transaction_date'] >= cutoff]
eth_daily_df = eth_daily_df[eth_daily_df['transaction_date'] >= cutoff]

# 1. Bitcoin transaction volume
st.subheader("Bitcoin Transaction Volume Over Time")
st.line_chart(btc_df.set_index("month")[["transaction_count"]])

# 2. Bitcoin total fees
st.subheader("Bitcoin Total Transaction Fees (BTC)")
st.line_chart(btc_df.set_index("month")[["total_fee_btc"]])

# 3. Bitcoin Average Fee Per Transaction
st.subheader("Bitcoin Average Fee Per Transaction (BTC)")
st.line_chart(btc_df.set_index("month")[["avg_fee_btc"]])

# 4. Ethereum transaction volume
st.subheader("Ethereum Transaction Volume Over Time")
st.line_chart(eth_df.set_index("month")[["transaction_count"]])

# 5. Ethereum Total Gas Fees (ETH)
st.subheader("Ethereum Total Gas Fees (ETH)")
st.line_chart(eth_df.set_index("month")[["total_fee_eth"]])

# 6. Ethereum Average Fee Per Transaction
st.subheader("Ethereum Average Fee Per Transaction (ETH)")
st.line_chart(eth_df.set_index("month")[["avg_fee_eth"]])

# 7. Compare BTC vs ETH Average Fees
st.subheader("BTC vs ETH Average Transaction Fee Comparison")
fee_comparison_df = pd.concat([
    btc_df.set_index("month")["avg_fee_btc"].rename("Bitcoin"),
    eth_df.set_index("month")["avg_fee_eth"].rename("Ethereum")
], axis=1)
st.line_chart(fee_comparison_df)

# 8. Daily Transactions Comparison
st.subheader("Daily Transactions: Bitcoin vs Ethereum")
daily_tx_df = pd.concat([
    btc_daily_df.set_index("transaction_date")["daily_transaction_count"].rename("Bitcoin"),
    eth_daily_df.set_index("transaction_date")["daily_transaction_count"].rename("Ethereum")
], axis=1)
st.line_chart(daily_tx_df)
