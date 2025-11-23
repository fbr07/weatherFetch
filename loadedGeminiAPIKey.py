from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()


genAIKey = os.getenv("GEMINI_API_KEY")
print("Loaded key prefix:", genAIKey[:10])  # TEMP DEBUG
client = client = genai.Client()
