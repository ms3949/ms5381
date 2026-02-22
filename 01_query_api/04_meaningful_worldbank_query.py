# 04_meaningful_worldbank_query.py
# World Bank API: meaningful query with formatted output
# Pairs with 01_query_api activities

# This script shows how to:
# - Query the World Bank API and build a clean dataset
# - Use pandas for readable tables and summary statistics
# - Present results in a meaningful way (trend, min/max, recent values)

# 0. Setup #################################

## 0.1 Load Packages ############################

import os  # for reading environment variables
import requests  # for making HTTP requests
from dotenv import load_dotenv  # for loading variables from .env
import pandas as pd  # for data manipulation and formatted output

## 0.2 Load Environment Variables ################

if os.path.exists(".env"):
    load_dotenv()
else:
    print(".env file not found. World Bank API works without a key.")

## 1. API Request ###########################

# World Bank API details
COUNTRY = "US"
INDICATOR = "NY.GDP.PCAP.CD"  # GDP per capita, current US$

url = f"https://api.worldbank.org/v2/country/{COUNTRY}/indicator/{INDICATOR}"

params = {
    "format": "json",
    "date": "2000:2023",
    "per_page": 100,
}

response = requests.get(url, params=params)

if response.status_code != 200:
    raise Exception(f"API request failed with status {response.status_code}")

data = response.json()
records = data[1]

## 2. Build Meaningful Dataset ###########################

# Convert to DataFrame and keep only year and value
df = pd.DataFrame([
    {"year": int(r["date"]), "gdp_per_capita_usd": r["value"]}
    for r in records
])

# Drop rows where value is missing (World Bank uses None for missing)
df = df.dropna(subset=["gdp_per_capita_usd"])
df = df.sort_values("year", ascending=False).reset_index(drop=True)

## 3. Meaningful Output ###########################

print("Status Code:", response.status_code)
print("Indicator: GDP per capita (current US$), country:", COUNTRY)
print("Records (non-missing):", len(df))
print()

# Summary statistics
print("Summary (USD):")
print(f"  Min:    {df['gdp_per_capita_usd'].min():,.0f} ({df.loc[df['gdp_per_capita_usd'].idxmin(), 'year']})")
print(f"  Max:    {df['gdp_per_capita_usd'].max():,.0f} ({df.loc[df['gdp_per_capita_usd'].idxmax(), 'year']})")
print(f"  Latest: {df['gdp_per_capita_usd'].iloc[0]:,.0f} ({df['year'].iloc[0]})")
print()

# Formatted table (first 10 years, most recent first)
print("Recent values (first 10 rows):")
print(df.head(10).to_string(index=False))
