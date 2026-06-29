import os


# =========================
# API KEYS
# =========================

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    ""
)

SERPER_API_KEY = os.getenv(
    "SERPER_API_KEY",
    ""
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)


# =========================
# APP SETTINGS
# =========================

APP_NAME = "Growth Radar AI"

VERSION = "1.0.0"

FREE_MODE = True