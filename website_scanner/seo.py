import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 GrowthRadarAI SEO Scanner"
}


def analyze_seo(url):

    score = 100

    recommendations = []

    try:

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=15,

        )

        soup = BeautifulSoup(

            response.text,

            "html.parser",

        )

        # -------------------------
        # Title
        # -------------------------

        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        if not title:

            score -= 20

            recommendations.append(
                "Missing page title."
            )

        elif len(title) < 30:

            score -= 5

            recommendations.append(
                "Page title is too short."
            )

        elif len(title) > 60:

            score -= 5

            recommendations.append(
                "Page title is too long."
            )

        # -------------------------
        # Meta Description
        # -------------------------

        meta = soup.find(

            "meta",

            attrs={"name": "description"}

        )

        description = meta.get("content", "").strip() if meta else ""

        if not description:

            score -= 20

            recommendations.append(
                "Missing meta description."
            )

        elif len(description) < 70:

            score -= 5

            recommendations.append(
                "Meta description is too short."
            )

        elif len(description) > 160:

            score -= 5

            recommendations.append(
                "Meta description is too long."
            )

        # -------------------------
        # H1
        # -------------------------

        h1_tags = soup.find_all("h1")

        if len(h1_tags) == 0:

            score -= 15

            recommendations.append(
                "No H1 heading found."
            )

        elif len(h1_tags) > 1:

            score -= 5

            recommendations.append(
                "Multiple H1 headings detected."
            )

        # -------------------------
        # Images ALT
        # -------------------------

        images = soup.find_all("img")

        if images:

            missing_alt = sum(
                1 for img in images if not img.get("alt")
            )

            if missing_alt:

                penalty = min(20, missing_alt)

                score -= penalty

                recommendations.append(
                    f"{missing_alt} image(s) are missing ALT text."
                )

        # -------------------------
        # Canonical
        # -------------------------

        canonical = soup.find(

            "link",

            attrs={"rel": "canonical"}

        )

        if canonical is None:

            score -= 5

            recommendations.append(
                "Canonical tag is missing."
            )

        # -------------------------
        # Open Graph
        # -------------------------

        og = soup.find(

            "meta",

            attrs={"property": "og:title"}

        )

        if og is None:

            score -= 5

            recommendations.append(
                "Open Graph tags are missing."
            )

        # -------------------------
        # Robots
        # -------------------------

        robots = soup.find(

            "meta",

            attrs={"name": "robots"}

        )

        if robots is None:

            score -= 3

            recommendations.append(
                "Robots meta tag not found."
            )

    except Exception as e:

        score = 20

        recommendations.append(
            f"SEO scan failed: {str(e)}"
        )

    return {

        "score": max(0, min(score, 100)),

        "recommendations": recommendations,

    }