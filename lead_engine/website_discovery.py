from urllib.parse import urlparse

from services.places_client import PlacesClient
from config.settings import GOOGLE_PLACES_API_KEY


class WebsiteDiscovery:

    def __init__(self):

        self.client = PlacesClient(
            GOOGLE_PLACES_API_KEY
        )

    # ===================================================
    # Clean URL
    # ===================================================

    def clean_url(self, url):

        if not url:
            return ""

        if not url.startswith("http"):
            url = "https://" + url

        return url.rstrip("/")

    # ===================================================
    # Validate Domain
    # ===================================================

    def valid_domain(self, url):

        if not url:
            return False

        try:

            domain = urlparse(url).netloc

            if "." not in domain:
                return False

            return True

        except Exception:

            return False

    # ===================================================
    # Discover Website
    # ===================================================

    def discover(self, business_name, city):

        query = f"{business_name} {city}"

        try:

            search_data = self.client.text_search(query)

        except Exception as e:

            print("Search Error:", e)

            return ""

        results = search_data.get("results", [])

        if len(results) == 0:

            print("No Google Places results found.")

            return ""

        place_id = results[0].get("place_id")

        if not place_id:

            print("Place ID not found.")

            return ""

        try:

            details = self.client.get_place_details(place_id)

        except Exception as e:

            print("Details Error:", e)

            return ""

        result = details.get("result", {})

        print("=" * 80)
        print("PLACE DETAILS")
        print(result)
        print("=" * 80)

        website = result.get("website", "")

        website = self.clean_url(website)

        if self.valid_domain(website):

            return website

        return ""


website_discovery = WebsiteDiscovery()