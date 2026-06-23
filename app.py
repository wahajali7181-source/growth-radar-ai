import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

from business_finder.scorer import calculate_score, get_recommendation

# Trend Radar import (safe)
from trend_radar.analyzer import analyze_trends, get_top_trend


st.set_page_config(page_title="Growth Radar AI", layout="wide")

# =========================
# HEADER
# =========================
st.title("🚀 Growth Radar AI - AI Business Intelligence Suite")
st.caption("Lead Finder + Trend Radar AI in one platform")

st.info("""
👋 Welcome to Growth Radar AI

This tool helps you:
- Find high quality business leads
- Analyze business scores
- Detect trending topics
- Generate insights for growth
""")

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("📂 Upload Business CSV File")

if uploaded_file is None:
    st.warning("Upload a CSV file to start analysis")

if uploaded_file is not None:

    df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))

    # =========================
    # LEAD SCORING
    # =========================
    df["score"] = df.apply(calculate_score, axis=1)
    df["recommendation"] = df["score"].apply(get_recommendation)

    df = df.sort_values(by="score")

    # =========================
    # STATS
    # =========================
    st.subheader("📊 Lead Stats")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Leads", len(df))
    col2.metric("High Priority", len(df[df["recommendation"] == "High Priority Lead"]))
    col3.metric("Best Score", df["score"].max())

    st.divider()

    # =========================
    # DASHBOARD
    # =========================
    st.subheader("📋 Lead Dashboard")

    st.dataframe(df[["name", "score", "recommendation"]])

    # Download report
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "⬇ Download Report",
        csv,
        "lead_report.csv",
        "text/csv"
    )

    st.divider()

    # =========================
    # BEST LEAD
    # =========================
    best = df.iloc[0]

    st.subheader("🏆 Best Lead")

    st.success(f"{best['name']} | Score: {best['score']} | {best['recommendation']}")

    # =========================
    # INSIGHT
    # =========================
    st.subheader("🧠 AI Insight")

    if best["score"] > 80:
        st.info("Strong digital presence - High conversion potential")
    elif best["score"] > 50:
        st.warning("Medium opportunity - Needs improvement")
    else:
        st.error("Low presence - Easy outreach target")

    st.divider()

    # =========================
    # CHARTS
    # =========================
    st.subheader("📊 Score Chart")

    fig, ax = plt.subplots()
    ax.bar(df["name"], df["score"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # =========================
    # TREND RADAR AI
    # =========================
    st.divider()

    st.header("📈 Trend Radar AI (Beta)")

    if st.button("Analyze Trends"):

        df_trends = analyze_trends("trend_radar/trends_data.csv")

        st.subheader("📊 Trend Dashboard")
        st.dataframe(df_trends)

        top = get_top_trend(df_trends)

        st.success(f"🔥 Top Trend: {top['keyword']} | Score: {top['trend_score']}")

        st.info("💡 Create content around this topic for maximum reach")

        st.bar_chart(df_trends.set_index("keyword")["trend_score"])