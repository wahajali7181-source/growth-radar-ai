import os

from config.loader import *

# ==========================
# APP
# ==========================

APP_NAME = os.getenv("APP_NAME", "Growth Radar AI")
APP_VERSION = os.getenv("APP_VERSION", "1.0")
DEBUG = os.getenv("DEBUG", "False")

# ==========================
# AI
# ==========================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

# ==========================
# PAYMENTS
# ==========================

LEMON_SQUEEZY_API = os.getenv("LEMON_SQUEEZY_API", "")
LEMON_STORE_ID = os.getenv("LEMON_STORE_ID", "")
LEMON_WEBHOOK_SECRET = os.getenv("LEMON_WEBHOOK_SECRET", "")

# ==========================
# GOOGLE PLACES
# ==========================

GOOGLE_PLACES_API_KEY = os.getenv(
    "GOOGLE_PLACES_API_KEY",
    GOOGLE_API_KEY
)

MAX_RESULTS = int(
    os.getenv(
        "MAX_RESULTS",
        "20"
    )
)

REQUEST_TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT",
        "20"
    )
)

USER_AGENT = os.getenv(
    "USER_AGENT",
    "GrowthRadarAI/1.0"
)