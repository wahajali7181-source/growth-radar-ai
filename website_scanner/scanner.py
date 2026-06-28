import requests


def get_website_html(url):

    try:

        headers = {
            "User-Agent": "Growth Radar AI"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            return response.text

        return None

    except Exception:
        return None