import re
import requests


EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"


def find_emails(url):

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

        matches = re.findall(
            EMAIL_PATTERN,
            response.text
        )

        emails = sorted(list(set(matches)))

        return emails

    except Exception:

        return []