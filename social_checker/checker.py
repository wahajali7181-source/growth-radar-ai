import re
import requests


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
        website = "https://" + website

    try:

        response = requests.get(
            website,
            headers=HEADERS,
            timeout=10
        )

        html = response.text.lower()

        result["website"] = "✅ Found"

        if "instagram.com" in html:
            result["instagram"] = "✅ Found"

        if "facebook.com" in html:
            result["facebook"] = "✅ Found"

        if "linkedin.com" in html:
            result["linkedin"] = "✅ Found"

        if "youtube.com" in html or "youtu.be" in html:
            result["youtube"] = "✅ Found"

        if "tiktok.com" in html:
            result["tiktok"] = "✅ Found"

        if "twitter.com" in html or "x.com" in html:
            result["twitter"] = "✅ Found"

        if "wa.me" in html or "whatsapp" in html:
            result["whatsapp"] = "✅ Found"

        if "google.com/maps" in html:
            result["google_maps"] = "✅ Found"

        email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        if re.search(email_pattern, html):
            result["email"] = "✅ Found"

        phone_pattern = r"tel:"

        if phone_pattern in html:
            result["phone"] = "✅ Found"

    except Exception:
        pass

    return result