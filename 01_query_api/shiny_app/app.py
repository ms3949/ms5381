# app.py
# Shiny for Python: World Bank GDP per capita explorer
# Built on 01_query_api/my_good_query.py

# This app lets users choose a country and year range, run the World Bank API
# query, and view results in a table and chart with loading and error handling.

import os
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from dotenv import load_dotenv

from worldbank_api import fetch_gdp_per_capita

# Load .env if present (World Bank API works without a key)
if os.path.exists(".env"):
    load_dotenv()
elif os.path.exists("../.env"):
    load_dotenv("../.env")

# Common countries for the dropdown (ISO2 codes and labels)
COUNTRIES = [
    ("US", "United States"),
    ("GB", "United Kingdom"),
    ("CA", "Canada"),
    ("CN", "China"),
    ("MX", "Mexico"),
    ("DE", "Germany"),
    ("FR", "France"),
    ("JP", "Japan"),
    ("IN", "India"),
    ("BR", "Brazil"),
    ("AU", "Australia"),
    ("KR", "Korea, Rep."),
    ("IT", "Italy"),
    ("ES", "Spain"),
    ("NL", "Netherlands"),
]

# 0. UI ########################################################################

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.tags.h4("Query parameters", class_="mb-3"),
        ui.input_select(
            "country",
            "Country",
            choices=dict(COUNTRIES),
            selected="US",
        ),
        ui.input_numeric("year_start", "Start year", value=2000, min=1960, max=2030),
        ui.input_numeric("year_end", "End year", value=2023, min=1960, max=2030),
        ui.input_action_button("run_query", "Run query", class_="btn-primary w-100 mt-3"),
        ui.tags.hr(),
        ui.tags.p(
            "Data: World Bank GDP per capita (current US$). "
            "No API key required.",
            class_="small text-muted",
        ),
        width=320,
    ),
    ui.div(
        ui.tags.style(
            """
            .app-title { font-weight: 600; color: #1a1a2e; margin-bottom: 0.25rem; }
            .app-desc { color: #4a4a6a; margin-bottom: 1.5rem; }
            .result-card { background: #f8f9fc; border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem; }
            .error-msg { background: #fff5f5; border-left: 4px solid #c53030; padding: 1rem; border-radius: 4px; }
            .loading-msg { color: #4a5568; padding: 1.5rem; text-align: center; }
            """
        ),
        ui.tags.div(
            ui.tags.h2("GDP per capita explorer", class_="app-title"),
            ui.tags.p(
                "Select a country and year range, then click Run query to fetch "
                "World Bank data. Results appear as a table and time series chart.",
                class_="app-desc",
            ),
            class_="mb-4",
        ),
        ui.output_ui("result_ui"),
        class_="p-4",
    ),
    title="World Bank GDP Explorer",
    fillable=True,
)

# 1. Server ####################################################################


def server(input: Inputs, output: Outputs, session: Session):
    # Reactive state: "idle" | "loading" | "success" | "error"
    status = reactive.value("idle")
    result_df = reactive.value(None)
    result_error = reactive.value(None)

    @reactive.effect
    @reactive.event(input.run_query)
    def run_query():
        country = input.country()
        year_start = input.year_start()
        year_end = input.year_end()

        status.set("loading")
        result_df.set(None)
        result_error.set(None)

        # Allow None from numeric inputs
        ys = year_start if year_start is not None else 2000
        ye = year_end if year_end is not None else 2023

        df, err = fetch_gdp_per_capita(country, ys, ye)
        if err:
            result_error.set(err)
            status.set("error")
        else:
            result_df.set(df)
            status.set("success")

    @render.ui
    def result_ui():
        s = status.get()
        if s == "idle":
            return ui.tags.p(
                "Click “Run query” to load data.",
                class_="text-muted",
            )
        if s == "loading":
            return ui.tags.div(
                ui.tags.div(
                    class_="spinner-border text-primary me-2",
                    role="status",
                    style="width: 1.5rem; height: 1.5rem; display: inline-block; vertical-align: middle;",
                ),
                ui.tags.span("Fetching data from World Bank API…"),
                class_="loading-msg",
            )
        if s == "error":
            return ui.tags.div(
                ui.tags.strong("Error"),
                ui.tags.p(result_error.get(), class_="mb-0 mt-1"),
                class_="error-msg",
            )
        # success
        df = result_df.get()
        if df is None or df.empty:
            return ui.tags.p("No data to display.", class_="text-muted")

        return ui.TagList(
            ui.tags.div(
                ui.tags.strong(f"Records: {len(df)}"),
                " — GDP per capita (current US$), most recent first.",
                class_="result-card",
            ),
            ui.tags.h5("Table", class_="mt-3 mb-2"),
            ui.output_data_frame("table"),
            ui.tags.h5("Time series", class_="mt-4 mb-2"),
            ui.output_plot("plot", height="320px"),
        )

    @render.data_frame
    def table():
        df = result_df.get()
        if df is None or df.empty:
            return None
        return render.DataTable(df, height="280px")

    @render.plot
    def plot():
        df = result_df.get()
        if df is None or df.empty:
            return None
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.fill_between(
            df["year"],
            df["gdp_per_capita_usd"],
            alpha=0.4,
            color="#3182ce",
        )
        ax.plot(df["year"], df["gdp_per_capita_usd"], color="#2c5282", linewidth=2)
        ax.set_xlabel("Year")
        ax.set_ylabel("GDP per capita (USD)")
        ax.set_title("GDP per capita over time")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig


app = App(app_ui, server)
