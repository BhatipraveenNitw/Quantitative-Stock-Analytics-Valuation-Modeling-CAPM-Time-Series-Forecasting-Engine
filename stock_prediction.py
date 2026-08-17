import streamlit as st
import pandas as pd
from pages.utils.model_train import (
    get_data, get_rolling_mean, get_differencing_order,
    scaling, evaluate_model, get_forecast
)
from pages.utils.plotly_figure import plotly_table, moving_average_forecast

st.set_page_config(page_title="Stock Prediction", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("Stock Prediction")

col1, col2 = st.columns(2)
with col1:
    ticker = st.text_input("Stock Ticker", "TSLA")

st.subheader(f"Predicting Next 30 Days Close Price for: {ticker}")

try:
    close_price = get_data(ticker)
    rolling_price = get_rolling_mean(close_price)
    differencing_order = get_differencing_order(rolling_price)

    scaled_data, scaler = scaling(rolling_price)

    train_data = scaled_data[:-30]
    test_data = scaled_data[-30:]
    rmse_score = evaluate_model(train_data, test_data, differencing_order)

    st.write(f"**Model RMSE Score:** `{rmse_score}`")

    forecast = get_forecast(scaled_data, differencing_order, scaler)

    st.subheader("Next 30 Days Projected Close Prices")
    forecast_display = forecast.copy().round(2).reset_index()
    forecast_display.columns = ['Date', 'Projected Close Price']
    forecast_display['Date'] = forecast_display['Date'].dt.strftime('%Y-%m-%d')
    st.plotly_chart(plotly_table(forecast_display), use_container_width=True)

    combined_df = pd.concat([rolling_price.iloc[-150:], forecast])
    st.plotly_chart(moving_average_forecast(combined_df), use_container_width=True)
except Exception as e:
    st.error(f"Error generating predictions: {str(e)}")
