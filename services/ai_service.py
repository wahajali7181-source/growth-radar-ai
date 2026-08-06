import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


DEFAULT_MODEL = "deepseek/deepseek-chat-v3-0324"


def ask_ai(
    prompt,
    system_prompt="You are an expert business consultant.",
    model=DEFAULT_MODEL,
    temperature=0.7,
    max_tokens=1500,
):

    if not API_KEY:
        return "❌ OPENROUTER_API_KEY not found in .env"

    try:

        response = client.chat.completions.create(

            model=model,

            temperature=temperature,

            max_tokens=max_tokens,

            messages=[

                {
                    "role": "system",
                    "content": system_prompt,
                },

                {
                    "role": "user",
                    "content": prompt,
                },

            ],

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"AI Error: {e}"