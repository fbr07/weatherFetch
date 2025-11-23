from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import Dict, Any

load_dotenv()

# 1) Load environment variables so we can access OPENAI_API_KEY
openAIKey = os.getenv("OPENAI_API_KEY")
if not openAIKey:
    raise SystemExit("Missing API KEY. Fix .env before running.")

# Create a single global client (recommended)
client = OpenAI(api_key=openAIKey)

# function takes enriched weather dic extracts the fields, formats into plain text so LLM can read easily


# 2) Build function that will prepare text for LLM
def buildWeatherContext(weather):
    city = weather.get("city")
    country = weather.get("county")
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

    # Calling OPENAI
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # or gpt-4o-mini / gpt-4.1, etc.
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,  # slightly conservative for factual weather
        )
    except Exception as e:
        # You can log this instead, but returning a string is fine for now
        return f"Error calling OpenAI API: {e}"

    # Extract the assistant's answer text
    answer = response.choices[0].message.content
    return answer
