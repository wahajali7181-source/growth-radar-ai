import pandas as pd
import requests
import random


def find_businesses(business_type, city):

    query = f"{business_type} in {city}"

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": query,
        "format": "json",
        "limit": 10
    }

    headers = {
        "User-Agent": "GrowthRadarAI"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=20
    )

    data = response.json()

    businesses = []

    for item in data:

        businesses.append(
            {
                "name": item.get("display_name", "Unknown"),
                "latitude": item.get("lat"),
                "longitude": item.get("lon"),
                "rating": round(random.uniform(3.0, 5.0), 1),
                "reviews": random.randint(5, 500),
                "website": random.choice(["Yes", "No"])
            }
        )

    return pd.DataFrame(businesses)