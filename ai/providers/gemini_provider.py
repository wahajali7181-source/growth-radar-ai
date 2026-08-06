from google import genai
from google.genai import types

from config.settings import GOOGLE_API_KEY


_client = None


def get_client():
    global _client

    if _client is None:

        if not GOOGLE_API_KEY.strip():
            raise Exception("GOOGLE_API_KEY is missing in .env")

        _client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

    return _client


def ask_gemini(
    prompt,
    system_prompt=""
):

    try:

        client = get_client()

        full_prompt = f"""
{system_prompt}

User Request:

{prompt}
"""

        models_to_try = [
            "gemini-2.5-flash-lite",
            "gemini-2.5-pro",
            "gemini-2.0-flash"
        ]

        last_error = None

        for model_name in models_to_try:

            try:

                response = client.models.generate_content(

                    model=model_name,

                    contents=full_prompt,

                    config=types.GenerateContentConfig(

                        temperature=0.7,

                        max_output_tokens=4096

                    )

                )

                if hasattr(response, "text") and response.text:
                    return response.text

            except Exception as e:
                last_error = e
                continue

        return f"❌ Gemini Error:\n\n{str(last_error)}"

    except Exception as e:

        return f"❌ Gemini Error:\n\n{str(e)}"