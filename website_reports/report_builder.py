from datetime import datetime


def build_report(report, ai):

    return {

        "generated_on": datetime.now().strftime(
            "%d %B %Y %I:%M %p"
        ),

        "website": report["url"],

        "overall_score": report["overall_score"],

        "grade": ai["grade"],

        "priority": ai["priority"],

        "health_score": report["health"]["score"],

        "seo_score": report["seo"]["score"],

        "security_score": report["security"]["score"],

        "performance_score": report["performance"]["score"],

        "technologies": report["technologies"],

        "summary": ai["summary"],

        "strengths": ai["strengths"],

        "weaknesses": ai["weaknesses"],

        "health_recommendations":
            report["health"]["recommendations"],

        "seo_recommendations":
            report["seo"]["recommendations"],

        "security_recommendations":
            report["security"]["recommendations"],

        "performance_recommendations":
            report["performance"]["recommendations"]

    }