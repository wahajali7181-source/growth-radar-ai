def calculate_presence_score(business):

    score = 0

    # Website
    if business.get("website"):
        score += 25

    # Facebook
    if business.get("facebook"):
        score += 15

    # Instagram
    if business.get("instagram"):
        score += 15

    # LinkedIn
    if business.get("linkedin"):
        score += 10

    # Email
    if business.get("email"):
        score += 15

    # Phone
    if business.get("phone"):
        score += 10

    # Google Rating
    rating = business.get("rating")

    if rating:

        if rating >= 4.5:
            score += 10

    return min(score, 100)