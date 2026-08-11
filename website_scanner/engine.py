from website_scanner.health import calculate_health_score
from website_scanner.seo import analyze_seo
from website_scanner.security import analyze_security
from website_scanner.performance import analyze_performance
from website_scanner.technology import detect_technology


def _calculate_overall(scores):

    if not scores:
        return 0

    return round(sum(scores) / len(scores))


def _calculate_grade(score):

    if score >= 90:
        return "A+"

    if score >= 80:
        return "A"

    if score >= 70:
        return "B"

    if score >= 60:
        return "C"

    if score >= 50:
        return "D"

    return "F"


def _calculate_priority(score):

    if score >= 85:
        return "Low"

    if score >= 70:
        return "Medium"

    return "High"


def analyze_website(url):

    health = calculate_health_score(url)

    seo = analyze_seo(url)

    security = analyze_security(url)

    performance = analyze_performance(url)

    technologies = detect_technology(url)

    scores = [

        health["score"],

        seo["score"],

        security["score"],

        performance["score"],

    ]

    overall = _calculate_overall(scores)

    grade = _calculate_grade(overall)

    priority = _calculate_priority(overall)

    total_recommendations = (
        len(health["recommendations"])
        + len(seo["recommendations"])
        + len(security["recommendations"])
        + len(performance["recommendations"])
    )

    return {

        "url": url,

        "overall_score": overall,

        "grade": grade,

        "priority": priority,

        "recommendation_count": total_recommendations,

        "health": health,

        "seo": seo,

        "security": security,

        "performance": performance,

        "technologies": technologies,

    }