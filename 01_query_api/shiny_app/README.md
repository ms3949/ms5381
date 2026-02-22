# World Bank GDP Explorer (Shiny for Python)

Shiny app built on [`my_good_query.py`](../my_good_query.py). Fetches GDP per capita (current US$) from the World Bank API and displays results in a table and time series chart.

## Run locally

1. Create a virtual environment (recommended) and install dependencies:

   ```bash
   cd 01_query_api/shiny_app
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Start the app:

   ```bash
   shiny run app.py
   ```

3. Open the URL shown in the terminal (e.g. http://127.0.0.1:8000).

## Options

- **Country**: Choose from the dropdown (ISO2 codes).
- **Start / End year**: Valid range 1960–2030.
- **Run query**: Executes the API request; loading and errors are shown in the main panel.

No API key is required for the World Bank API. A `.env` file in the project root is optional (used for other APIs if you extend the app).
