# ==========================================
# Growth Radar AI Settings
# ==========================================

APP_NAME = "Growth Radar AI"

VERSION = "2.0"

MAX_RESULTS = 25

REQUEST_TIMEOUT = 20

USER_AGENT = (
    "GrowthRadarAI/2.0"
)

# ==========================================
# Future APIs
# ==========================================
import os

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")

GOOGLE_CSE_API_KEY = ""

GOOGLE_SEARCH_ENGINE_ID = ""

OPENAI_API_KEY = ""

# ==========================================
# Finder
# ==========================================

DEFAULT_COUNTRY = ""

DEFAULT_LANGUAGE = "en"

# ==========================================
# Report
# ==========================================

PDF_AUTHOR = "Growth Radar AI"

PDF_COMPANY = "Growth Radar AI"

# ==========================================
# Debug
# ==========================================

DEBUG = True