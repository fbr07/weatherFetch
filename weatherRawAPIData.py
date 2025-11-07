# We are creating this file so we can figure out what information the API has and we can select what I need

# We need to load the variables stored in the .env file into Python.
# The python-dotenv library provides the `load_dotenv()` function, which reads .env and
# makes its key/value pairs available as environment variables.
from dotenv import load_dotenv

# The built-in `os` module allows Python to access environment variables using os.getenv().
import os

# Since our script is calling an external API that interacts with website we import requests. It requests information from the external API website
import requests

# since we want to print what's in the API we import json
import json


# This loads .env in this directory
# After this runs, any variable in .env becomes accessible via os.getenv().
load_dotenv()

# Now that we have everything above to grab from the data on .env we can load the fields of the API
#  In order to load the fields of the API, I first have to create a variable that grabs the weatherAPI and then create another variable to grab the city and that
# should be enough information so it can pull all of the data.
weatherAPIKey = os.getenv("OPENWEATHER_API_KEY")
city = "Dallas,US"
