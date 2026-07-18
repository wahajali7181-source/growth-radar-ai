import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MODELS = [
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-2.0-flash",
]


def ask_gemini(prompt):

    last_error = ""

    for model in MODELS:

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text

        except Exception as e:

            last_error = str(e)

            print(f"{model} failed")

            time.sleep(1)

    return f"Gemini unavailable.\n\n{last_error}"