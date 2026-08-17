# 📈 Quantitative Stock Analytics, Valuation Modeling (CAPM) & Time Series Forecasting Engine

[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Statsmodels](https://img.shields.io/badge/Modeling-Statsmodels-green?style=for-the-badge)](https://www.statsmodels.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An end-to-end quantitative financial analytics and predictive modeling dashboard developed in Python. This platform integrates real-time equity data extraction, fundamental corporate valuation, technical momentum indicators, modern portfolio theory (Capital Asset Pricing Model), and statistical time-series forecasting using auto-integrated ARIMA models.

---

## 🌟 Application Modules

1. **📊 Real-Time Stock & Technical Analysis (`Stock_Analysis.py`)**
   - Live ingestion of equity data and corporate profiles from the Yahoo Finance API (`yfinance`).
   - Fundamental valuation dashboards displaying key ratios: Market Capitalization, Trailing P/E, Trailing EPS, Quick Ratio, Profit Margins, and Debt-to-Equity.
   - Multi-period interactive OHLC line charts and Candlestick trajectories ($5\text{D}$, $1\text{M}$, $6\text{M}$, $\text{YTD}$, $1\text{Y}$, $5\text{Y}$).
   - Momentum oscillators and trend analysis: **14-period RSI**, **MACD (12, 26, 9)**, and **50-day Simple Moving Average (SMA)**.

2. **📈 Time Series Price Forecasting (`stock_prediction.py`)**[cite: 2]
   - Automated stationarity diagnostics via the **Augmented Dickey-Fuller (ADF)** test[cite: 2].
   - 7-day rolling window smoothing to mitigate high-frequency market noise[cite: 2].
   - Dynamic differencing order ($d$) optimization[cite: 2].
   - 30-day forward price horizon projections modeled via **ARIMA** with out-of-sample Root Mean Squared Error (**RMSE**) evaluation[cite: 2].

3. **💼 Capital Asset Pricing Model Portfolio Valuation (`CAPM_Return.py`)**[cite: 2]
   - Benchmark synchronization against the **S&P 500 (`^GSPC`)** index[cite: 2].
   - Base-$1.0$ price normalization for direct comparison of multi-stock cumulative performance[cite: 1, 2].
   - Calculation of daily percentage returns and annualized expected returns based on systematic asset risk[cite: 1, 2].

4. **📉 Systematic Risk & Sensitivity Regression (`CAPM_Beta.py`)**[cite: 2]
   - Ordinary Least Squares (OLS) linear regression between individual stock returns and market benchmark returns[cite: 1, 2].
   - Direct estimation of asset **Beta ($\beta$)** and **Alpha ($\alpha$)**[cite: 1, 2].

---

## 📐 Mathematical & Theoretical Foundations

### 1. Capital Asset Pricing Model (CAPM) & Linear Regression

The **Capital Asset Pricing Model (CAPM)** describes the relationship between systematic risk and expected return for assets, particularly equities[cite: 1]. It quantifies the required rate of return an investor should demand given the asset's risk exposure relative to the broad market[cite: 1].

#### Standard CAPM Equation:
$$E[R_i] = R_f + \beta_i \left( E[R_m] - R_f \right)$$

Where:
* $E[R_i]$: Expected annualized return on asset $i$[cite: 1].
* $R_f$: Risk-Free Rate of return (e.g., U.S. Treasury yield; assumed at $0.0$ baseline in the application)[cite: 1, 2].
* $E[R_m]$: Expected annualized return of the broad market benchmark (annualized from S&P 500 daily returns via $E[R_m] = \overline{R}_m \times 252$)[cite: 1, 2].
* $\left( E[R_m] - R_f \right)$: Market Risk Premium[cite: 1].
* $\beta_i$: Beta coefficient (systematic risk) of security $i$[cite: 1].

#### Beta ($\beta$) and Alpha ($\alpha$) Estimation:
The application fits a first-degree polynomial (Ordinary Least Squares regression) over the daily percentage returns of asset $i$ and market $m$[cite: 1, 2]:

$$R_{i,t} = \alpha_i + \beta_i R_{m,t} + \epsilon_t$$

Where:
$$\beta_i = \frac{\text{Cov}(R_i, R_m)}{\text{Var}(R_m)}$$

$$\alpha_i = \overline{R}_i - \beta_i \overline{R}_m$$

* **$\beta > 1.0$:** High-beta asset; more volatile than the market[cite: 1].
* **$\beta = 1.0$:** Asset moves in lockstep with the market.
* **$0 < \beta < 1.0$:** Lower volatility than the market[cite: 1].
* **$\alpha > 0$:** Positive excess return generated independently of market movement.

---

### 2. Daily Returns & Cumulative Normalization

#### Daily Percentage Return:
$$R_t = \left( \frac{P_t - P_{t-1}}{P_{t-1}} \right) \times 100$$
[cite: 1, 2]

Where $P_t$ represents the asset close price at trading day $t$[cite: 1, 2].

#### Price Normalization (Base 1.0):
To allow fair comparison across stocks trading at vastly different price levels, daily prices are normalized relative to day zero[cite: 1, 2]:

$$P_{t,\text{norm}} = \frac{P_t}{P_0}$$
[cite: 1, 2]

---

### 3. Time Series Modeling (ADF & ARIMA)

Financial asset prices are typically non-stationary processes featuring stochastic trends and changing variance. To produce reliable forecasts, the series must first be stabilized.

#### A. 7-Day Rolling Window Smoothing
High-frequency volatility and intraday noise are filtered using a 7-day rolling moving average[cite: 2]:

$$\text{MA}_{7,t} = \frac{1}{7} \sum_{k=0}^{6} P_{t-k}$$

#### B. Stationarity Diagnostic (Augmented Dickey-Fuller Test)
The application evaluates the null hypothesis $H_0$ that a unit root is present in the time series (non-stationary)[cite: 2]:

$$\Delta Y_t = \alpha + \beta t + \gamma Y_{t-1} + \sum_{j=1}^{p} \delta_j \Delta Y_{t-j} + \epsilon_t$$

* If the calculated $p\text{-value} > 0.05$, the null hypothesis is accepted, indicating non-stationarity[cite: 2].
* The series is iteratively differenced ($\Delta^d Y_t = Y_t - Y_{t-1}$) until $p\text{-value} \le 0.05$, automatically deriving the optimal integration order $d$[cite: 2].

#### C. Autoregressive Integrated Moving Average Model: $\text{ARIMA}(p, d, q)$
The stationary differenced series $X_t = \Delta^d Y_t$ is modeled via combined auto-regressive and moving-average terms[cite: 2]:

$$X_t = c + \sum_{i=1}^{p} \phi_i X_{t-i} + \epsilon_t + \sum_{j=1}^{q} \theta_j \epsilon_{t-j}$$

Where:
* $p$: Order of the autoregressive (AR) model (lagged observations)[cite: 2].
* $d$: Degree of differencing required for stationarity[cite: 2].
* $q$: Order of the moving average (MA) model (lagged forecast errors)[cite: 2].
* $\epsilon_t \sim \mathcal{N}(0, \sigma^2)$: White noise error term.

#### D. Evaluation Metric: Root Mean Squared Error (RMSE)
Out-of-sample predictive performance on the test split (last 30 trading days) is measured using RMSE[cite: 2]:

$$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{t=1}^{N} \left( y_t - \hat{y}_t \right)^2}$$

---

### 4. Technical Indicators

#### A. Relative Strength Index (RSI - 14 Periods)
RSI measures the speed and change of price movements to identify overbought or oversold conditions:

$$\text{RSI} = 100 - \left( \frac{100}{1 + \text{RS}} \right)$$

$$\text{RS} = \frac{\text{Exponential Moving Average of 14-day Gains}}{\text{Exponential Moving Average of 14-day Losses}}$$

* $\text{RSI} \ge 70$: Overbought (potential reversal/pullback zone)[cite: 2].
* $\text{RSI} \le 30$: Oversold (potential buying opportunity)[cite: 2].

#### B. Moving Average Convergence Divergence (MACD)
$$\text{MACD Line} = \text{EMA}_{12}(\text{Close}) - \text{EMA}_{26}(\text{Close})$$

$$\text{Signal Line} = \text{EMA}_{9}(\text{MACD Line})$$

$$\text{MACD Histogram} = \text{MACD Line} - \text{Signal Line}$$
[cite: 2]

---

