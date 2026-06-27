def calculate_lead_score(business):

    score = 0

    # Website
    if str(business.get("website", "")).lower() == "yes":
        score += 30

    # Rating
    rating = float(business.get("rating", 0))

    if rating >= 4.8:
        score += 30

    elif rating >= 4.5:
        score += 25

    elif rating >= 4.0:
        score += 20

    elif rating >= 3.5:
        score += 10

    # Reviews
    reviews = int(business.get("reviews", 0))

    if reviews >= 500:
        score += 40

    elif reviews >= 200:
        score += 30

    elif reviews >= 100:
        score += 20

    elif reviews >= 50:
        score += 10

    return min(score, 100)


def opportunity_level(score):

    if score >= 80:
        return "🟢 Excellent"

    elif score >= 60:
        return "🟡 Good"

    elif score >= 40:
        return "🟠 Average"

    return "🔴 High Opportunity"