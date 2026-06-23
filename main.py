import pandas as pd
from business_finder.scorer import calculate_score, get_recommendation

print("Growth Radar AI")
print("----------------")

df = pd.read_csv("data/businesses.csv")

# Calculate scores
df["score"] = df.apply(calculate_score, axis=1)

# Generate recommendations
df["recommendation"] = df["score"].apply(get_recommendation)

# Sort by score (lowest first = best leads)
df = df.sort_values(by="score")

print(df)

# Save report
df.to_csv("reports/business_report.csv", index=False)

print("\nReport saved to reports/business_report.csv")
total = len(df)
high = len(df[df["recommendation"] == "High Priority Lead"])
medium = len(df[df["recommendation"] == "Medium Priority"])
low = len(df[df["recommendation"] == "Low Priority"])

print("\nSUMMARY")
print("-------")
print("Total Leads:", total)
print("High Priority:", high)
print("Medium Priority:", medium)
print("Low Priority:", low)
best_lead = df.iloc[0]
df = df.sort_values(by="score")
print("\nTOP LEADS DASHBOARD")
print("-------------------")

print(df[["name", "score", "recommendation"]].to_string(index=False))
best_lead = df.iloc[0]

print("\nBEST LEAD")
print("---------")
print(best_lead["name"], "| Score:", best_lead["score"])
