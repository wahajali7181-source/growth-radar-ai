import requests


HEADERS = {

    "User-Agent": "GrowthRadarAI"

}


def analyze_security(url):

    score = 100

    recommendations = []

    try:

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=10

        )

        headers = response.headers

        if not url.startswith("https://"):

            score -= 30

            recommendations.append(

                "Website is not using HTTPS."

            )

        if "Strict-Transport-Security" not in headers:

            score -= 15

            recommendations.append(

                "HSTS header is missing."

            )

        if "Content-Security-Policy" not in headers:

            score -= 20

            recommendations.append(

                "Content Security Policy is missing."

            )

        if "X-Frame-Options" not in headers:

            score -= 10

            recommendations.append(

                "X-Frame-Options header is missing."

            )

        if "X-Content-Type-Options" not in headers:

            score -= 10

            recommendations.append(

                "X-Content-Type-Options header is missing."

            )

        if "Referrer-Policy" not in headers:

            score -= 5

            recommendations.append(

                "Referrer Policy header is missing."

            )

    except Exception:

        score = 20

        recommendations.append(

            "Unable to analyze website security."

        )

    return {

        "score": max(score, 0),

        "recommendations": recommendations

    }