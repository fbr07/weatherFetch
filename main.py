# Purpose of main.py
# So now that we've validated our envValidation.py, and inspectedAPIFields, then extracted what we want from the JSON API
# We can now create a script(main.py) that ties all of it
# main.py fetches the data from the API, parse the json into a Python project, extract meaningful subset, print or use that clean data in the app


from dotenv import load_dotenv
import os
import requests
from pprint import pprint
from enrichment import enrichWeather
from llmAgent import answerQuestionAboutWeather
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class WeatherRequest(BaseModel):
    city: str
    units: str
    question: str


# getCurrentWeather is going to fetch the data, parse and extract
def getCurrentWeather(
    city: str,
    units: str = "imperial",
) -> dict:
    # Call OpenWeather, parse JSON, returned cleaned dict

    weatherAPIKey = os.getenv("OPENWEATHER_API_KEY")

    # after loading the API Key we want a guardrail as soon as possible so if the API key is not read from .env it will throw an error immediately
    if not weatherAPIKey:
        raise SystemExit("Missing API KEY. Fix .env before running.")

    # If API is able to load, we then build the request using the exact parameter names from the API docs.
    # Using a params dictionary lets 'requests' construct the query string safely,
    # instead of manually concatenating URL strings.
    url = "https://api.openweathermap.org/data/2.5/weather"
    parameters = {"q": city, "appid": weatherAPIKey, "units": units}

    # We’re about to “fetch(GET) the data”.
    # GET = retrieve data (no creation, no modification).
    try:
        # Send the request. 'requests' builds the URL safely and encodes params.
        # timeout=10 → wait at most 10 seconds before aborting the connection.
        response = requests.get(url, params=parameters, timeout=10)  # fetches the data

        # If the server returns 4xx or 5xx, raise an HTTPError right now.
        # This converts failed responses into exceptions we can handle cleanly.
        response.raise_for_status()

        # Handle specific API response errors (e.g., invalid key, bad city)
    except requests.HTTPError as http_err:
        status = response.status_code if "response" in locals() else "unknown"
        body = response.text[:300] if "response" in locals() else ""
        raise SystemExit(f"HTTP error {status}:\n{body}") from http_err

        # Handle general network issues (e.g., DNS, timeout, no internet)
    except requests.RequestException as net_err:
        raise SystemExit(f"Network error: {net_err}") from net_err

    # Now we parse + extract
    raw = response.json()  # where the parse happens
    from extractedAPIFields import extractWeatherFields

    # Extract
    return extractWeatherFields(
        raw, units
    )  # where extracts occurs inside getCurrentWeather()


# Creating a new reusable function both terminal and FASTAPI wall call
def run_weather_qa(city, units, question):
    weatherData = getCurrentWeather(city, units)

    weatherData = enrichWeather(weatherData)

    answer = answerQuestionAboutWeather(weatherData, question)

    return {"weather": weatherData, "answer": answer}


@app.post("/ask")
def ask_weather(request: WeatherRequest):
    result = run_weather_qa(
        city=request.city,
        units=request.units,
        question=request.question,
    )
    return 

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    


# Create Integration Test (run everything together), you want to confirm that your fetch works before adding complexity"
# The question this steps answers is, "Does my full weather pipeline work?" Does it return the correct structure for my app


if __name__ == "__main__":
    city = input("What city: ").strip() or "Dallas,US"
    units = input("Units [imperial/metric] (default imperial): ").strip() or "imperial"

    print("\n=== ENRICHED WEATHER DATA ===")

    userQuestion = input("\nAsk a question about the weather: ")

    result = run_weather_qa(city, units, userQuestion)

    pprint(result["weather"])

    print("\n=== LLM ANSWER ===")
    print(result["answer"])
