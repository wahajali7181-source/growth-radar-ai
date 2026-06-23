def calculate_score(row):
    score = 0

    # safe access using .get()
    if row.get("website", "no") == "yes":
        score += 30

    if row.get("instagram", "no") == "yes":
        score += 20

    if row.get("facebook", "no") == "yes":
        score += 20

    reviews = int(row.get("google_reviews", 0))

    if reviews > 100:
        score += 30
    elif reviews > 50:
        score += 20
    elif reviews > 10:
        score += 10

    return score


def get_recommendation(score):
    if score < 50:
        return "High Priority Lead"
    elif score < 80:
        return "Medium Priority"
    else:
        return "Low Priority"