import pandas as pd

def analyze_trends(file_path):
    df = pd.read_csv(file_path)

    # Trend score formula
    df["trend_score"] = (df["views"] / 1000) + df["growth_rate"]

    df = df.sort_values(by="trend_score", ascending=False)

    return df


def get_top_trend(df):
    return df.iloc[0]