import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, date
from pages.utils.plotly_figure import (
    plotly_table, close_chart, candel_stick, rsi, moving_average, macd
)

st.set_page_config(page_title="Stock Analysis", page_icon=":chart_with_downwards_trend:", layout="wide")
st.title("Stock Analysis")

col1, col2, col3 = st.columns(3)
today = date.today()

with col1:
    ticker = st.text_input("Stock Ticker", "TSLA")
with col2:
    start_date = st.date_input("Choose Start Date", date(today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", today)

st.subheader(ticker)
stock = yf.Ticker(ticker)
st.write(stock.info.get('longBusinessSummary', ''))
st.markdown(f"**Sector:** {stock.info.get('sector', 'N/A')}")
st.markdown(f"**Full Time Employees:** {stock.info.get('fullTimeEmployees', 'N/A')}")
st.markdown(f"**Website:** {stock.info.get('website', 'N/A')}")

col1, col2 = st.columns(2)
with col1:
    df1 = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
    df1[''] = [
        stock.info.get('marketCap', 'N/A'),
        stock.info.get('beta', 'N/A'),
        stock.info.get('trailingEps', 'N/A'),
        stock.info.get('trailingPE', 'N/A')
    ]
    df1.reset_index(inplace=True)
    df1.rename(columns={'index': 'Metrics'}, inplace=True)
    st.plotly_chart(plotly_table(df1), use_container_width=True)

with col2:
    df2 = pd.DataFrame(index=['Quick Ratio', 'Revenue Per Share', 'Profit Margin', 'Debt To Equity', 'Return On Equity'])
    df2[''] = [
        stock.info.get('quickRatio', 'N/A'),
        stock.info.get('revenuePerShare', 'N/A'),
        stock.info.get('profitMargins', 'N/A'),
        stock.info.get('debtToEquity', 'N/A'),
        stock.info.get('returnOnEquity', 'N/A')
    ]
    df2.reset_index(inplace=True)
    df2.rename(columns={'index': 'Metrics'}, inplace=True)
    st.plotly_chart(plotly_table(df2), use_container_width=True)

data = yf.download(ticker, start=start_date, end=end_date, progress=False)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

if len(data) >= 2:
    col1, col2, col3 = st.columns(3)
    daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    with col1:
        st.metric(
            label=f"Daily Change ({ticker})",
            value=f"{data['Close'].iloc[-1]:.2f}",
            delta=f"{daily_change:.2f}"
        )

    st.subheader("Historical Data (Last 10 Days)")
    last_10_df = data.tail(10).sort_index(ascending=False).round(2)
    last_10_df.reset_index(inplace=True)
    last_10_df['Date'] = last_10_df['Date'].dt.strftime('%Y-%m-%d')
    st.plotly_chart(plotly_table(last_10_df), use_container_width=True)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    num_period = ''
    with col1:
        if st.button('5D'): num_period = '5d'
    with col2:
        if st.button('1M'): num_period = '1mo'
    with col3:
        if st.button('6M'): num_period = '6mo'
    with col4:
        if st.button('YTD'): num_period = 'ytd'
    with col5:
        if st.button('1Y'): num_period = '1y'
    with col6:
        if st.button('5Y'): num_period = '5y'

    col1, col2 = st.columns(2)
    with col1:
        chart_type = st.selectbox("Select Chart Type", ['Candle', 'Line'])
    with col2:
        if chart_type == 'Candle':
            indicators = st.selectbox("Select Indicator", ['RSI', 'MACD'])
        else:
            indicators = st.selectbox("Select Indicator", ['RSI', 'Moving Average', 'MACD'])

    if chart_type == 'Candle':
        st.plotly_chart(candel_stick(data, num_period), use_container_width=True)
        if indicators == 'RSI':
            st.plotly_chart(rsi(data, num_period), use_container_width=True)
        elif indicators == 'MACD':
            st.plotly_chart(macd(data, num_period), use_container_width=True)
    else:
        if indicators == 'Moving Average':
            st.plotly_chart(moving_average(data, num_period), use_container_width=True)
        else:
            st.plotly_chart(close_chart(data, num_period), use_container_width=True)
            if indicators == 'RSI':
                st.plotly_chart(rsi(data, num_period), use_container_width=True)
            elif indicators == 'MACD':
                st.plotly_chart(macd(data, num_period), use_container_width=True)
