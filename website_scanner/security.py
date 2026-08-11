import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 GrowthRadarAI Security Scanner"
}


def analyze_security(url):

    score = 100

    recommendations = []

    try:

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=15,

            allow_redirects=True,

        )

        headers = response.headers

        final_url = response.url

        # -------------------------
        # HTTPS
        # -------------------------

        if not final_url.startswith("https://"):

            score -= 30

            recommendations.append(
                "Website is not using HTTPS."
            )

        # -------------------------
        # HSTS
        # -------------------------

        if "Strict-Transport-Security" not in headers:

            score -= 10

            recommendations.append(
                "HSTS security header is missing."
            )

        # -------------------------
        # CSP
        # -------------------------

        if "Content-Security-Policy" not in headers:

            score -= 15

            recommendations.append(
                "Content Security Policy header is missing."
            )

        # -------------------------
        # X Frame
        # -------------------------

        if "X-Frame-Options" not in headers:

            score -= 10

            recommendations.append(
                "X-Frame-Options header is missing."
            )

        # -------------------------
        # MIME Protection
        # -------------------------

        if "X-Content-Type-Options" not in headers:

            score -= 10

            recommendations.append(
                "X-Content-Type-Options header is missing."
            )

        # -------------------------
        # Referrer
        # -------------------------

        if "Referrer-Policy" not in headers:

            score -= 5

            recommendations.append(
                "Referrer Policy header is missing."
            )

        # -------------------------
        # Permissions Policy
        # -------------------------

        if "Permissions-Policy" not in headers:

            score -= 5

            recommendations.append(
                "Permissions Policy header is missing."
            )

        # -------------------------
        # Cross Origin Policy
        # -------------------------

        if "Cross-Origin-Opener-Policy" not in headers:

            score -= 5

            recommendations.append(
                "Cross-Origin-Opener-Policy header is missing."
            )

        # -------------------------
        # Server Disclosure
        # -------------------------

        server = headers.get("Server")

        if server:

            score -= 3

            recommendations.append(
                "Server header exposes server information."
            )

        # -------------------------
        # Powered By
        # -------------------------

        powered = headers.get("X-Powered-By")

        if powered:

            score -= 5

            recommendations.append(
                "X-Powered-By header exposes technology."
            )

    except Exception as e:

        score = 20

        recommendations.append(
            f"Security scan failed: {str(e)}"
        )

    return {

        "score": max(0, min(score, 100)),

        "recommendations": recommendations,

    }