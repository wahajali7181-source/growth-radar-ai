import pandas as pd
import requests

from config.settings import (
    MAX_RESULTS,
    REQUEST_TIMEOUT,
    USER_AGENT,
    GOOGLE_PLACES_API_KEY,
)

from services.places_client import PlacesClient


# =====================================================
# Google Places
# =====================================================

client = PlacesClient(GOOGLE_PLACES_API_KEY)


def use_google_places():
    """
    Returns True if Google Places API key exists.
    """
    return bool(GOOGLE_PLACES_API_KEY.strip())


# =====================================================
# Helpers
# =====================================================

def clean_business_name(name):

    if not name:
        return "Unknown"

    return name.split(",")[0].strip()


# =====================================================
# Main Finder
# =====================================================

def find_businesses(business_type, city):

    # ---------------------------------------
    # Google Places
    # ---------------------------------------

    if use_google_places():

        try:

            query = f"{business_type} in {city}"

            data = client.text_search(query)

            businesses = []

            for place in data.get("results", []):

                # -----------------------------------
                # Get Detailed Information
                # -----------------------------------

                details = {}

                try:

                    details = client.get_place_details(
                        place.get("place_id")
                    ).get("result", {})

                except Exception:
                    pass

                businesses.append(
                    {
                        "name": place.get("name", "Unknown"),

                        "place_id": place.get(
                            "place_id",
                            ""
                        ),

                        "address": place.get(
                            "formatted_address",
                            ""
                        ),

                        "latitude": place.get(
                            "geometry",
                            {}
                        ).get(
                            "location",
                            {}
                        ).get("lat"),

                        "longitude": place.get(
                            "geometry",
                            {}
                        ).get(
                            "location",
                            {}
                        ).get("lng"),

                        "website": details.get(
                            "website",
                            ""
                        ),

                        "phone": details.get(
                            "formatted_phone_number",
                            ""
                        ),

                        "email": "",

                        "instagram": "",

                        "facebook": "",

                        "linkedin": "",

                        "rating": place.get(
                            "rating"
                        ),

                        "reviews": place.get(
                            "user_ratings_total"
                        ),

                        "business_status": details.get(
                            "business_status",
                            ""
                        ),

                        "maps_url": details.get(
                            "url",
                            ""
                        ),

                        "opening_hours": (
                            details.get(
                                "opening_hours",
                                {}
                            ).get(
                                "weekday_text",
                                []
                            )
                        ),
                    }
                )

            return pd.DataFrame(businesses)

        except Exception as e:

            print(e)

    # ---------------------------------------
    # OpenStreetMap Backup
    # ---------------------------------------

    query = f"{business_type} in {city}"

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": query,
        "format": "json",
        "limit": MAX_RESULTS,
    }

    headers = {
        "User-Agent": USER_AGENT,
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
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
                    item.get(
                        "display_name",
                        ""
                    )
                ),

                "address": item.get(
                    "display_name",
                    ""
                ),

                "latitude": item.get(
                    "lat"
                ),

                "longitude": item.get(
                    "lon"
                ),

                "website": "",

                "phone": "",

                "email": "",

                "instagram": "",

                "facebook": "",

                "linkedin": "",

                "rating": None,

                "reviews": None,

                "business_status": "",

                "maps_url": "",

                "opening_hours": [],
            }
        )

    return pd.DataFrame(businesses)