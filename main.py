import pandas as pd
from business_finder.scorer import calculate_score, get_recommendation

print("Growth Radar AI")
print("----------------")

# Read business data
df = pd.read_csv("data/businesses.csv")

# Calculate scores
df["score"] = df.apply(calculate_score, axis=1)

# Generate recommendations
df["recommendation"] = df["score"].apply(get_recommendation)

# Display results
print(df)

# Save report
df.to_csv("reports/business_report.csv", index=False)

print("\nReport saved to reports/business_report.csv")