import requests


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 GrowthRadarAI Website Scanner"
    )
}


def calculate_health_score(url):

    score = 100

    recommendations = []

    try:

        response = requests.get(

            url,

            timeout=15,

            headers=HEADERS,

            allow_redirects=True,

        )

        html = response.text.lower()

        status = response.status_code

        final_url = response.url

        # --------------------------------
        # Status Code
        # --------------------------------

        if status >= 500:

            score -= 40

            recommendations.append(
                "Server is returning 5xx errors."
            )

        elif status >= 400:

            score -= 30

            recommendations.append(
                "Website returned client errors."
            )

        elif status >= 300:

            score -= 10

            recommendations.append(
                "Website redirects users before loading."
            )

        # --------------------------------
        # HTTPS
        # --------------------------------

        if not final_url.startswith("https://"):

            score -= 20

            recommendations.append(
                "Website is not secured with HTTPS."
            )

        # --------------------------------
        # HTML Checks
        # --------------------------------

        if "<title>" not in html:

            score -= 10

            recommendations.append(
                "Missing HTML title tag."
            )

        if 'meta name="description"' not in html and \
           "meta name='description'" not in html:

            score -= 10

            recommendations.append(
                "Meta description is missing."
            )

        if "<h1" not in html:

            score -= 5

            recommendations.append(
                "No H1 heading detected."
            )

        if "<html" not in html:

            score -= 5

            recommendations.append(
                "HTML document appears invalid."
            )

        # --------------------------------
        # Page Size
        # --------------------------------

        size_kb = len(response.content) / 1024

        if size_kb > 2500:

            score -= 10

            recommendations.append(
                "Page size is very large."
            )

        elif size_kb > 1500:

            score -= 5

            recommendations.append(
                "Large page size may slow loading."
            )

    except requests.exceptions.Timeout:

        score = 10

        recommendations.append(
            "Website timed out."
        )

    except requests.exceptions.ConnectionError:

        score = 10

        recommendations.append(
            "Unable to connect to website."
        )

    except Exception as e:

        score = 5

        recommendations.append(
            f"Health scan failed: {str(e)}"
        )

    return {

        "score": max(0, min(score, 100)),

        "recommendations": recommendations,

    }