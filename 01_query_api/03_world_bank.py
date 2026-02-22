# 03_world_bank.py
# World Bank API: US GDP per capita (current US$)
# Pairs with 01_query_api activities

# This script shows how to:
# - Load environment variables from .env (optional for this API)
# - Query the World Bank API with configurable country and indicator
# - Handle errors and extract records from the response

# 0. Setup #################################

## 0.1 Load Packages ############################

import os  # for reading environment variables
import requests  # for making HTTP requests
from dotenv import load_dotenv  # for loading variables from .env

## 0.2 Load Environment Variables ################

# Load environment variables (API key not required, but pattern is demonstrated)
if os.path.exists(".env"):
    load_dotenv()
else:
    print(".env file not found. World Bank API works without a key.")

# Demonstrate secure loading (not required for this API)
api_key = os.getenv("WORLD_BANK_API_KEY")

## 1. API Request ###########################

# World Bank API details
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

# Basic error handling
if response.status_code != 200:
    raise Exception(f"API request failed with status {response.status_code}")

data = response.json()

## 2. Inspect Response ###########################

# Extract records (second element contains data)
records = data[1]

print("Status Code:", response.status_code)
print("Number of records:", len(records))
print("\nFirst 10 records:\n")

for row in records[:10]:
    print({
        "year": row["date"],
        "gdp_per_capita_usd": row["value"],
    })
