import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


def scan_website(website):

    result = {
        "status": "Offline",
        "status_code": "N/A",
        "ssl": "❌ No",
        "load_time": "N/A",
        "title": "Not Found",
        "meta_description": "Not Found",
        "favicon": "❌ Not Found",
    }

    if not website:
        return result

    website = website.strip()

    if website.lower() == "no":
        return result

    if not website.startswith(("http://", "https://")):
        website = "https://" + website

    try:

        start = time.perf_counter()

        response = requests.get(
            website,
            headers=HEADERS,
            timeout=10
        )

        end = time.perf_counter()

        load_time = round(end - start, 2)

        result["load_time"] = f"{load_time} sec"

        result["status_code"] = response.status_code

        if response.status_code == 200:
            result["status"] = "🟢 Online"
        else:
            result["status"] = "🟠 Reachable"

        if website.startswith("https://"):
            result["ssl"] = "✅ Enabled"

        soup = BeautifulSoup(response.text, "lxml")

        if soup.title and soup.title.string:
            result["title"] = soup.title.string.strip()

        meta = soup.find("meta", attrs={"name": "description"})

        if meta and meta.get("content"):
            result["meta_description"] = meta["content"].strip()

        icon = (
            soup.find("link", rel=lambda x: x and "icon" in x.lower())
        )

        if icon and icon.get("href"):

            favicon = urljoin(
                website,
                icon["href"]
            )

            result["favicon"] = favicon

    except Exception:
        pass

    return result