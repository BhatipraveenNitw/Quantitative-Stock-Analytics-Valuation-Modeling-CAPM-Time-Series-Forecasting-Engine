import plotly.graph_objects as go
import pandas_ta as pta
from datetime import datetime
from dateutil.relativedelta import relativedelta

def plotly_table(dataframe):
    headerColor = '#1f77b4'
    rowEvenColor = '#f8f9fa'
    rowOddColor = '#e9ecef'

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(dataframe.columns),
            line_color='darkslategray',
            fill_color=headerColor,
            align=['left', 'center'],
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[dataframe[col] for col in dataframe.columns],
            line_color='darkslategray',
            fill_color=[[rowOddColor if i % 2 == 0 else rowEvenColor for i in range(len(dataframe))]],
            align=['left', 'center'],
            font=dict(color='black', size=11),
            height=28
        )
    )])
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=250)
    return fig

def filter_data(df, num_period):
    if num_period == '1mo':
        date = df.index[-1] + relativedelta(months=-1)
    elif num_period == '5d':
        date = df.index[-1] + relativedelta(days=-5)
    elif num_period == '6mo':
        date = df.index[-1] + relativedelta(months=-6)
    elif num_period == '1y':
        date = df.index[-1] + relativedelta(years=-1)
    elif num_period == '5y':
        date = df.index[-1] + relativedelta(years=-5)
    else:
        date = df.index[0]
    return df[df.index >= date]

def close_chart(dataframe, num_period=None):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Open'], mode='lines', name='Open'))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['High'], mode='lines', name='High'))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Low'], mode='lines', name='Low'))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Close'], mode='lines', name='Close'))
    fig.update_layout(title="Line Chart", xaxis_title="Date", yaxis_title="Price", height=450)
    return fig

def candel_stick(dataframe, num_period=None):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure(data=[go.Candlestick(
        x=dataframe.index,
        open=dataframe['Open'],
        high=dataframe['High'],
        low=dataframe['Low'],
        close=dataframe['Close'],
        name='Candlestick'
    )])
    fig.update_layout(title="Candlestick Chart", xaxis_title="Date", yaxis_title="Price", height=450)
    return fig

def rsi(dataframe, num_period=None):
    dataframe['RSI'] = pta.rsi(dataframe['Close'], length=14)
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['RSI'], name='RSI', line=dict(color='orange')))
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
    fig.update_layout(title="RSI", height=300)
    return fig

def moving_average(dataframe, num_period=None):
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], length=50)
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Open'], mode='lines', name='Open'))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['High'], mode='lines', name='High'))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Low'], mode='lines', name='Low'))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['SMA_50'], mode='lines', name='SMA 50', line=dict(color='purple')))
    fig.update_layout(title="Moving Average (SMA 50)", height=450)
    return fig

def macd(dataframe, num_period=None):
    macd_data = pta.macd(dataframe['Close'])
    dataframe['MACD'] = macd_data.iloc[:, 0]
    dataframe['MACD_Signal'] = macd_data.iloc[:, 2]
    dataframe['MACD_Hist'] = macd_data.iloc[:, 1]
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['MACD'], name='MACD Line', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['MACD_Signal'], name='Signal Line', line=dict(color='orange')))
    fig.add_trace(go.Bar(x=dataframe.index, y=dataframe['MACD_Hist'], name='Histogram', marker_color='gray'))
    fig.update_layout(title="MACD", height=300)
    return fig

def moving_average_forecast(forecast_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast_data.index[:-30],
        y=forecast_data['Close'][:-30],
        mode='lines',
        name='Close Price'
    ))
    fig.add_trace(go.Scatter(
        x=forecast_data.index[-30:],
        y=forecast_data['Close'][-30:],
        mode='lines',
        name='Future Close Price',
        line=dict(color='red')
    ))
    fig.update_layout(title="Stock Price Forecast", xaxis_title="Date", yaxis_title="Price", height=450)
    return fig
