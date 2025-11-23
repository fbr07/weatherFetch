from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from typing import Dict, Any

load_dotenv()

# 1) Load environment variables so we can access OPENAI_API_KEY
genAIKey = os.getenv("GEMINI_API_KEY")
if not genAIKey:
    raise SystemExit("Missing API KEY. Fix .env before running.")

print("DEBUG OPENAI KEY PREFIX:", repr(genAIKey[:20]))
print("DEBUG FULL KEY LENGTH:", len(genAIKey))
# Create a single global client (recommended)
client = genai.Client()

# function takes enriched weather dic extracts the fields, formats into plain text so LLM can read easily


# 2) Build function that will prepare text for LLM
def buildWeatherContext(weather):
    city = weather.get("city")
    country = weather.get("country")
    temp = weather.get("temp")
    feels_like = weather.get("feels_like")
    conditions = weather.get("conditionsDesc")
    humidity = weather.get("humidity")
    sunrise = weather.get("sunrise")
    sunset = weather.get("sunset")
    temp_max = weather.get("temp_max")
    temp_min = weather.get("temp_min")
    timestamp = weather.get("timestamp")
    units = weather.get("units")
    wind_speed = weather.get("wind_speed")
    wind_deg = weather.get("wind_deg")

    if units == "metric":
        temp_unit = "°C"
        wind_unit = "m/s"
    else:
        temp_unit = "°F"
        wind_unit = "mph"

    textLines = [
        f"Location: {city}, {country}",
        f"Observation time (local): {timestamp}",
        f"Temperature: {temp}{temp_unit}, feels like: {feels_like}{temp_unit}",
        f"Conditions: {conditions}",
        f"Humidity: {humidity}%",
        f"Wind: {wind_speed} {wind_unit} at {wind_deg} degrees",
        f"Sunrise (local): {sunrise}",
        f"Sunset (local): {sunset}",
    ]

    cleaned_lines = [line for line in textLines if "None" not in line]
    return "\n".join(cleaned_lines)


def answerQuestionAboutWeather(weather, question):
    """
    Use the enriched weather data + an LLM to answer a user's question.
    - weather: enriched dict from enrichWeather(...)
    - question: user's natural-language question about the weather
    """

    weatherContext = buildWeatherContext(weather)

    system_prompt = (
        "You are a helpful assistant that answers questions about the current weather "
        "and gives any practical recommendations and activity suggestions. "
        "Use ONLY the weather data provided below. "
        "Be specific and concise, and explain your reasoning based on temperature, conditions, "
        "wind, humidity, and daylight (sunrise/sunset)."
    )

    user_prompt = (
        f"Here is the current weather data:\n\n"
        f"{weatherContext}\n\n"
        f"User question: {question}"
    )

    # Calling GENAI
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=[system_prompt, user_prompt]
        )
    except Exception as e:
        # You can log this instead, but returning a string is fine for now
        return f"Error calling GoogleAI API: {e}"

    # Extract the assistant's answer text
    answer = response.text
    return answer
