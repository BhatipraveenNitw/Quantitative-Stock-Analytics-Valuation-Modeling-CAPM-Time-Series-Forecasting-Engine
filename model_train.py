import yfinance as yf
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import root_mean_squared_error
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

def get_data(ticker):
    stock_data = yf.download(ticker, start="2020-01-01", progress=False)
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = stock_data.columns.get_level_values(0)
    return stock_data[['Close']]

def stationarity_check(close_price):
    result = adfuller(close_price.dropna())
    return result[1]

def get_rolling_mean(close_price):
    return close_price.rolling(window=7).mean().dropna()

def get_differencing_order(close_price):
    p_value = stationarity_check(close_price)
    d = 0
    while p_value > 0.05:
        d += 1
        close_price = close_price.diff().dropna()
        p_value = stationarity_check(close_price)
    return d

def fit_model(data, differencing_order):
    model = ARIMA(data, order=(30, differencing_order, 30))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=30)
    return forecast

def evaluate_model(train_data, test_data, differencing_order):
    prediction = fit_model(train_data, differencing_order)
    rmse = root_mean_squared_error(test_data, prediction)
    return round(float(rmse), 2)

def scaling(close_price):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(close_price.values.reshape(-1, 1))
    return scaled_data, scaler

def inverse_scaling(scaler, scaled_data):
    return scaler.inverse_transform(scaled_data.reshape(-1, 1))

def get_forecast(scaled_data, differencing_order, scaler):
    prediction = fit_model(scaled_data, differencing_order)
    start_date = datetime.today()
    end_date = start_date + timedelta(days=29)
    forecast_index = pd.date_range(start=start_date, end=end_date)
    forecast_df = pd.DataFrame(index=forecast_index, columns=['Close'])
    forecast_df['Close'] = inverse_scaling(scaler, prediction)
    return forecast_df
