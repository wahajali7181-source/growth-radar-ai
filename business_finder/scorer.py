import pandas as pd

def calculate_score(row):
    score = 100

    if row["website"] == "no":
        score -= 40

    if row["instagram"] == "no":
        score -= 20

    return score
