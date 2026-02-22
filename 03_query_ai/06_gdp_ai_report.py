# 06_gdp_ai_report.py
# World Bank GDP Data + OpenAI Economic Report
# Pairs with 03_query_ai materials

# This script fetches US GDP data from the World Bank API, computes growth
# and summary stats, then uses OpenAI to generate a short economic report.
# Students learn end-to-end: API → pandas → prompt → LLM output.

# 0. SETUP ###################################

## 0.1 Load Packages #################################

import os
import requests  # for World Bank API
import pandas as pd  # for data manipulation
from openai import OpenAI  # for report generation

## 0.2 Configuration #################################

COUNTRY = "US"
INDICATOR = "NY.GDP.MKTP.CD"  # GDP (current US$)
START_YEAR = 2018
END_YEAR = 2023

# OpenAI client; uses OPENAI_API_KEY from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. QUERY WORLD BANK API ###################################

# Fetch indicator data for a country and date range
# Returns list of records from the API response
def fetch_world_bank_data(country, indicator, start, end):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    params = {
        "format": "json",
        "date": f"{start}:{end}",
        "per_page": 100
    }

    response = requests.get(url, params=params)
    data = response.json()

    if len(data) < 2:
        raise Exception("No data returned from API")

    records = data[1]
    return records


# 2. PROCESS DATA ###################################

# Build DataFrame, compute GDP in trillions and YoY growth, return summary stats
def process_data(records):
    df = pd.DataFrame(records)

    df = df[["date", "value"]]
    df = df.dropna()
    df["date"] = df["date"].astype(int)
    df = df.sort_values("date")

    df["gdp_trillions"] = df["value"] / 1e12
    df["growth_rate"] = df["value"].pct_change() * 100

    avg_growth = df["growth_rate"].mean()

    summary_stats = {
        "years_analyzed": len(df),
        "average_growth_rate_percent": round(avg_growth, 2),
        "highest_growth_year": int(df.loc[df["growth_rate"].idxmax()]["date"]),
        "lowest_growth_year": int(df.loc[df["growth_rate"].idxmin()]["date"])
    }

    return df, summary_stats


# 3. FORMAT FOR AI ###################################

# Turn DataFrame and stats into a single text block for the LLM prompt
def format_data_for_ai(df, stats):
    formatted_data = ""

    for _, row in df.iterrows():
        formatted_data += (
            f"Year: {int(row['date'])}, "
            f"GDP (Trillions USD): {row['gdp_trillions']:.2f}, "
            f"Growth Rate (%): "
            f"{0 if pd.isna(row['growth_rate']) else round(row['growth_rate'], 2)}\n"
        )

    structured_input = f"""
Economic Data Summary:

{formatted_data}

Aggregate Statistics:
Years Analyzed: {stats['years_analyzed']}
Average Growth Rate: {stats['average_growth_rate_percent']}%
Highest Growth Year: {stats['highest_growth_year']}
Lowest Growth Year: {stats['lowest_growth_year']}
"""

    return structured_input


# 4. AI REPORT GENERATION ###################################

# Send structured data to OpenAI and return the model's report text
def generate_ai_report(structured_data):
    prompt = f"""
You are a senior macroeconomic strategist preparing a briefing for a policy board.

Using the structured GDP data below:

1. Write a 3-sentence executive summary focused on economic trajectory and volatility.
2. Provide 3 analytical insights that interpret the trend (not just restate data).
3. Provide 1 forward-looking recommendation grounded in the trend.

Use a professional tone.
Reference numerical patterns where relevant.
Avoid copying raw lines directly.
Keep total response under 250 words.

DATA:
{structured_data}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert economic analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# 5. MAIN EXECUTION ###################################

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Set OPENAI_API_KEY in your environment (e.g. export OPENAI_API_KEY=sk-...)")
        exit(1)

    print("Fetching data from World Bank API...")
    records = fetch_world_bank_data(COUNTRY, INDICATOR, START_YEAR, END_YEAR)

    print("Processing data...")
    df, stats = process_data(records)

    print("Formatting data for AI...")
    structured_data = format_data_for_ai(df, stats)

    print("Generating AI report...")
    report = generate_ai_report(structured_data)

    print("\n" + "=" * 60)
    print("AI-GENERATED ECONOMIC REPORT")
    print("=" * 60 + "\n")
    print(report)
