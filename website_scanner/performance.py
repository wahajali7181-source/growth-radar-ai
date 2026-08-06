import requests


def analyze_performance(url):

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

        load_time = response.elapsed.total_seconds()

        if load_time > 3:

            score -= 30

            recommendations.append(

                "Website loads slowly."

            )

        elif load_time > 2:

            score -= 15

            recommendations.append(

                "Improve page speed."

            )

        if len(response.text) > 1500000:

            score -= 10

            recommendations.append(

                "Large page size detected."

            )

    except Exception:

        score = 20

        recommendations.append(

            "Website is unreachable."

        )

    return {

        "score": max(score, 0),

        "recommendations": recommendations

    }