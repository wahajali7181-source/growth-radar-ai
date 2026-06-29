import requests
from urllib.parse import quote


def find_website(business_name, city):

    """
    Returns website URL if found.
    Otherwise returns empty string.
    """

    query = quote(f"{business_name} {city}")

    url = (
        f"https://duckduckgo.com/html/?q={query}"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0"
        )
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        html = response.text.lower()

    except Exception:

        return ""

    keywords = [
        ".com",
        ".net",
        ".org",
        ".co",
        ".io",
        ".ai"
    ]

    for word in html.split('"'):

        if word.startswith("http"):

            if any(
                k in word
                for k in keywords
            ):

                if "duckduckgo" not in word:

                    return word

    return ""