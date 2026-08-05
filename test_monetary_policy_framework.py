# Test file for Monetary Policy Framework Calculator
# Run with: pytest test_monetary_policy_framework.py

import pandas as pd
from monetary_policy_framework import (
    calculate_real_interest_rate,
    monetary_stance_index,
    simulate_policy_change,
    taylor_rule,
    exchange_rate_pass_through,
    inflation_forecast_arima,
    sarima_forecast,
    arimax_forecast
)

def test_calculate_real_interest_rate():
    assert calculate_real_interest_rate(15, 10) == 5.0
    assert calculate_real_interest_rate(20, 5) == 15.0

def test_monetary_stance_index():
    assert monetary_stance_index(15, 5, 3) == 7.0
    assert monetary_stance_index(10, 4, 2) == 4.0

def test_simulate_policy_change():
    assert simulate_policy_change(15, -2) == 13.0
    assert simulate_policy_change(10, 5) == 15.0

def test_taylor_rule():
    assert taylor_rule(10, 8, 2) == 14.0
    assert taylor_rule(5, 5, 0) == 7.0

def test_exchange_rate_pass_through():
    assert exchange_rate_pass_through(10, 0.3) == 3.0
    assert exchange_rate_pass_through(-5, 0.4) == -2.0

def test_inflation_forecast_arima():
    series = pd.Series([10, 12, 14, 13, 15])
    forecast = inflation_forecast_arima(series, order=(1,1,1), steps=2)
    assert len(forecast) == 2

def test_sarima_forecast():
    series = pd.Series([10, 12, 14, 13, 15])
    forecast = sarima_forecast(series, order=(1,1,1), steps=2)
    assert len(forecast) == 2

def test_arimax_forecast():
    series = pd.Series([10, 12, 14, 13, 15])
    exog = pd.Series([7500, 7600, 7700, 7800, 7900])
    forecast = arimax_forecast(series, exog, order=(1,1,1), steps=2)
    assert len(forecast) == 2