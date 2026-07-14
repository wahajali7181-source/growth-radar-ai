import os
from dotenv import load_dotenv
import streamlit as st
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

st.write("KEY FOUND:", API_KEY is not None)
st.write("KEY LENGTH:", len(API_KEY) if API_KEY else 0)

client = genai.Client(api_key=API_KEY)

def ask_gemini(prompt):

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return str(e)