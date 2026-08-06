import requests
from bs4 import BeautifulSoup


HEADERS = {

    "User-Agent": "GrowthRadarAI"

}


def analyze_seo(url):

    score = 100

    recommendations = []

    try:

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=10

        )

        soup = BeautifulSoup(

            response.text,

            "html.parser"

        )

        # -------------------------
        # Title
        # -------------------------

        if not soup.title:

            score -= 20

            recommendations.append(

                "Missing page title."

            )

        # -------------------------
        # Meta Description
        # -------------------------

        meta = soup.find(

            "meta",

            attrs={

                "name": "description"

            }

        )

        if not meta:

            score -= 20

            recommendations.append(

                "Missing meta description."

            )

        # -------------------------
        # H1
        # -------------------------

        h1 = soup.find_all("h1")

        if len(h1) == 0:

            score -= 15

            recommendations.append(

                "No H1 heading found."

            )

        elif len(h1) > 1:

            score -= 5

            recommendations.append(

                "Multiple H1 headings detected."

            )

        # -------------------------
        # Images ALT
        # -------------------------

        images = soup.find_all("img")

        missing_alt = 0

        for img in images:

            if not img.get("alt"):

                missing_alt += 1

        if missing_alt:

            score -= min(

                20,

                missing_alt

            )

            recommendations.append(

                f"{missing_alt} images are missing ALT text."

            )

    except Exception:

        score = 20

        recommendations.append(

            "Unable to analyze SEO."

        )

    return {

        "score": max(score, 0),

        "recommendations": recommendations

    }