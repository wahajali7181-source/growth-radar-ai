import pandas as pd
from business_finder.scorer import calculate_score, get_recommendation

print("Growth Radar AI")
print("----------------")

df = pd.read_csv("data/businesses.csv")

df["score"] = df.apply(calculate_score, axis=1)
df["recommendation"] = df["score"].apply(get_recommendation)

print(df)