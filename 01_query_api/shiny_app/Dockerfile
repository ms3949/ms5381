# Shiny for Python: World Bank GDP Explorer
# For deployment to DigitalOcean App Platform (or any Docker host)

FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code (worldbank_api.py and app.py)
COPY worldbank_api.py .
COPY app.py .

# App Platform expects HTTP on 8080 by default
EXPOSE 8080

# Bind to 0.0.0.0 so the app is reachable from outside the container
CMD ["shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "8080"]
