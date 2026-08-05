# Monetary Policy Framework Mobile App (Python + Dash + ReportLab + Matplotlib)
# Author: Julius Conteh
# Bank of Sierra Leone - Monetary Policy Department

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from dash import Dash, dcc, html, Input, Output
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Image

# Load Excel data
data = pd.read_excel("monetary_policy_data.xlsx")

# -------------------------------
# Core Functions
# -------------------------------

def calculate_real_interest_rate(nominal, inflation):
    return round(nominal - inflation, 2)

def monetary_stance_index(policy_rate, gdp_growth, inflation_gap):
    return round(policy_rate - (gdp_growth + inflation_gap), 2)

def taylor_rule(inflation, target_inflation, output_gap,
                neutral_rate=2.0, w_infl=0.5, w_output=0.5):
    return round(neutral_rate + inflation +
                 w_infl * (inflation - target_inflation) +
                 w_output * output_gap, 2)

def exchange_rate_pass_through(exchange_rate_change, import_share):
    return round(exchange_rate_change * import_share, 2)

def arima_forecast(series, steps=3):
    model = ARIMA(series, order=(1,1,1))
    fit = model.fit()
    return fit.forecast(steps=steps)

def sarima_forecast(series, steps=3):
    model = SARIMAX(series, order=(1,1,1), seasonal_order=(1,1,1,12))
    fit = model.fit(disp=False)
    return fit.forecast(steps=steps)

def arimax_forecast(series, exog, steps=3):
    model = SARIMAX(series, exog=exog, order=(1,1,1))
    fit = model.fit(disp=False)
    return fit.forecast(steps=steps, exog=exog[-steps:])

# -------------------------------
# Explanatory Notes
# -------------------------------

EXPLANATIONS = {
    "Real Interest Rate": "A positive real interest rate indicates restrictive monetary policy, discouraging borrowing and consumption. A negative rate suggests accommodative policy that may fuel inflation.",
    "Monetary Stance Index": "A higher stance index implies restrictive policy, while a lower or negative index suggests accommodative conditions supporting growth.",
    "Taylor Rule": "The recommended policy rate reflects inflation relative to target and the output gap. A higher rate signals tightening to stabilize prices.",
    "Exchange Rate Pass-Through": "Depreciation raises import costs. With high import share, exchange rate shocks quickly translate into inflationary pressure.",
    "ARIMA Forecast": "ARIMA projects inflation based on past trends. Persistent upward forecasts suggest ongoing price pressures.",
    "SARIMA Forecast": "SARIMA captures seasonal patterns in inflation. Useful for quarterly or monthly data where seasonality matters.",
    "ARIMAX Forecast (Exchange Rate)": "ARIMAX shows how exchange rate movements influence inflation forecasts, highlighting external vulnerability.",
    "ARIMAX Forecast (Oil Price)": "ARIMAX with oil prices captures how global commodity shocks affect domestic inflation."
}

# -------------------------------
# Report Generator with Chart
# -------------------------------

def generate_report(title, result_text, forecast_series=None):
    explanation = EXPLANATIONS.get(title, "")
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 750, "Monetary Policy Department - Policy Brief")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Analysis: {title}")
    c.drawString(100, 710, f"Result: {result_text}")
    
    text_obj = c.beginText(100, 690)
    text_obj.setFont("Helvetica", 11)
    text_obj.textLines(f"Notes:\n{explanation}")
    c.drawText(text_obj)
    
    # Add chart if forecast data is available
    if forecast_series is not None:
        plt.figure(figsize=(5,3))
        plt.plot(forecast_series, marker="o", label="Forecast")
        plt.title(f"{title} Chart")
        plt.xlabel("Steps Ahead")
        plt.ylabel("Inflation (%)")
        plt.legend()
        chart_buf = BytesIO()
        plt.savefig(chart_buf, format="PNG")
        plt.close()
        chart_buf.seek(0)
        img = Image(chart_buf, width=400, height=200)
        img.drawOn(c, 100, 450)
    
    c.showPage()
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    b64 = base64.b64encode(pdf_bytes).decode()
    return f"data:application/pdf;base64,{b64}"

# -------------------------------
# Dash App Layout
# -------------------------------

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Monetary Policy Framework Dashboard", style={"textAlign":"center"}),

    dcc.Dropdown(
        id="analysis",
        options=[
            {"label":"Real Interest Rate","value":"real"},
            {"label":"Monetary Stance Index","value":"stance"},
            {"label":"Taylor Rule","value":"taylor"},
            {"label":"Exchange Rate Pass-Through","value":"pass"},
            {"label":"ARIMA Forecast","value":"arima"},
            {"label":"SARIMA Forecast","value":"sarima"},
            {"label":"ARIMAX Forecast (Exchange Rate)","value":"arimax_ex"},
            {"label":"ARIMAX Forecast (Oil Price)","value":"arimax_oil"}
        ],
        value="real"
    ),

    html.Div(id="result", style={"marginTop":"20px", "fontSize":"18px"}),

    html.A("Download Report", id="download-link", href="", target="_blank",
           style={"display":"block", "marginTop":"20px", "fontSize":"16px"})
])

# -------------------------------
# Callbacks
# -------------------------------

@app.callback(
    [Output("result","children"),
     Output("download-link","href")],
    Input("analysis","value")
)
def run_analysis(choice):
    if choice == "real":
        result = f"{calculate_real_interest_rate(data['NominalRate'][0], data['Inflation'][0])}%"
        report = generate_report("Real Interest Rate", result)
        return f"Real Interest Rate: {result}", report
    elif choice == "stance":
        result = f"{monetary_stance_index(data['PolicyRate'][0], data['GDPGrowth'][0], 2)}"
        report = generate_report("Monetary Stance Index", result)
        return f"Monetary Stance Index: {result}", report
    elif choice == "taylor":
        result = f"{taylor_rule(data['Inflation'][0], 10, 2)}%"
        report = generate_report("Taylor Rule", result)
        return f"Taylor Rule Policy Rate: {result}", report
    elif choice == "pass":
        result = f"{exchange_rate_pass_through(10, data['ImportShare'][0])}%"
        report = generate_report("Exchange Rate Pass-Through", result)
        return f"Inflation Impact: {result}", report
    elif choice == "arima":
        forecast = arima_forecast(data['Inflation'], steps=3)
        report = generate_report("ARIMA Forecast", str(forecast.tolist()), forecast_series=forecast)
        return f"ARIMA Forecast: {forecast.tolist()}", report
    elif choice == "sarima":
        forecast = sarima_forecast(data['Inflation'], steps=3)
        report = generate_report("SARIMA Forecast", str(forecast.tolist()), forecast_series=forecast)
        return f"SARIMA Forecast: {forecast.tolist()}", report
    elif choice == "arimax_ex":
        forecast = arimax_forecast(data['Inflation'], data['ExchangeRate'], steps=3)
        report = generate_report("ARIMAX Forecast (Exchange Rate)", str(forecast.tolist()), forecast_series=forecast)
        return f"ARIMAX Forecast (Exchange Rate): {forecast.tolist()}", report
    elif choice == "arimax_oil":
        forecast = arimax_forecast(data['Inflation'], data['OilPrice'], steps=3)
        report = generate_report("ARIMAX Forecast (Oil Price)", str(forecast.tolist()), forecast_series=forecast)
        return f"ARIMAX Forecast (Oil Price): {forecast.tolist()}", report

if __name__ == "__main__":
    app.run_server(debug=True)
