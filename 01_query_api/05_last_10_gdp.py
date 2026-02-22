# 05_last_10_gdp.py
# World Bank API: last 10 years GDP per capita (current US$)
# Pairs with 01_query_api activities

# This script fetches US GDP per capita, sorts by year ascending,
# and prints the last 10 records (most recent 10 years).

import requests  # for making HTTP requests

# World Bank API endpoint
url = "https://api.worldbank.org/v2/country/US/indicator/NY.GDP.PCAP.CD"

params = {
    "format": "json",
    "per_page": 100,  # ensure we get enough records
}

response = requests.get(url, params=params)

# Check request success
if response.status_code != 200:
    raise Exception(f"Request failed with status {response.status_code}")

data = response.json()

# The actual records are in index 1
records = data[1]

# Sort by year (date) ascending, then take last 10
records_sorted = sorted(records, key=lambda x: int(x["date"]))
last_10 = records_sorted[-10:]

print("Status Code:", response.status_code)
print("\nLast 10 GDP per capita records (USD):\n")

for r in last_10:
    year = r["date"]
    value = r["value"]
    print(f"  {year}: {value:,.0f}" if value else f"  {year}: (no data)")
