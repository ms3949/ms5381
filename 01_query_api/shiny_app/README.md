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

---

## Deploy to DigitalOcean App Platform

The app is ready to deploy using the included **Dockerfile**. Follow these steps so the Shiny app is good to go on DigitalOcean.

### 1. Prerequisites

- [DigitalOcean account](https://www.digitalocean.com/) (e.g. Basic plan ~$5/month).
- This repo on **GitHub** (public or private) with **DigitalOcean authorized** to access it (see [04_deployment/digitalocean/README.md](../../04_deployment/digitalocean/README.md)).

### 2. Create the app on App Platform

1. In DigitalOcean: **Create** → **Apps** → **Create App**.
2. Choose **GitHub** and select this repository and branch (e.g. `main`).
3. **Important:** Set **Source Directory** to:
   ```text
   01_query_api/shiny_app
   ```
   so the build uses the `Dockerfile` and app code in this folder.
4. Set **Build** to **Dockerfile** (leave Dockerfile path as `Dockerfile`).
5. Leave **Run command** blank (the Dockerfile `CMD` starts the app).
6. Pick a plan (e.g. Basic $5/month) and **Create Resources**.

### 3. After deploy

- Open the app URL from the App Platform dashboard (e.g. `https://your-app-name.ondigitalocean.app`).
- The app listens on port **8080** inside the container; App Platform maps this for you.

### 4. Optional: run with Docker locally

To confirm the image runs like production:

```bash
cd 01_query_api/shiny_app
docker build -t shiny-gdp-explorer .
docker run -p 8080:8080 shiny-gdp-explorer
```

Then open http://localhost:8080.

### Troubleshooting

- **Build fails:** Ensure **Source Directory** is exactly `01_query_api/shiny_app` and that `requirements.txt`, `app.py`, and `worldbank_api.py` are in that directory.
- **App not loading:** Check **Runtime Logs** in the App Platform dashboard; the app must bind to `0.0.0.0:8080` (already set in the Dockerfile).
- More deployment details: [04_deployment/digitalocean/README.md](../../04_deployment/digitalocean/README.md) and [ACTIVITY_digitalocean_create_app_platform.md](../../04_deployment/digitalocean/ACTIVITY_digitalocean_create_app_platform.md).
