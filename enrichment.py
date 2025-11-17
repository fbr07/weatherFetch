# Now that we know that Integration test was successful. We want to enrich the data in the pipeline so it can be user friendly. 
# This enrichment layer will take the extractedAPIFields and enrich the following fields sunset, sunrise, timestamp, timezone_effect
# Why did we not do this in the extractedAPIFields because the goal for that was not to enrich but to extract successfully the fields that we wanted
# Why did we not do the enrich before the main.py integration test? Because we wanted to know as soon as possible if the integration was going to fail so if we did the enrichment before it
    # would of added another layer of complexitivity. But now that the integration test was successful we can now add the enrichment

# sunrise, sunset, timestamp, timezone_offset are all used in UNIX time but Python has a module(library) datetime and in that we are utilizing datetime, timezone, timedelta
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any

#so what are the arguments in the function? 
def toLocalTime(timestamp[int], timezone_offset[int]) -> Optional([str]):
    if timestamp is None or time