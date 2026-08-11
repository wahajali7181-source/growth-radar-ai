import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 GrowthRadarAI Performance Scanner"
}


def analyze_performance(url):

    score = 100

    recommendations = []

    try:

        response = requests.get(

            url,

            timeout=15,

            headers=HEADERS,

            allow_redirects=True,

        )

        # -------------------------
        # Load Time
        # -------------------------

        load_time = response.elapsed.total_seconds()

        if load_time >= 5:

            score -= 35

            recommendations.append(
                "Website is extremely slow."
            )

        elif load_time >= 3:

            score -= 20

            recommendations.append(
                "Website loading speed should be improved."
            )

        elif load_time >= 2:

            score -= 10

            recommendations.append(
                "Loading speed can be optimized."
            )

        # -------------------------
        # Page Size
        # -------------------------

        page_size = len(response.content)

        page_size_mb = page_size / (1024 * 1024)

        if page_size_mb >= 5:

            score -= 25

            recommendations.append(
                "Page size is extremely large."
            )

        elif page_size_mb >= 3:

            score -= 15

            recommendations.append(
                "Reduce page size."
            )

        elif page_size_mb >= 2:

            score -= 8

            recommendations.append(
                "Optimize images and assets."
            )

        # -------------------------
        # Compression
        # -------------------------

        encoding = response.headers.get(

            "Content-Encoding",

            ""

        ).lower()

        if "gzip" not in encoding and "br" not in encoding:

            score -= 8

            recommendations.append(
                "Enable GZIP/Brotli compression."
            )

        # -------------------------
        # Cache
        # -------------------------

        if "Cache-Control" not in response.headers:

            score -= 6

            recommendations.append(
                "Cache-Control header is missing."
            )

        # -------------------------
        # Keep Alive
        # -------------------------

        connection = response.headers.get(

            "Connection",

            ""

        ).lower()

        if connection == "close":

            score -= 5

            recommendations.append(
                "Keep-Alive connection is not enabled."
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

        score = 10

        recommendations.append(
            f"Performance scan failed: {str(e)}"
        )

    return {

        "score": max(0, min(score, 100)),

        "recommendations": recommendations,

    }