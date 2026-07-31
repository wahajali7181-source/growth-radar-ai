import requests


HEADERS = {
    "User-Agent": "GrowthRadarAI"
}


def detect_technology(url):

    technologies = []

    try:

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=10

        )

        html = response.text.lower()

        headers = response.headers

        # ==========================
        # WordPress
        # ==========================

        if "wp-content" in html or "wp-includes" in html:

            technologies.append("WordPress")

        # ==========================
        # Shopify
        # ==========================

        if "cdn.shopify.com" in html:

            technologies.append("Shopify")

        # ==========================
        # React
        # ==========================

        if "__next" in html or "react" in html:

            technologies.append("React")

        # ==========================
        # Bootstrap
        # ==========================

        if "bootstrap" in html:

            technologies.append("Bootstrap")

        # ==========================
        # jQuery
        # ==========================

        if "jquery" in html:

            technologies.append("jQuery")

        # ==========================
        # Google Analytics
        # ==========================

        if "googletagmanager" in html or "google-analytics" in html:

            technologies.append("Google Analytics")

        # ==========================
        # Facebook Pixel
        # ==========================

        if "connect.facebook.net" in html:

            technologies.append("Facebook Pixel")

        # ==========================
        # Cloudflare
        # ==========================

        if headers.get("server", "").lower().startswith("cloudflare"):

            technologies.append("Cloudflare")

        # ==========================
        # Google Fonts
        # ==========================

        if "fonts.googleapis.com" in html:

            technologies.append("Google Fonts")

        # ==========================
        # Font Awesome
        # ==========================

        if "font-awesome" in html or "fontawesome" in html:

            technologies.append("Font Awesome")

    except Exception:

        pass

    return sorted(list(set(technologies)))