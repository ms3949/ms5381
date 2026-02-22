# 06_multi_country_gdp.py
# World Bank API: GDP per capita for multiple countries
# Pairs with 01_query_api activities

# This script shows how to:
# - Query the World Bank API for several countries (US, UK, Canada, China, Mexico)
# - Extract the most recent non-null GDP per capita for each
# - Display results in a pandas DataFrame table

# 0. Setup #################################

## 0.1 Load Packages ############################

import requests  # for making HTTP requests
import pandas as pd  # for data manipulation and table display

## 1. Fetch Data ###########################

# Countries and World Bank ISO codes
countries = ["US", "GB", "CA", "CN", "MX"]  # USA, UK, Canada, China, Mexico
indicator = "NY.GDP.PCAP.CD"  # GDP per capita, current US$


def get_gdp_per_capita(country_code):
    """Fetch GDP per capita for a country; return (value, year) of most recent non-null, or (None, None)."""
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=5000"
    response = requests.get(url)
    if response.status_code != 200:
        return None, None
    data = response.json()
    # data[1] contains the actual records (API returns newest first)
    if len(data) < 2:
        return None, None
    for record in data[1]:
        if record["value"] is not None:
            return record["value"], record["date"]
    return None, None


# Fetch data for all countries
results = []
for country in countries:
    gdp, year = get_gdp_per_capita(country)
    results.append({
        "Country": country,
        "GDP per Capita (USD)": gdp,
        "Year": year,
    })

## 2. Display ###########################

# Convert to DataFrame for nice table display
df = pd.DataFrame(results)
print(df)
