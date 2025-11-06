# The purpose of the .envValidation file is to confirm project is correctly reading secret values from .env before you start writing real API code
# The goal is Can Python successfully load my .env file and read my API keys? Before writing code that USES the API keys, we must confirm we can ACCESS the API keys
# This step is the foundation check before building the app. Can my Python app successfully load API keys from .env

# We need to load the variables stored in the .env file into Python.
# The python-dotenv library provides the `load_dotenv()` function, which reads .env and
# makes its key/value pairs available as environment variables.
from dotenv import load_dotenv

# The built-in `os` module allows Python to access environment variables using os.getenv().
import os


# This loads .env in this directory
# After this runs, any variable in .env becomes accessible via os.getenv().
load_dotenv()


# Now we can test whether the variables were successfully loaded.
# os.getenv("VAR_NAME") returns the value if it exists, otherwise it returns None.
print(f"Weather API Key {os.getenv("OPENWEATHER_API_KEY")}")
print(f"Weather API Key {os.getenv("OPENAI_API_KEY")}")
