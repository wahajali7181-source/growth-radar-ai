import pandas as pd

def calculate_score(row):
    score = 100

    if row["website"] == "no":
        score -= 40

    if row["instagram"] == "no":
        score -= 20

    return score
def get_recommendation(score):
    if score < 50:
        return "High Priority Lead"
    elif score < 80:
        return "Medium Priority"
    else:
        return "Low Priority"
    import pandas as pd

def calculate_score(row):
    score = 100

    if row["website"] == "no":
        score -= 40

    if row["instagram"] == "no":
        score -= 20

    return score

def get_recommendation(score):
    if score < 50:
        return "High Priority Lead"
    elif score < 80:
        return "Medium Priority"
    else:
        return "Low Priority"