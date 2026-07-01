import requests
from config.settings import REQUEST_TIMEOUT

class PlacesClient:

    def __init__(self, api_key):

       from config.settings import GOOGLE_PLACES_API_KEY
       self.api_key = api_key or GOOGLE_PLACES_API_KEY

    def text_search(self, query):

        url = (
            "https://maps.googleapis.com/maps/api/place/textsearch/json"
        )

        params = {
            "query": query,
            "key": self.api_key
        }

        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        return response.json()