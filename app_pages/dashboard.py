import streamlit as st
import pandas as pd

from lead_engine.database import load_businesses


def show():

    st.title("🚀 Growth Radar AI Dashboard")
    st.caption("AI Powered Business Intelligence Platform")

    df = load_businesses()

    if df.empty:
        st.info("No businesses available.")
        return

    total = len(df)

    excellent = len(df[df["opportunity"] == "🟢 Excellent"])
    good = len(df[df["opportunity"] == "🟡 Good"])
    average = len(df[df["opportunity"] == "🟠 Average"])
    high = len(df[df["opportunity"] == "🔴 High Opportunity"])

    avg_score = round(df["lead_score"].mean(), 1)

    st.subheader("📊 Business Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Businesses", total)
    c2.metric("Excellent", excellent)
    c3.metric("Good", good)
    c4.metric("Average Score", avg_score)

    st.divider()

    left, right = st.columns([2, 1])

    with left:

        st.subheader("📈 Opportunity Distribution")

        chart_data = pd.DataFrame(
            {
                "Category": [
                    "Excellent",
                    "Good",
                    "Average",
                    "High Opportunity"
                ],
                "Businesses": [
                    excellent,
                    good,
                    average,
                    high
                ]
            }
        )

        st.bar_chart(
            chart_data.set_index("Category")
        )

    with right:

        st.subheader("🤖 AI Insights")

        if high > 0:
            st.warning(f"🔴 {high} businesses have high growth opportunity.")

        if excellent > 0:
            st.success(f"🟢 {excellent} businesses already have a strong presence.")

        st.info(f"⭐ Average Lead Score: {avg_score}/100")

    st.divider()

    st.subheader("🕒 Recent Businesses")

    latest = (
        df.sort_values("id", ascending=False)
        .head(10)
    )

    st.dataframe(
        latest,
        use_container_width=True,
        hide_index=True
    )