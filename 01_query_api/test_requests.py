# test_requests.py
# POST request with JSON using the requests library
# Pairs with ACTIVITY_add_documentation_to_cursor (Docs: requests)
# Tim Fraser

# Demonstrates how to send JSON in a POST request.
# The json= parameter serializes the dict and sets Content-Type: application/json.

# 0. Setup #################################

## 0.1 Load Packages ############################

import requests  # for HTTP requests

# 1. Make POST request with JSON ####################################

url = "https://httpbin.org/post"
data = {"name": "test"}

# requests.post() with json= encodes the dict as JSON and sets the right header
response = requests.post(url, json=data)

# 2. Inspect response ####################################

print(response.status_code)
print(response.json())
