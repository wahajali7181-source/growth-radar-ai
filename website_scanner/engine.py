from website_scanner.health import calculate_health_score
from website_scanner.seo import analyze_seo
from website_scanner.security import analyze_security
from website_scanner.performance import analyze_performance
from website_scanner.technology import detect_technology


def analyze_website(url):

    health = calculate_health_score(url)

    seo = analyze_seo(url)

    security = analyze_security(url)

    performance = analyze_performance(url)

    technologies = detect_technology(url)

    overall = round(

        (

            health["score"]

            + seo["score"]

            + security["score"]

            + performance["score"]

        ) / 4

    )

    return {

        "overall_score": overall,

        "health": health,

        "seo": seo,

        "security": security,

        "performance": performance,

        "technologies": technologies

    }