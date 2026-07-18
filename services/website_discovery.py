import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64)"
    )
}


def normalize(url):

    if not url:
        return ""

    if not url.startswith("http"):

        url = "https://" + url

    return url


def is_valid(url):

    try:

        response = requests.get(
            url,
            timeout=8,
            headers=HEADERS
        )

        return response.status_code < 400

    except:

        return False


def discover_website(name):

    """
    Finds the official website
    using DuckDuckGo Instant API.
    """

    try:

        url = (
            "https://api.duckduckgo.com/"
        )

        params = {

            "q": name + " official website",

            "format": "json"

        }

        response = requests.get(

            url,

            params=params,

            timeout=10,

            headers=HEADERS

        )

        data = response.json()

        website = ""

        if "AbstractURL" in data:

            website = data["AbstractURL"]

        website = normalize(website)

        if website and is_valid(website):

            return website

        return ""

    except:

        return ""


def discover_title(url):

    if not url:

        return ""

    try:

        html = requests.get(

            url,

            timeout=8,

            headers=HEADERS

        )

        soup = BeautifulSoup(

            html.text,

            "html.parser"

        )

        if soup.title:

            return soup.title.text.strip()

        return ""

    except:

        return ""


def discover_domain(url):

    if not url:

        return ""

    try:

        return urlparse(url).netloc

    except:

        return ""