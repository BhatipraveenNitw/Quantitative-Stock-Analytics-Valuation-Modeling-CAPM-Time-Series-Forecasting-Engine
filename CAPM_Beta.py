import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import plotly.express as px
from pages.utils.capm_function import daily_return, calculate_beta

st.set_page_config(page_title="CAPM Beta", page_icon=":bar_chart:", layout="wide")
st.title("Capital Asset Pricing Model - Beta Analysis")

col1, col2 = st.columns(2)
with col1:
    stock = st.selectbox("Select Stock for Beta Regression", ('TSLA', 'AAPL', 'NFLX', 'MSFT', 'AMZN', 'GOOGL'))
with col2:
    year = st.number_input("Lookback Years", 1, 10, value=3)

try:
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)

    sp500 = yf.download('^GSPC', start=start, end=end, progress=False)[['Close']]
    if isinstance(sp500.columns, pd.MultiIndex):
        sp500.columns = sp500.columns.get_level_values(0)
    sp500.reset_index(inplace=True)
    sp500.rename(columns={'Close': 'sp500'}, inplace=True)
    sp500['Date'] = pd.to_datetime(sp500['Date']).dt.tz_localize(None)

    stock_df = yf.download(stock, start=start, end=end, progress=False)[['Close']]
    if isinstance(stock_df.columns, pd.MultiIndex):
        stock_df.columns = stock_df.columns.get_level_values(0)
    stock_df.reset_index(inplace=True)
    stock_df.rename(columns={'Close': stock}, inplace=True)
    stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.tz_localize(None)

    df = pd.merge(stock_df, sp500, on='Date', how='inner')
    ret_df = daily_return(df)

    b, a = calculate_beta(ret_df, stock)

    col1, col2 = st.columns(2)
    col1.metric("Calculated Beta (Slope)", value=f"{b:.3f}")
    col2.metric("Calculated Alpha (Intercept)", value=f"{a:.3f}")

    fig = px.scatter(
        ret_df,
        x='sp500',
        y=stock,
        trendline="ols",
        title=f"Daily Return Regression: {stock} vs S&P 500",
        labels={'sp500': 'S&P 500 Daily Return (%)', stock: f'{stock} Daily Return (%)'}
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error executing Beta calculation: {e}")
