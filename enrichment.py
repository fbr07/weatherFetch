# Now that we know that Integration test was successful. We want to enrich the data in the pipeline so it can be user friendly.
# This enrichment layer will take the extractedAPIFields and enrich the following fields sunset, sunrise, timestamp, timezone_effect
# Why did we not do this in the extractedAPIFields because the goal for that was not to enrich but to extract successfully the fields that we wanted
# Why did we not do the enrich before the main.py integration test? Because we wanted to know as soon as possible if the integration was going to fail so if we did the enrichment before it
# would of added another layer of complexitivity. But now that the integration test was successful we can now add the enrichment

# sunrise, sunset, timestamp, timezone_offset are all used in UNIX time but Python has a module(library) datetime and in that we are utilizing datetime, timezone, timedelta
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any

# so what are the arguments in the function?
# what are we going to grab that's in UNIX
# sunrise, sunset, timestamp, timezone_offset
# okay once we grab those inputs we are going to convert them, this will create new variables
# localSunrise, localSunset, localTimestamp, localTimezoneOffset

# okay when creating a function for this, what type of function do I create?
# well remember these inputs are put of weather {...} inside a dictionary
# so we can't create a function that has 4 inputs


def enrichWeather(weather):
    """
    Take the cleaned weather dictionary and add human-friendly
    versions of the timestamps (sunrise, sunset, timestamp).
    """

    # 1) Make a copy so we don't mutate the original dict
    enriched = dict(weather)

    # 2) Extract the raw UNIX values we need
    offset = weather.get("timezone_offset")
    sunrise = weather.get("sunrise")
    sunset = weather.get("sunset")
    timestamp = weather.get("timestamp")

    #Overwrite the raw Unix values with local strings
    #timezone offset if not a timestamp. Its number of seconds the local timezone is offset from UTC, that is why offset is in the enriched
    #UTC timestamp represents number of secs that have elapsed Unix
    
    enriched["sunrise"] = toLocalTime(sunrise, offset)
    enriched["sunset"] = toLocalTime(sunset, offset)
    enriched["timestamp"] = toLocalTime(timestamp, offset)

    # 4) Return enriched dictionary
    return enriched


def toLocalTime(timeStamp, offset):
    # the function above is grabbing the Unix and turning it into localtime
    # if there is no information for the input that we need to convert that we return None so
    # code doesn't crash
    if timeStamp is None or offset is None:
        return None

    timeZone = timezone(timedelta(seconds=offset))
    dateTime = datetime.fromtimestamp(timeStamp, timeZone)
    return dateTime.strftime("%Y-%m-%d %H:%M")
