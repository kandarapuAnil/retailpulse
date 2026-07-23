
# utils.py

import pandas as pd
import os

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")


# ==========================================================
# HELPER
# ==========================================================

def _load_csv(filename):
    path = os.path.join(DATA_DIR, filename)

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


# ==========================================================
# KPI DATA
# ==========================================================

def load_kpi():
    df = _load_csv("dashboard_kpi.csv")

    if not df.empty:
        return df

    return pd.DataFrame({
        "Total Revenue": [8798233.74],
        "Customers": [4312],
        "Inventory Items": [5000],
        "Average Revenue": [2040.00]
    })


# ==========================================================
# MONTHLY SALES
# ==========================================================

def load_monthly():
    df = _load_csv("dashboard_monthly.csv")

    if not df.empty:
        return df

    dates = pd.date_range("2024-01-01", periods=12, freq="ME")

    return pd.DataFrame({
        "InvoiceDate": dates,
        "Revenue": [500000 + i * 20000 for i in range(12)]
    })


# ==========================================================
# PRODUCTS
# ==========================================================

def load_products():
    df = _load_csv("dashboard_products.csv")

    if not df.empty:
        return df

    return pd.DataFrame({
        "Description": ["Product A", "Product B", "Product C"],
        "Revenue": [10000, 9000, 8000]
    })


# ==========================================================
# COUNTRY SALES
# ==========================================================

def load_country():
    df = _load_csv("dashboard_country.csv")

    if not df.empty:
        return df

    return pd.DataFrame({
        "Country": [
            "United Kingdom",
            "Germany",
            "France",
            "USA",
            "Spain"
        ],
        "Revenue": [
            5000000,
            1200000,
            900000,
            700000,
            500000
        ]
    })


# ==========================================================
# CUSTOMER SEGMENTS
# ==========================================================

def load_segments():
    """
    Loads customer segmentation data.

    Expected columns:
    CustomerID
    Recency
    Frequency
    Monetary
    Cluster
    """

    possible_files = [
        "customer_segments.csv",
        "customer_features.csv",
        "dashboard_customers.csv"
    ]

    for file in possible_files:
        path = os.path.join(DATA_DIR, file)

        if os.path.exists(path):
            return pd.read_csv(path)

    return pd.DataFrame({
        "CustomerID": [1, 2, 3, 4, 5],
        "Recency": [10, 25, 40, 12, 7],
        "Frequency": [20, 15, 10, 18, 30],
        "Monetary": [5000, 3000, 1500, 4500, 8000],
        "Cluster": [0, 1, 2, 0, 1]
    })


# ==========================================================
# FORECASTS
# ==========================================================

def load_prophet_forecast():
    return _load_csv("forecast_prophet.csv")


def load_lstm_forecast():
    return _load_csv("forecast_lstm.csv")


def load_hybrid_forecast():
    return _load_csv("hybrid_forecast.csv")


def load_forecast():
    df = load_hybrid_forecast()

    if not df.empty:
        return df

    dates = pd.date_range("2024-01-01", periods=30, freq="D")

    return pd.DataFrame({
        "ds": dates,
        "Actual": [1000 + i * 10 for i in range(30)],
        "Hybrid": [1000 + i * 10 + (i % 5) * 5 for i in range(30)]
    })


# ==========================================================
# CURRENCY FORMATTER
# ==========================================================
def format_currency(value):
    return f"₹{value:,.2f}"