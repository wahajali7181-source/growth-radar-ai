import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

from business_finder.scorer import calculate_score, get_recommendation

st.set_page_config(page_title="Growth Radar AI", layout="wide")

# ======================
# HEADER
# ======================
st.title("🚀 Growth Radar AI - Smart Lead Intelligence System")
st.caption("AI-powered tool to analyze, score and prioritize business leads automatically.")

st.info("""
👋 Welcome!

Upload a CSV file with business data and get:
- Lead scoring
- Priority detection
- AI insights
- Downloadable report
""")

# ======================
# FILE UPLOAD
# ======================
uploaded_file = st.file_uploader("📂 Upload Business CSV File")

if uploaded_file is None:
    st.warning("Please upload a CSV file to start analysis.")

if uploaded_file is not None:

    # SAFE CSV READ (IMPORTANT FIX)
    df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))

    # ======================
    # SCORING ENGINE
    # ======================
    df["score"] = df.apply(calculate_score, axis=1)
    df["recommendation"] = df["score"].apply(get_recommendation)

    df = df.sort_values(by="score")

    # ======================
    # 📊 METRICS
    # ======================
    st.subheader("📊 Quick Stats")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Leads", len(df))
    col2.metric("High Priority", len(df[df["recommendation"] == "High Priority Lead"]))
    col3.metric("Best Score", df["score"].max())

    st.divider()

    # ======================
    # 📋 DASHBOARD
    # ======================
    st.subheader("📋 Leads Dashboard")

    st.dataframe(df[["name", "score", "recommendation"]])

    # ======================
    # ⬇ DOWNLOAD REPORT
    # ======================
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "⬇ Download Report CSV",
        csv,
        "lead_report.csv",
        "text/csv"
    )

    st.divider()

    # ======================
    # 🏆 BEST LEAD
    # ======================
    st.subheader("🏆 Best Lead")

    best = df.iloc[0]

    st.success(f"{best['name']} | Score: {best['score']} | {best['recommendation']}")

    # ======================
    # 🧠 AI INSIGHT
    # ======================
    st.subheader("🧠 AI Insight")

    if best["score"] > 80:
        st.info("Strong digital presence detected. High conversion potential.")
    elif best["score"] > 50:
        st.warning("Medium opportunity. Needs marketing improvement.")
    else:
        st.error("Weak online presence. Easy outreach target.")

    st.divider()

    # ======================
    # 📈 BAR CHART
    # ======================
    st.subheader("📊 Lead Score Chart")

    fig, ax = plt.subplots()
    ax.bar(df["name"], df["score"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ======================
    # 🥧 PIE CHART
    # ======================
    st.subheader("🥧 Lead Distribution")

    lead_counts = df["recommendation"].value_counts()

    fig2, ax2 = plt.subplots()
    ax2.pie(lead_counts, labels=lead_counts.index, autopct='%1.1f%%')

    st.pyplot(fig2)
    # =========================
# 🟡 TOOL #2 - TREND RADAR
# =========================

st.header("📈 Trend Radar AI (Beta)")

if st.button("Analyze Trends"):

    from trend_radar.analyzer import analyze_trends, get_top_trend

    df_trends = analyze_trends("trend_radar/trends_data.csv")

    st.subheader("📊 Trend Dashboard")
    st.dataframe(df_trends)

    st.subheader("🔥 Top Trend")

    top = get_top_trend(df_trends)

    st.success(f"{top['keyword']} | Score: {top['trend_score']}")

    st.info("💡 Create content around this topic for maximum reach!")

    st.bar_chart(df_trends.set_index("keyword")["trend_score"])