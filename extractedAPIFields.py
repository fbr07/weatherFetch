# This file extracts relevant fields from OpenWeatherFetch API’s JSON response.
# We need to create a function that takes the fields that we want to extract from JSON (API response fields) from OpenWeather
# and stores them into a new simpler dictionary

# remember what variable gave us the APIs JSON response???
# it was step # 6) Pretty-print the entire JSON so you can inspect every field and pick what you need.
#       data = response.json()

# we defined units in inspectRawAPIData.py that way all info is in same units and universal

# what do we want this function to return a dictionary with the inputs that we are extracting so therefore -> dict


def extractWeatherFields(data: dict, units: str) -> dict:
      """
      Extracts key fields from the OpenWeather /weather API response.
      Returns a simplified dictionary that our app or LLM can use.
      """
      """
      remember what variable gave us the APIs JSON response???
      it was step # 6) Pretty-print the entire JSON so you can inspect every field and pick what you need.
            data = response.json()
            we defined units in inspectRawAPIData.py that way all info is in same units and universal

      what do we want this function to return a dictionary with the inputs that we are extracting so therefore -> dict
      """
      weather = data.get("weather", {})
      coord = data.get("coord", {})
      main = data.get("main", {})
      wind = data.get("main", {})
      sys = data.get("sys", {})
      clouds = data.get("clouds", {})

      # When the JSON API printed the weather had a nested dictionary unlike the other one so therefore
      # Safely extract condition details from the "weather" list
      if weather:
            # If the weather list has at least one item, access its first element
            conditionsMain = weather[0].get("main")
            conditionsDesc = weather[0].get("description")
      else:
            # If it's empty or missing, assign None to avoid IndexError
            conditionsMain = None
            conditionsDesc = None

      return {
            "city": data.get("name"),
            "country": sys.get("country"),
            "latitude": coord.get("lat"),
            "longitude": coord.get("lon"),
            "timestamp": data.get("dt"),
            "timezone_offset": data.get("timezone"),
            "temp": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "temp_min": main.get("temp_min"),
            "temp_max": main.get("temp_max"),
            "humidity": main.get("humidity"),
            "pressure": main.get("pressure"),
            "wind_speed": wind.get("speed"),
            "wind_gust": wind.get("gust"),
            "wind_deg": wind.get("deg"),
            "conditionsMain": conditionsMain,
            "conditionsDesc": conditionsDesc,
            "cloud_cover_pct": clouds.get("all"),
            "visibility_m": data.get("visibility"),
            "sunrise": sys.get("sunrise"),
            "sunset": sys.get("sunset"),
            "units": units,
      }
