# Purpose: Call the OpenWeather "current weather" HTTP API, pretty-print the full JSON
# response, and use that inspection to decide which fields we want to keep later.

# We need to load the variables stored in the .env file into Python.
# The python-dotenv library provides the `load_dotenv()` function, which reads .env and
# makes its key/value pairs available as environment variables.
from dotenv import load_dotenv

# The built-in `os` module allows Python to access environment variables using os.getenv().
import os

# Since our script is calling an external API that calls the HTTP API (server) over the internet,” rather than “website.
import requests

# since we want to print what's in the API we import json
import json


# 1) Load secrets/config from .env so os.getenv() can access them.
load_dotenv()

# 2) Define the minimum inputs required by the API.
# These values come from the OpenWeather API documentation
# (e.g., 'q' for city, 'appid' for API key, optional 'units').
# Keeping them separate from the request logic(#4) makes the code easier to modify,
# reuse, and validate (for example, when accepting user input later).
weatherAPIKey = os.getenv("OPENWEATHER_API_KEY")
city = "Dallas,US"
units = "imperial"

# 3) You want it to fail fast if it does not read the API Key, therefore we create a guardrail right after variable setup and before HTTP request
# This prevents confusing HTTP 401 errors later and forces the developer to fix config first.
if not weatherAPIKey:
    raise SystemExit("Missing API KEY. Fix .env before running.")


# 4) Build the request using the exact parameter names from the API docs.
# Using a params dictionary lets 'requests' construct the query string safely,
# instead of manually concatenating URL strings.
baseURL = "https://api.openweathermap.org/data/2.5/weather"
parameters = {"q": city, "appid": weatherAPIKey, "units": units}

# 5) MAKE THE HTTP GET REQUEST
# -------------------------------------

# We’re about to “ask the server for data”.
# GET = retrieve data (no creation, no modification).
try:
    # Send the request. 'requests' builds the URL safely and encodes params.
    # timeout=10 → wait at most 10 seconds before aborting the connection.
    response = requests.get(baseURL, params=parameters, timeout=10)

    # If the server returns 4xx or 5xx, raise an HTTPError right now.
    # This converts failed responses into exceptions we can handle cleanly.
    response.raise_for_status()

# Handle specific API response errors (e.g., invalid key, bad city)
except requests.HTTPError as http_err:
    status = response.status_code if "resp" in locals() else "unknown"
    body = response.text[:300] if "resp" in locals() else ""
    raise SystemExit(f"HTTP error {status}:\n{body}") from http_err

# Handle general network issues (e.g., DNS, timeout, no internet)
except requests.RequestException as net_err:
    raise SystemExit(f"Network error: {net_err}") from net_err


# 6) Pretty-print the entire JSON so you can inspect every field and pick what you need.
data = response.json()
print("\n=== RAW OPENWEATHER RESPONSE ===")
print(json.dumps(data, indent=2))


# The OpenWeather API returns a JSON payload in the response body.
# I parse that JSON into a Python dictionary and then extract the fields I need.
# In file extractedAPIFields.py
