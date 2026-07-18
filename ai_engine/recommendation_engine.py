class RecommendationEngine:

    def generate(
        self,
        scanner,
        seo,
        score
    ):

        recommendations = []

        if scanner["status"] != "Online":
            recommendations.append(
                "Website appears offline. Restore it immediately."
            )

        if scanner["ssl"] != "✅ Yes":
            recommendations.append(
                "Enable HTTPS SSL certificate."
            )

        if scanner["meta_description"] == "Not Found":
            recommendations.append(
                "Add a compelling meta description."
            )

        if seo["canonical"] == "❌ Not Found":
            recommendations.append(
                "Add canonical URLs."
            )

        if seo["robots_txt"] == "❌ Not Found":
            recommendations.append(
                "Create robots.txt."
            )

        if seo["sitemap_xml"] == "❌ Not Found":
            recommendations.append(
                "Generate sitemap.xml."
            )

        if seo["open_graph"] == "❌ Not Found":
            recommendations.append(
                "Add Open Graph tags."
            )

        if seo["twitter_cards"] == "❌ Not Found":
            recommendations.append(
                "Add Twitter Cards."
            )

        if seo["h1_count"] == 0:
            recommendations.append(
                "Homepage should contain an H1 heading."
            )

        if score >= 90:
            level = "🟢 Excellent"

        elif score >= 70:
            level = "🟡 Good"

        elif score >= 40:
            level = "🟠 Needs Improvement"

        else:
            level = "🔴 High Priority"

        return {
            "score": score,
            "level": level,
            "recommendations": recommendations
        }


recommendation_engine = RecommendationEngine()


# ======================================================
# AI Action Plan
# ======================================================

def generate_ai_actions(report):

    scanner = report["scanner"]
    seo = report["seo"]
    security = report["security"]

    actions = []

    if scanner["status"] != "Online":
        actions.append({
            "priority": "HIGH",
            "title": "Website Offline",
            "description": "Restore the website immediately."
        })

    if scanner["ssl"] != "✅ Yes":
        actions.append({
            "priority": "HIGH",
            "title": "Enable SSL",
            "description": "Install an SSL certificate and use HTTPS."
        })

    if seo["meta_description"] == "Not Found":
        actions.append({
            "priority": "MEDIUM",
            "title": "Add Meta Description",
            "description": "Write an SEO optimized meta description."
        })

    if seo["canonical"] == "❌ Not Found":
        actions.append({
            "priority": "MEDIUM",
            "title": "Add Canonical Tag",
            "description": "Prevent duplicate content issues."
        })

    if seo["robots_txt"] == "❌ Not Found":
        actions.append({
            "priority": "LOW",
            "title": "Create robots.txt",
            "description": "Allow search engines to crawl correctly."
        })

    if seo["sitemap_xml"] == "❌ Not Found":
        actions.append({
            "priority": "LOW",
            "title": "Generate Sitemap",
            "description": "Create sitemap.xml for indexing."
        })

    if security["content_security_policy"] == "❌ Missing":
        actions.append({
            "priority": "MEDIUM",
            "title": "Improve Security Headers",
            "description": "Add Content Security Policy."
        })

    analysis = (
        f"Overall website health analysis completed. "
        f"{len(actions)} improvement opportunities detected."
    )

    return {
        "actions": actions,
        "analysis": analysis
    }