import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 GrowthRadarAI Technology Scanner"
}


def detect_technology(url):

    technologies = set()

    try:

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=15,

            allow_redirects=True,

        )

        html = response.text.lower()

        headers = response.headers

        server = headers.get("Server", "").lower()

        powered = headers.get("X-Powered-By", "").lower()

        # ==========================
        # CMS
        # ==========================

        if "wp-content" in html or "wp-includes" in html:
            technologies.add("WordPress")

        if "cdn.shopify.com" in html or "shopify" in powered:
            technologies.add("Shopify")

        if "wixstatic" in html:
            technologies.add("Wix")

        if "squarespace" in html:
            technologies.add("Squarespace")

        if "webflow" in html:
            technologies.add("Webflow")

        # ==========================
        # Frameworks
        # ==========================

        if "__next" in html:
            technologies.add("Next.js")

        if "_nuxt" in html:
            technologies.add("Nuxt.js")

        if "react" in html:
            technologies.add("React")

        if "vue" in html:
            technologies.add("Vue.js")

        if "angular" in html:
            technologies.add("Angular")

        # ==========================
        # CSS
        # ==========================

        if "bootstrap" in html:
            technologies.add("Bootstrap")

        if "tailwind" in html:
            technologies.add("Tailwind CSS")

        if "bulma" in html:
            technologies.add("Bulma")

        # ==========================
        # JavaScript
        # ==========================

        if "jquery" in html:
            technologies.add("jQuery")

        # ==========================
        # Analytics
        # ==========================

        if "googletagmanager" in html:
            technologies.add("Google Tag Manager")

        if "google-analytics" in html or "gtag(" in html:
            technologies.add("Google Analytics")

        if "connect.facebook.net" in html:
            technologies.add("Facebook Pixel")

        if "hotjar" in html:
            technologies.add("Hotjar")

        if "clarity.ms" in html:
            technologies.add("Microsoft Clarity")

        # ==========================
        # CDN
        # ==========================

        if "cloudflare" in server:
            technologies.add("Cloudflare")

        if "cloudfront" in server:
            technologies.add("CloudFront")

        # ==========================
        # Fonts
        # ==========================

        if "fonts.googleapis.com" in html:
            technologies.add("Google Fonts")

        if "font-awesome" in html or "fontawesome" in html:
            technologies.add("Font Awesome")

        # ==========================
        # Backend
        # ==========================

        if "php" in powered:
            technologies.add("PHP")

        if "asp.net" in powered:
            technologies.add("ASP.NET")

        if "express" in powered:
            technologies.add("Express.js")

        if "laravel" in html:
            technologies.add("Laravel")

    except Exception:
        return []

    return sorted(technologies)