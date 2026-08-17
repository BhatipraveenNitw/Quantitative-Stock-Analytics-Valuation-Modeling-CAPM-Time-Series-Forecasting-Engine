import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from pages.utils.capm_function import (
    interactive_plot, normalize, daily_return, calculate_beta
)

st.set_page_config(page_title="CAPM Return", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("Capital Asset Pricing Model")

col1, col2 = st.columns([1, 1])
with col1:
    stocks_list = st.multiselect(
        "Choose 4 stocks",
        ('TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'),
        ['TSLA', 'AAPL', 'AMZN', 'GOOGL']
    )
with col2:
    year = st.number_input("Number of years", 1, 10, value=3)

try:
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)

    SP500 = yf.download('^GSPC', start=start, end=end, progress=False)[['Close']]
    if isinstance(SP500.columns, pd.MultiIndex):
        SP500.columns = SP500.columns.get_level_values(0)
    SP500.reset_index(inplace=True)
    SP500.rename(columns={'Close': 'sp500'}, inplace=True)
    SP500['Date'] = pd.to_datetime(SP500['Date']).dt.tz_localize(None)

    stocks_df = pd.DataFrame({'Date': SP500['Date']})
    for stock in stocks_list:
        temp = yf.download(stock, start=start, end=end, progress=False)[['Close']]
        if isinstance(temp.columns, pd.MultiIndex):
            temp.columns = temp.columns.get_level_values(0)
        temp.reset_index(inplace=True)
        temp['Date'] = pd.to_datetime(temp['Date']).dt.tz_localize(None)
        stocks_df = pd.merge(stocks_df, temp.rename(columns={'Close': stock}), on='Date', how='inner')

    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Dataframe Head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### Dataframe Tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Price of all the Stocks")
        st.plotly_chart(interactive_plot(stocks_df.drop(columns=['sp500'])))
    with col2:
        st.markdown("### Price of all the Stocks (After Normalization)")
        st.plotly_chart(interactive_plot(normalize(stocks_df.drop(columns=['sp500']))))

    stocks_daily_return = daily_return(stocks_df)

    beta = {}
    alpha = {}
    for i in stocks_daily_return.columns:
        if i != 'Date' and i != 'sp500':
            b, a = calculate_beta(stocks_daily_return, i)
            beta[i] = b
            alpha[i] = a

    beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
    beta_df['Stock'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

    return_value = []
    rf = 0
    rm = stocks_daily_return['sp500'].mean() * 252

    for i in stocks_list:
        return_value.append(str(round(rf + (beta[i] * (rm - rf)), 2)))

    return_df = pd.DataFrame(columns=['Stock', 'Return Value'])
    return_df['Stock'] = stocks_list
    return_df['Return Value'] = return_value

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Calculated Beta Value")
        st.dataframe(beta_df, use_container_width=True)
    with col2:
        st.markdown("### Calculated Return using CAPM")
        st.dataframe(return_df, use_container_width=True)

except Exception as e:
    st.write("Please select valid input")
