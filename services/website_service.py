import requests
from urllib.parse import quote


def find_website(business_name, city=""):

    """
    Returns:

    {
        "website": "",
        "source": "",
        "confidence": 0
    }

    Future:
    - Google Places
    - Serper
    - Brave Search
    """

    return {
        "website": "",
        "source": "none",
        "confidence": 0
    }