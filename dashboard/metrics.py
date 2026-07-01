import pandas as pd


def get_dashboard_metrics(df: pd.DataFrame):

    if df.empty:

        return {
            "businesses": 0,
            "qualified": 0,
            "average_score": 0,
            "high_opportunity": 0,
            "estimated_revenue": 0
        }

    total = len(df)

    qualified = len(
        df[df["lead_score"] >= 60]
    )

    average_score = round(
        df["lead_score"].mean(),
        1
    )

    high_opportunity = len(
        df[df["opportunity"] == "🟢 Excellent"]
    )

    estimated_revenue = qualified * 1500

    return {

        "businesses": total,

        "qualified": qualified,

        "average_score": average_score,

        "high_opportunity": high_opportunity,

        "estimated_revenue": estimated_revenue
    }