def get_business_advice(business):

    advice = []

    # Website
    if str(business.get("website", "")).lower() != "yes":
        advice.append("• Build a professional website.")

    # Rating
    if float(business.get("rating", 0)) < 4.5:
        advice.append("• Improve Google rating by requesting customer reviews.")

    # Reviews
    if int(business.get("reviews", 0)) < 100:
        advice.append("• Increase Google reviews to improve trust.")

    # Lead Score
    if business["lead_score"] >= 80:
        advice.append("• Excellent lead. Contact immediately.")

    elif business["lead_score"] >= 60:
        advice.append("• Good opportunity for Meta Ads and SEO.")

    else:
        advice.append("• Needs complete digital marketing strategy.")

    return "\n".join(advice)