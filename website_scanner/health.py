import requests


def calculate_health_score(url):

    score = 100

    recommendations = []

    try:

        response = requests.get(

            url,

            timeout=10,

            headers={

                "User-Agent": "GrowthRadarAI"

            }

        )

        if response.status_code != 200:

            score -= 20

            recommendations.append(

                "Website returned an unexpected status."

            )

        if not url.startswith("https://"):

            score -= 20

            recommendations.append(

                "Website is not using HTTPS."

            )

        html = response.text.lower()

        if "<title>" not in html:

            score -= 10

            recommendations.append(

                "Missing page title."

            )

        if "meta name=\"description\"" not in html:

            score -= 10

            recommendations.append(

                "Missing meta description."

            )

    except Exception:

        score = 10

        recommendations.append(

            "Website could not be reached."

        )

    return {

        "score": max(score, 0),

        "recommendations": recommendations

    }