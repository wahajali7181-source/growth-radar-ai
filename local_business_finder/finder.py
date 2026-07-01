from config.settings import (
    MAX_RESULTS,
    REQUEST_TIMEOUT,
    USER_AGENT
)
import pandas as pd
import requests
from services.places_client import PlacesClient
from config.settings import GOOGLE_PLACES_API_KEY
client = PlacesClient(GOOGLE_PLACES_API_KEY)

def clean_business_name(name):

    if not name:
        return "Unknown"

    return name.split(",")[0].strip()


def find_businesses(business_type, city):

    query = f"{business_type} in {city}"

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": query,
        "format": "json",
        "limit": MAX_RESULTS
    }

    headers = {
        "User-Agent": USER_AGENT
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

    except Exception:

        return pd.DataFrame()

    businesses = []

    for item in data:

        businesses.append(
            {
                "name": clean_business_name(
                    item.get("display_name", "Unknown")
                ),

                "address": item.get(
                    "display_name",
                    ""
                ),

                "latitude": item.get("lat"),

                "longitude": item.get("lon"),

                "website": "",

                "phone": "",

                "email": "",

                "instagram": "",

                "facebook": "",

                "linkedin": "",

                "rating": None,

                "reviews": None
            }
        )

    return pd.DataFrame(businesses)
def use_google_places():

    return GOOGLE_PLACES_API_KEY.strip() != ""