import requests


TECH_SIGNATURES = {

    "WordPress": [
        "wp-content",
        "wp-includes",
        "wordpress"
    ],

    "Shopify": [
        "cdn.shopify.com",
        "shopify.theme",
        "shopify"
    ],

    "Wix": [
        "wix.com",
        "static.wixstatic.com"
    ],

    "Squarespace": [
        "static.squarespace.com",
        "squarespace"
    ],

    "Webflow": [
        "webflow"
    ],

    "React": [
        "__NEXT_DATA__",
        "react"
    ],

    "Next.js": [
        "__NEXT_DATA__"
    ],

    "Laravel": [
        "laravel"
    ],

    "WooCommerce": [
        "woocommerce"
    ]
}


def detect_technology(url):

    if not url:

        return {
            "technology": "Unknown"
        }

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        html = response.text.lower()

        detected = []

        for tech, signatures in TECH_SIGNATURES.items():

            for item in signatures:

                if item.lower() in html:

                    detected.append(tech)

                    break

        if not detected:

            detected.append("Custom Website")

        return {

            "technology": ", ".join(detected)

        }

    except Exception:

        return {

            "technology": "Unknown"

        }