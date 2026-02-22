# my_good_query.py
# Meaningful API query: World Bank GDP per capita time series
# Pairs with LAB_your_good_api_query.md

# This script implements a single API query that returns 10+ rows of time series
# data (GDP per capita by year), suitable for analysis or a reporter-style app.
# It loads .env, uses clear parameters and error handling, and documents the
# API, endpoint, and expected data.

# --- API documentation (for LAB Stage 3) ---
# API name:     World Bank Data API
# Endpoint:     GET https://api.worldbank.org/v2/country/{country}/indicator/{indicator}
# Parameters:   format=json, date=YYYY:YYYY (range), per_page=N
# Expected:     Multiple records (one per year); key fields: date (year), value (GDP per capita USD)
# Data shape:   List of dicts in response[1]; each dict has "date", "value", "country", etc.

# 0. Setup #################################

## 0.1 Load Packages ############################

import os  # for reading environment variables
import requests  # for making HTTP requests
from dotenv import load_dotenv  # for loading variables from .env
import pandas as pd  # for data manipulation and formatted output

## 0.2 Load Environment Variables ################

# Load .env if present (World Bank API works without a key; pattern for other APIs)
if os.path.exists(".env"):
    load_dotenv()
else:
    print(".env file not found. World Bank API works without a key.")

## 1. API Request ###########################

# Query design: one country, 2000–2023 → 20+ rows of time series data
API_NAME = "World Bank Data API"
COUNTRY = "US"
INDICATOR = "NY.GDP.PCAP.CD"  # GDP per capita, current US$

url = f"https://api.worldbank.org/v2/country/{COUNTRY}/indicator/{INDICATOR}"

params = {
    "format": "json",
    "date": "2000:2023",
    "per_page": 100,
}

response = requests.get(url, params=params)

# Error handling: fail clearly if request fails
if response.status_code != 200:
    raise Exception(f"API request failed with status {response.status_code}")

data = response.json()

# World Bank returns [metadata, records]; ensure we have records
if not data or len(data) < 2:
    raise Exception("API response missing data array")

records = data[1]

## 2. Build Dataset ###########################

# Convert to DataFrame; keep year and value for reporting
df = pd.DataFrame([
    {"year": int(r["date"]), "gdp_per_capita_usd": r["value"]}
    for r in records
])

# Drop rows where value is missing
df = df.dropna(subset=["gdp_per_capita_usd"])
df = df.sort_values("year", ascending=False).reset_index(drop=True)

## 3. Document and Display Results ###########################

# Document: number of records, key fields, structure (per LAB Stage 3)
print("--- Query summary ---")
print("API:", API_NAME)
print("Endpoint: country/{}/indicator/{}".format(COUNTRY, INDICATOR))
print("Parameters:", params)
print("Number of records (non-missing):", len(df))
print("Key fields: year, gdp_per_capita_usd")
print()

# Show first 10+ rows for submission screenshot
print("Data (first 10+ rows):")
print(df.head(12).to_string(index=False))
