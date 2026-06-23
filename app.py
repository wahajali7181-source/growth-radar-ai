import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

from business_finder.scorer import calculate_score, get_recommendation

# =========================
# TREND RADAR IMPORT
# =========================
try:
    from trend_radar.analyzer import analyze_trends, get_top_trend
    TREND_RADAR_AVAILABLE = True
except Exception:
    TREND_RADAR_AVAILABLE = False


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Growth Radar AI",
    layout="wide"
)


# =========================
# PDF GENERATOR
# =========================
def generate_pdf_report(df):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Growth Radar AI Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Total Leads: {len(df)}", styles["Normal"]))
    elements.append(Paragraph(f"Best Score: {df['score'].max()}", styles["Normal"]))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Top Leads", styles["Heading2"]))

    for _, row in df.head(5).iterrows():
        elements.append(
            Paragraph(
                f"{row['name']} | Score: {row['score']} | {row['recommendation']}",
                styles["Normal"]
            )
        )

    doc.build(elements)
    buffer.seek(0)
    return buffer


# =========================
# UI HEADER
# =========================
st.title("🚀 Growth Radar AI")
st.caption("AI Lead Finder + Trend Analyzer + SaaS Tool")

st.info("""
Upload CSV or analyze businesses instantly:

✔ Lead Scoring  
✔ AI Insights  
✔ Trend Radar  
✔ PDF Reports  
✔ Outreach Messages
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
    "sample.csv",
    "text/csv"
)


# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("📂 Upload Business CSV", type=["csv"])

if uploaded_file is None:
    st.warning("Upload CSV file to start analysis")

else:

    try:
        df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))

        # =========================
        # VALIDATION
        # =========================
        required_columns = ["name", "website", "instagram", "facebook", "google_reviews"]

        missing = [c for c in required_columns if c not in df.columns]

        if missing:
            st.error(f"Missing columns: {', '.join(missing)}")
            st.stop()

        # =========================
        # SCORING
        # =========================
        df["score"] = df.apply(calculate_score, axis=1)
        df["recommendation"] = df["score"].apply(get_recommendation)

        df = df.sort_values(by="score", ascending=False)

        # =========================
        # OVERVIEW
        # =========================
        st.subheader("📊 Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Leads", len(df))
        col2.metric("High Priority", len(df[df["recommendation"] == "High Priority Lead"]))
        col3.metric("Best Score", int(df["score"].max()))

        st.divider()

        # =========================
        # DASHBOARD
        # =========================
        st.subheader("📋 Leads Dashboard")

        # OUTREACH MESSAGE
        if st.button("Generate Outreach Message"):

            best = df.iloc[0]

            message = f"""
Hi {best['name']},

I noticed your business and analyzed your online presence.

Your current score is {best['score']} and category is:
{best['recommendation']}

We help businesses improve visibility and generate more leads.

Would you be open to a quick discussion?

Best regards,
Growth Radar AI
"""

            st.text_area("AI Outreach Message", message, height=250)

        st.dataframe(df)

        # =========================
        # DOWNLOAD CSV
        # =========================
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button("⬇ Download Report", csv, "report.csv", "text/csv")

        # =========================
        # DOWNLOAD PDF
        # =========================
        pdf_file = generate_pdf_report(df)

        st.download_button(
            "📄 Download PDF Report",
            pdf_file,
            "report.pdf",
            "application/pdf"
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

        st.divider()

        # =========================
        # TREND RADAR
        # =========================
        st.header("📈 Trend Radar AI")

        if TREND_RADAR_AVAILABLE:

            if st.button("Analyze Trends"):

                df_trends = analyze_trends("trend_radar/trends_data.csv")

                st.dataframe(df_trends)

                top = get_top_trend(df_trends)

                st.success(
                    f"Top Trend: {top['keyword']} | Score: {top['trend_score']:.1f}"
                )

                st.bar_chart(df_trends.set_index("keyword")["trend_score"])

        else:
            st.warning("Trend Radar not available")

    except Exception as e:
        st.error(f"Error: {str(e)}")