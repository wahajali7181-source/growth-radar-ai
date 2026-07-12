from ai_core.gemini_engine import ask_gemini
from ai_prompts.recommendation_prompt import build_recommendation_prompt


def generate_ai_actions(report):

    scanner = report.get("scanner", {})
    seo = report.get("seo", {})
    security = report.get("security", {})

    actions = []

    # =========================
    # WEBSITE
    # =========================

    if scanner.get("status_code") != 200:

        actions.append({
            "priority": "HIGH",
            "title": "Website is not accessible",
            "description": "Fix website availability immediately."
        })

    load_time = scanner.get("load_time", 0)

    try:
        load_time = float(
            str(load_time)
            .replace("sec", "")
            .replace("seconds", "")
            .strip()
        )
    except:
        load_time = 0

    if load_time > 3:

        actions.append({
            "priority": "HIGH",
            "title": "Improve Website Speed",
            "description": "Slow websites lose visitors and revenue."
        })

    # =========================
    # SEO
    # =========================

    if seo.get("meta_description") == "❌ Not Found":

        actions.append({
            "priority": "HIGH",
            "title": "Add Meta Description",
            "description": "Missing meta description hurts SEO."
        })

    if seo.get("h1_count", 0) == 0:

        actions.append({
            "priority": "MEDIUM",
            "title": "Add H1 Heading",
            "description": "Every page should contain one H1 heading."
        })

    # =========================
    # SECURITY
    # =========================

    if security.get("ssl") != "✅ Enabled":

        actions.append({
            "priority": "HIGH",
            "title": "Enable SSL",
            "description": "Protect visitors using HTTPS."
        })

    if security.get("content_security_policy") != "✅ Enabled":

        actions.append({
            "priority": "MEDIUM",
            "title": "Enable Content Security Policy",
            "description": "Improve browser security."
        })

    if security.get("permissions_policy") == "❌ Missing":

        actions.append({
            "priority": "LOW",
            "title": "Add Permissions Policy",
            "description": "Modern browsers recommend Permissions Policy."
        })

    # =========================
    # GEMINI AI
    # =========================

    prompt = build_recommendation_prompt(report)

    try:

        ai_analysis = ask_gemini(prompt)

    except Exception as e:

        ai_analysis = f"Gemini Error: {e}"

    return {
        "actions": actions,
        "analysis": ai_analysis
    }