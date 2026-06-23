import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from business_finder.scorer import calculate_score, get_recommendation

st.set_page_config(page_title="Growth Radar AI", layout="wide")

st.title("🚀 Growth Radar AI")
st.write("Upload a business CSV file to analyze leads automatically.")

# Upload file
uploaded_file = st.file_uploader("📂 Upload Business CSV")

if uploaded_file is not None:

    # Read data
    df = pd.read_csv(uploaded_file)

    # Scoring
    df["score"] = df.apply(calculate_score, axis=1)
    df["recommendation"] = df["score"].apply(get_recommendation)

    # Sort
    df = df.sort_values(by="score")

    # ======================
    # 📊 QUICK STATS
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
        st.info("This is a very strong lead. High online presence detected.")
    elif best["score"] > 50:
        st.warning("Medium opportunity. Needs marketing improvement.")
    else:
        st.error("Weak digital presence. Easy target for outreach.")

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