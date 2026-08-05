# Monetary Policy Framework Calculator
# Author: Julius Conteh
# Bank of Sierra Leone - Monetary Policy Department
# -------------------------------------------------
# This program calculates key indicators useful in monetary policy analysis:
# - Real interest rate
# - Monetary stance index
# - Policy rate simulations
# - Taylor Rule recommendation
# - Exchange rate pass-through
# - Inflation forecast (ARIMA, SARIMA, ARIMAX)
# -------------------------------------------------

import math
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

# -------------------------------
# Core Functions
# -------------------------------

def calculate_real_interest_rate(nominal_rate: float, inflation_rate: float) -> float:
    """Calculate the real interest rate using Fisher equation."""
    return round(nominal_rate - inflation_rate, 2)


def monetary_stance_index(policy_rate: float, gdp_growth: float, inflation_gap: float) -> float:
    """Measure stance of monetary policy (restrictive vs accommodative)."""
    return round(policy_rate - (gdp_growth + inflation_gap), 2)


def simulate_policy_change(current_rate: float, change_amount: float) -> float:
    """Simulate effect of changing the policy rate."""
    return round(current_rate + change_amount, 2)


def taylor_rule(inflation: float, target_inflation: float, output_gap: float,
                neutral_rate: float = 2.0, weight_inflation: float = 0.5,
                weight_output: float = 0.5) -> float:
    """
    Taylor Rule: recommends optimal policy rate.
    Formula: i = r* + π + 0.5(π - π*) + 0.5(y_gap)
    """
    return round(neutral_rate + inflation + weight_inflation * (inflation - target_inflation)
                 + weight_output * output_gap, 2)


def exchange_rate_pass_through(exchange_rate_change: float, import_share: float) -> float:
    """Estimate inflation impact from exchange rate changes."""
    return round(exchange_rate_change * import_share, 2)


def inflation_forecast_arima(series, order=(1,1,1), steps=5):
    """Forecast inflation using ARIMA model."""
    model = ARIMA(series, order=order)
    fit = model.fit()
    forecast = fit.forecast(steps=steps)
    return forecast


def sarima_forecast(series, order=(1,1,1), seasonal_order=(0,0,0,0), steps=5):
    """Forecast inflation using SARIMA model."""
    model = SARIMAX(series, order=order, seasonal_order=seasonal_order)
    fit = model.fit(disp=False)
    forecast = fit.forecast(steps=steps)
    return forecast


def arimax_forecast(series, exog, order=(1,1,1), steps=5):
    """Forecast inflation using ARIMAX model with exogenous variable."""
    model = SARIMAX(series, exog=exog, order=order)
    fit = model.fit(disp=False)
    forecast = fit.forecast(steps=steps, exog=exog[-steps:])
    return forecast


def load_economic_data(filename: str, sheet_name: str = "Sheet1") -> pd.DataFrame:
    """Load economic data from Excel file."""
    return pd.read_excel(filename, sheet_name=sheet_name)


def plot_policy_effects(data: pd.DataFrame) -> None:
    """Plot trends of nominal rate, inflation, and GDP growth."""
    plt.figure(figsize=(8, 5))
    plt.plot(data['Year'], data['NominalRate'], label='Nominal Rate')
    plt.plot(data['Year'], data['Inflation'], label='Inflation')
    plt.plot(data['Year'], data['GDPGrowth'], label='GDP Growth')
    plt.xlabel("Year")
    plt.ylabel("Percentage (%)")
    plt.title("Policy Effects Over Time")
    plt.legend()
    plt.show()


def main_menu():
    """User interaction menu."""
    print("=== Monetary Policy Framework Calculator ===")
    print("1. Calculate Real Interest Rate")
    print("2. Calculate Monetary Stance Index")
    print("3. Simulate Policy Change")
    print("4. Taylor Rule Recommendation")
    print("5. Exchange Rate Pass-Through")
    print("6. Inflation Forecast (ARIMA)")
    print("7. SARIMA Forecast")
    print("8. ARIMAX Forecast (Exchange Rate)")
    print("9. ARIMAX Forecast (Oil Price)")
    choice = input("Enter choice: ")

    data = load_economic_data("monetary_policy_data.xlsx")

    if choice == "1":
        i = float(input("Enter nominal interest rate (%): "))
        pi = float(input("Enter inflation rate (%): "))
        print("Real Interest Rate:", calculate_real_interest_rate(i, pi), "%")

    elif choice == "2":
        pr = float(input("Enter policy rate (%): "))
        gdp = float(input("Enter GDP growth (%): "))
        gap = float(input("Enter inflation gap (%): "))
        print("Monetary Stance Index:", monetary_stance_index(pr, gdp, gap))

    elif choice == "3":
        cr = float(input("Enter current policy rate (%): "))
        change = float(input("Enter change amount (%): "))
        print("New Policy Rate:", simulate_policy_change(cr, change), "%")

    elif choice == "4":
        pi = float(input("Enter current inflation (%): "))
        pi_target = float(input("Enter target inflation (%): "))
        y_gap = float(input("Enter output gap (%): "))
        print("Taylor Rule Policy Rate:", taylor_rule(pi, pi_target, y_gap), "%")

    elif choice == "5":
        er_change = float(input("Enter exchange rate change (%): "))
        import_share = float(input("Enter import share of GDP (%): "))
        print("Inflation Impact:", exchange_rate_pass_through(er_change, import_share), "%")

    elif choice == "6":
        forecast = inflation_forecast_arima(data['Inflation'], steps=3)
        print("ARIMA Inflation Forecast:", forecast)

    elif choice == "7":
        forecast = sarima_forecast(data['Inflation'], steps=3)
        print("SARIMA Inflation Forecast:", forecast)

    elif choice == "8":
        forecast = arimax_forecast(data['Inflation'], data['ExchangeRate'], steps=3)
        print("ARIMAX Forecast (Exchange Rate):", forecast)

    elif choice == "9":
        forecast = arimax_forecast(data['Inflation'], data['OilPrice'], steps=3)
        print("ARIMAX Forecast (Oil Price):", forecast)

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main_menu()
