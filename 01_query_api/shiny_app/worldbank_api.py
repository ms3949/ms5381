# worldbank_api.py
# World Bank Data API helper for Shiny app
# Fetches GDP per capita time series; returns (DataFrame, None) or (None, error_message).

import requests
import pandas as pd

API_BASE = "https://api.worldbank.org/v2"
INDICATOR_GDP_PCAP = "NY.GDP.PCAP.CD"  # GDP per capita, current US$


def fetch_gdp_per_capita(country_code: str, year_start: int, year_end: int):
    """
    Fetch GDP per capita (current US$) for one country over a year range.
    Returns (df, None) on success or (None, error_message) on failure.
    """
    # Validate inputs
    country_code = (country_code or "").strip().upper()
    if not country_code or len(country_code) != 2:
        return None, "Please enter a valid 2-letter country code (e.g. US, GB)."

    if year_start > year_end:
        return None, "Start year must be less than or equal to end year."

    if year_start < 1960 or year_end > 2030:
        return None, "Year range should be between 1960 and 2030."

    url = f"{API_BASE}/country/{country_code}/indicator/{INDICATOR_GDP_PCAP}"
    params = {
        "format": "json",
        "date": f"{year_start}:{year_end}",
        "per_page": 500,
    }

    try:
        response = requests.get(url, params=params, timeout=15)
    except requests.RequestException as e:
        return None, f"Network error: {str(e)}"

    if response.status_code != 200:
        return None, f"API request failed (HTTP {response.status_code})."

    try:
        data = response.json()
    except Exception:
        return None, "Invalid response from API."

    if not data or len(data) < 2:
        return None, "API returned no data for this country or range."

    records = data[1]
    if not records:
        return None, "No records found for this country and year range."

    df = pd.DataFrame([
        {"year": int(r["date"]), "gdp_per_capita_usd": r["value"]}
        for r in records
    ])
    df = df.dropna(subset=["gdp_per_capita_usd"])
    df = df.sort_values("year", ascending=False).reset_index(drop=True)

    if df.empty:
        return None, "No non-missing values in the selected range."

    return df, None
