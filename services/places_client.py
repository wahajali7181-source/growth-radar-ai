import requests
from config.settings import REQUEST_TIMEOUT


class PlacesClient:

    def __init__(self, api_key):
        self.api_key = api_key

    # ==========================================
    # Google Places Text Search
    # ==========================================

    def text_search(self, query):

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

        params = {
            "query": query,
            "key": self.api_key
        }

        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    # ==========================================
    # Google Place Details
    # ==========================================

    def get_place_details(self, place_id):

        url = "https://maps.googleapis.com/maps/api/place/details/json"

        params = {
            "place_id": place_id,
            "fields": (
                "name,"
                "website,"
                "formatted_phone_number,"
                "rating,"
                "user_ratings_total,"
                "business_status,"
                "opening_hours,"
                "url"
            ),
            "key": self.api_key
        }

        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        print("=" * 80)
        print(data)
        print("=" * 80)

        return data