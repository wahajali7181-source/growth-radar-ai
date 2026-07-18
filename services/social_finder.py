import re
import requests


def find_social_links(url):

    if not url:
        return {}

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        html = response.text

        socials = {

            "facebook": "",

            "instagram": "",

            "linkedin": "",

            "youtube": "",

            "twitter": ""

        }

        patterns = {

            "facebook": r"https?://(?:www\.)?facebook\.com/[A-Za-z0-9._/-]+",

            "instagram": r"https?://(?:www\.)?instagram\.com/[A-Za-z0-9._/-]+",

            "linkedin": r"https?://(?:www\.)?linkedin\.com/[A-Za-z0-9._/-]+",

            "youtube": r"https?://(?:www\.)?youtube\.com/[A-Za-z0-9._/?=-]+",

            "twitter": r"https?://(?:www\.)?(?:twitter|x)\.com/[A-Za-z0-9._/-]+"

        }

        for key, pattern in patterns.items():

            match = re.search(pattern, html)

            if match:
                socials[key] = match.group()

        return socials

    except Exception:

        return {}