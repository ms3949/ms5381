# 07_top10_gdp_countries.py
# World Bank API: top 10 countries by GDP per capita
# Pairs with 01_query_api activities

# This script fetches GDP per capita (current US$) for all countries from the
# World Bank Open Data API, then sorts and displays the top 10.

# -------------------------------------------
# WORLD BANK API: GDP PER CAPITA (NY.GDP.PCAP.CD)
# -------------------------------------------
# API Name: World Bank Open Data API
# Purpose: Fetch GDP per capita (current US$) for all countries
# Endpoint: https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json
# Indicator: NY.GDP.PCAP.CD
# Parameters:
#   - country_code: ISO 2- or 3-letter country code (e.g., US, GB, CN)
#   - indicator: World Bank indicator code (NY.GDP.PCAP.CD)
#   - format=json: return data in JSON format
#   - per_page=5000: fetch all available records in one request
# Expected data (JSON):
#   - data[0]: metadata (total records, pages, per_page)
#   - data[1]: array of yearly records
#       * country: dictionary with 'id' (ISO code) and 'value' (country name)
#       * date: year (string)
#       * value: GDP per capita (numeric, may be None)
#       * indicator: dictionary with 'id' and 'value'
#       * unit, obs_status, decimal: additional metadata
# -------------------------------------------

# 0. Setup #################################

## 0.1 Load Packages ############################

import requests  # for making HTTP requests
import pandas as pd  # for data manipulation and table display

## 1. Fetch Countries ###########################


def get_countries():
    """Fetch country codes from World Bank API; exclude aggregates (e.g. 'World')."""
    url = "https://api.worldbank.org/v2/country?format=json&per_page=500"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    # data[1] contains the list of countries
    # Each country record includes: id, name, region (id, value), incomeLevel, etc.
    # We exclude aggregates (NA region) like 'World' or 'OECD'
    countries = [c["id"] for c in data[1] if c["region"]["id"] != "NA"]
    return countries


def get_latest_gdp(country_code):
    """Return (value, year) of most recent non-null GDP per capita, or (None, None)."""
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.PCAP.CD?format=json&per_page=5000"
    response = requests.get(url)
    if response.status_code != 200:
        return None, None
    data = response.json()
    # Check if data is valid
    if len(data) < 2:
        return None, None
    # data[1] contains yearly records (most recent first)
    # Each record includes: value (may be None), date, country, indicator
    # Return the most recent year with a non-null value
    for record in data[1]:
        if record["value"] is not None:
            return record["value"], record["date"]
    return None, None


## 2. Fetch GDP for All Countries ###########################

# Get ISO codes for all countries; store GDP per capita data
countries = get_countries()
results = []

for country in countries:
    gdp, year = get_latest_gdp(country)
    if gdp is not None:
        results.append({
            "Country": country,
            "GDP per Capita (USD)": gdp,
            "Year": year,
        })

## 3. Convert to DataFrame and Display ###########################

df = pd.DataFrame(results)

# Sort by GDP per capita descending and get top 10
top_10 = df.sort_values(by="GDP per Capita (USD)", ascending=False).head(10)
top_10 = top_10.reset_index(drop=True)

print(top_10)

# -------------------------------------------
# DATA STRUCTURE SUMMARY:
# - Number of records: equal to number of countries with GDP data
# - Each record contains:
#     * Country: ISO country code
#     * GDP per Capita (USD): numeric value
#     * Year: latest year with available data
# - Output is sorted descending by GDP per capita
# - The DataFrame shows top 10 countries by GDP per capita
# -------------------------------------------
