import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

from business_finder.scorer import calculate_score, get_recommendation

# Safe Trend Radar import
try:
    from trend_radar.analyzer import analyze_trends, get_top_trend
    TREND_RADAR_AVAILABLE = True
except Exception:
    TREND_RADAR_AVAILABLE = False

st.set_page_config(
    page_title="Growth Radar AI",
    layout="wide"
)

# =========================
# HEADER
# =========================

st.title("🚀 Growth Radar AI")
st.caption("AI Lead Finder & Business Intelligence Tool")

st.info("""
Upload a business CSV file and get:
- Lead scoring
- Priority ranking
- AI insights
- Trend analysis
""")

# =========================
# SAMPLE CSV
# =========================

sample_csv = """name,website,instagram,facebook,google_reviews
Business A,yes,yes,no,120
Business B,no,yes,yes,50
Business C,yes,no,no,10
"""

st.download_button(
    "📥 Download Sample CSV",
    sample_csv,
    "sample_businesses.csv",
    "text/csv"
)

# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "📂 Upload Business CSV File",
    type=["csv"]
)

if uploaded_file is None:
    st.warning("Please upload a CSV file to start analysis.")

else:

    try:

        df = pd.read_csv(
            io.StringIO(
                uploaded_file.getvalue().decode("utf-8")
            )
        )

        # =========================
        # VALIDATION
        # =========================

        required_columns = [
            "name",
            "website",
            "instagram",
            "facebook",
            "google_reviews"
        ]

        missing = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing:
            st.error(
                f"Missing columns: {', '.join(missing)}"
            )
            st.stop()

        # =========================
        # LEAD SCORING
        # =========================

        df["score"] = df.apply(
            calculate_score,
            axis=1
        )

        df["recommendation"] = df["score"].apply(
            get_recommendation
        )

        df = df.sort_values(
            by="score",
            ascending=False
        )

        # =========================
        # STATS
        # =========================

        st.subheader("📊 Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Leads",
            len(df)
        )

        col2.metric(
            "High Priority",
            len(
                df[
                    df["recommendation"]
                    == "High Priority Lead"
                ]
            )
        )

        col3.metric(
            "Best Score",
            int(df["score"].max())
        )

        st.divider()

        # =========================
        # DASHBOARD
        # =========================

        st.subheader("📋 Leads Dashboard")

        st.dataframe(df)

        # =========================
        # DOWNLOAD REPORT
        # =========================

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

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

        st.success(
            f"{best['name']} | "
            f"Score: {best['score']} | "
            f"{best['recommendation']}"
        )

        # =========================
        # AI INSIGHT
        # =========================

        st.subheader("🧠 AI Insight")

        if best["score"] > 80:
            st.info(
                "Strong digital presence - High conversion potential"
            )

        elif best["score"] > 50:
            st.warning(
                "Medium opportunity - Needs improvement"
            )

        else:
            st.error(
                "Low presence - Easy outreach target"
            )

        st.divider()

        # =========================
        # SCORE CHART
        # =========================

        st.subheader("📊 Score Chart")

        fig, ax = plt.subplots()

        ax.bar(
            df["name"],
            df["score"]
        )

        plt.xticks(rotation=45)

        st.pyplot(fig)

        st.divider()

        # =========================
        # TREND RADAR AI
        # =========================

        st.header("📈 Trend Radar AI")

        if TREND_RADAR_AVAILABLE:

            if st.button("Analyze Trends"):

                df_trends = analyze_trends(
                    "trend_radar/trends_data.csv"
                )

                st.subheader(
                    "🔥 Trending Topics"
                )

                st.dataframe(
                    df_trends
                )

                top = get_top_trend(
                    df_trends
                )

                st.success(
                    f"Top Trend: "
                    f"{top['keyword']} "
                    f"(Score: {top['trend_score']:.1f})"
                )

                st.bar_chart(
                    df_trends.set_index(
                        "keyword"
                    )["trend_score"]
                )

        else:

            st.warning(
                "Trend Radar module not available."
            )

    except Exception as e:

        st.error(
            f"Error processing file: {str(e)}"
        )