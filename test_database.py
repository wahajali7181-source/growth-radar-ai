from lead_engine.database import load_businesses

df = load_businesses()

print(df)
print()
print("Total Businesses:", len(df))