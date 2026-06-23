import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

from business_finder.scorer import calculate_score, get_recommendation


st.set_page_config(page_title="Growth Radar AI", layout="wide")

# =========================
# HEADER
# =========================
st.title("🚀 Growth Radar AI")
st.caption("AI Lead Finder & Business Intelligence Tool")

st.info("""
👋 Welcome!

Upload a CSV file and get:
- Lead scoring
- Priority ranking
- Business insights
""")

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("📂 Upload Business CSV File")

if uploaded_file is None:
    st.warning("Upload a CSV file to start analysis.")

if uploaded_file is not None:

    # SAFE CSV READ
    df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))

    # =========================
    # SCORING
    # =========================
    df["score"] = df.apply(calculate_score, axis=1)
    df["recommendation"] = df["score"].apply(get_recommendation)

    df = df.sort_values(by="score", ascending=False)

    # =========================
    # STATS
    # =========================
    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Leads", len(df))
    col2.metric("High Priority", len(df[df["recommendation"] == "High Priority Lead"]))
    col3.metric("Best Score", df["score"].max())

    st.divider()

    # =========================
    # TABLE
    # =========================
    st.subheader("📋 Leads Dashboard")

    st.dataframe(df[["name", "score", "recommendation"]])

    # DOWNLOAD REPORT
    csv = df.to_csv(index=False).encode("utf-8")

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
    # AI INSIGHT
    # =========================
    st.subheader("🧠 AI Insight")

    if best["score"] > 80:
        st.info("Strong digital presence - High conversion potential")
    elif best["score"] > 50:
        st.warning("Medium opportunity - Needs improvement")
    else:
        st.error("Low presence - Easy target")

    st.divider()

    # =========================
    # CHART
    # =========================
    st.subheader("📊 Score Chart")

    fig, ax = plt.subplots()
    ax.bar(df["name"], df["score"])
    plt.xticks(rotation=45)

    st.pyplot(fig)