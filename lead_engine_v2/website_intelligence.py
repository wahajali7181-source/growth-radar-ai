from website_scanner.engine import analyze_website


def enrich_website(lead):

    if not lead.website:

        return lead

    try:

        report = analyze_website(

            lead.website

        )

        lead.website_health = report["health"]["score"]

        lead.seo_score = report["seo"]["score"]

        lead.security_score = report["security"]["score"]

        lead.performance_score = report["performance"]["score"]

    except Exception:

        pass

    return lead