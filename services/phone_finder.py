import re
import requests


PHONE_PATTERN = r"(\+?\d[\d\s\-\(\)]{7,}\d)"


def find_phones(url):

    if not url:
        return []

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        phones = re.findall(
            PHONE_PATTERN,
            response.text
        )

        phones = sorted(list(set(phones)))

        return phones

    except Exception:

        return []