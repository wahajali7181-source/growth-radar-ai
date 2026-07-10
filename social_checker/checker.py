import re
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


def check_socials(website):

    result = {
        "website": "❌ Not Found",
        "instagram": "❌ Not Found",
        "facebook": "❌ Not Found",
        "linkedin": "❌ Not Found",
        "youtube": "❌ Not Found",
        "tiktok": "❌ Not Found",
        "twitter": "❌ Not Found",
        "whatsapp": "❌ Not Found",
        "email": "❌ Not Found",
        "phone": "❌ Not Found",
        "google_maps": "❌ Not Found"
    }

    if not website:
        return result

    website = str(website).strip()

    if website.lower() == "no":
        return result

    if not website.startswith(("http://", "https://")):
        website = "https://"+website

    try:

        response = requests.get(
            website,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            return result

        result["website"] = "✅ Found"

        html = response.text

        soup = BeautifulSoup(html, "lxml")

        links = []

        for tag in soup.find_all("a", href=True):

            href = tag["href"].strip()

            if href.startswith("/"):

                href = urljoin(website, href)

            links.append(href)

        for link in links:

            low = link.lower()

            if "instagram.com" in low:
                result["instagram"] = link

            elif "facebook.com" in low:
                result["facebook"] = link

            elif "linkedin.com" in low:
                result["linkedin"] = link

            elif "youtube.com" in low or "youtu.be" in low:
                result["youtube"] = link

            elif "tiktok.com" in low:
                result["tiktok"] = link

            elif "twitter.com" in low or "x.com" in low:
                result["twitter"] = link

            elif "wa.me" in low or "whatsapp" in low:
                result["whatsapp"] = link

            elif "google.com/maps" in low:
                result["google_maps"] = link

        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            html
        )

        if emails:
            result["email"] = sorted(set(emails))[0]

        phones = re.findall(
            r"tel:([+\d\-\(\)\s]+)",
            html,
            re.IGNORECASE
        )

        if phones:
            result["phone"] = phones[0].strip()

    except Exception:
        pass

    return result