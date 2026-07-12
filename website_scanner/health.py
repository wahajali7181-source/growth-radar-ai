def calculate_health_score(report):

    scanner = report["scanner"]
    seo = report["seo"]
    security = report["security"]

    score = 0

    # ======================
    # WEBSITE (30 Marks)
    # ======================

    if scanner["status"] == "🟢 Online":
        score += 10

    if scanner["ssl"] == "✅ Enabled":
        score += 10

    if scanner["favicon"] != "❌ Not Found":
        score += 5

    if scanner["meta_description"] != "Not Found":
        score += 5

    # ======================
    # SEO (40 Marks)
    # ======================

    if seo["canonical"] != "❌ Not Found":
        score += 8

    if seo["open_graph"] == "✅ Present":
        score += 8

    if seo["twitter_cards"] == "✅ Present":
        score += 5

    if seo["robots_txt"] != "❌ Not Found":
        score += 7

    if seo["sitemap_xml"] != "❌ Not Found":
        score += 7

    if seo["h1_count"] > 0:
        score += 5

    # ======================
    # SECURITY (30 Marks)
    # ======================

    if security["hsts"] == "✅ Enabled":
        score += 8

    if security["content_security_policy"] == "✅ Enabled":
        score += 8

    if security["x_frame_options"] != "❌ Missing":
        score += 5

    if security["x_content_type_options"] != "❌ Missing":
        score += 5

    if security["referrer_policy"] != "❌ Missing":
        score += 4

    # ======================
    # Grade
    # ======================

    if score >= 90:
        grade = "A+"

    elif score >= 80:
        grade = "A"

    elif score >= 70:
        grade = "B"

    elif score >= 60:
        grade = "C"

    elif score >= 50:
        grade = "D"

    else:
        grade = "F"

    return {
        "score": score,
        "grade": grade
    }