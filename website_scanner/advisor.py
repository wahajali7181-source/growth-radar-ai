def generate_ai_summary(report):

    score = report["overall_score"]

    health = report["health"]["score"]
    seo = report["seo"]["score"]
    security = report["security"]["score"]
    performance = report["performance"]["score"]

    technologies = report.get("technologies", [])

    # ---------------------------------
    # Grade
    # ---------------------------------

    if score >= 95:
        grade = "A+"
        priority = "🟢 Very Low"

    elif score >= 90:
        grade = "A"
        priority = "🟢 Low"

    elif score >= 80:
        grade = "B"

        priority = "🟡 Medium"

    elif score >= 70:

        grade = "C"

        priority = "🟠 High"

    elif score >= 60:

        grade = "D"

        priority = "🔴 Very High"

    else:

        grade = "F"

        priority = "🚨 Critical"

    # ---------------------------------
    # Strengths
    # ---------------------------------

    strengths = []

    if health >= 85:
        strengths.append("Good website health")

    if seo >= 85:
        strengths.append("Strong SEO foundation")

    if security >= 85:
        strengths.append("Good security configuration")

    if performance >= 85:
        strengths.append("Fast loading website")

    if technologies:
        strengths.append(
            "Modern technology stack detected"
        )

    if not strengths:
        strengths.append(
            "Basic website is online"
        )

    # ---------------------------------
    # Weaknesses
    # ---------------------------------

    weaknesses = []

    if health < 80:
        weaknesses.append(
            "Website health needs improvement"
        )

    if seo < 80:
        weaknesses.append(
            "SEO optimization required"
        )

    if security < 80:
        weaknesses.append(
            "Security configuration is weak"
        )

    if performance < 80:
        weaknesses.append(
            "Website speed should be improved"
        )

    # ---------------------------------
    # Executive Summary
    # ---------------------------------

    summary = f"""
### Executive Summary

Overall Website Score: **{score}/100**

Overall Grade: **{grade}**

Priority Level: **{priority}**

The website audit indicates the current digital presence has an overall quality score of **{score}/100**.

Strengths:

{chr(10).join([f"- {x}" for x in strengths])}

Improvement Areas:

{chr(10).join([f"- {x}" for x in weaknesses]) if weaknesses else "- No major weaknesses detected."}

Business Recommendation:

Improving SEO, website performance, technical health and security can significantly increase search rankings, user experience and lead generation.

Growth Radar AI recommends prioritizing the highest-impact improvements first to maximize ROI.
"""

    return {

        "summary": summary,

        "grade": grade,

        "priority": priority,

        "strengths": strengths,

        "weaknesses": weaknesses,

    }