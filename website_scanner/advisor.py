def generate_ai_summary(report):

    score = report["overall_score"]

    if score >= 90:

        summary = (
            "Excellent website. Only minor improvements are recommended."
        )

        priority = "🟢 LOW"

        grade = "A+"

    elif score >= 80:

        summary = (
            "Strong website with a few optimization opportunities."
        )

        priority = "🟡 MEDIUM"

        grade = "A"

    elif score >= 70:

        summary = (
            "Average website. SEO and performance improvements are recommended."
        )

        priority = "🟠 HIGH"

        grade = "B"

    elif score >= 60:

        summary = (
            "Weak online presence. Several technical improvements are required."
        )

        priority = "🔴 HIGH"

        grade = "C"

    else:

        summary = (
            "Critical website condition. Immediate optimization is recommended."
        )

        priority = "🚨 CRITICAL"

        grade = "F"

    return {

        "summary": summary,

        "priority": priority,

        "grade": grade

    }