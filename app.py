import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from business_finder.scorer import calculate_score, get_recommendation
from local_business_finder.finder import find_businesses

from auth.login import login_user, register_user
from lead_score.engine import calculate_lead_score, opportunity_level
from business_ai.advisor import get_business_advice
from app_config import FREE_MODE
from digital_presence.engine import calculate_presence_score
from proposal_generator.generator import generate_proposal
from dashboard.metrics import get_dashboard_metrics
from dashboard.ui import show_dashboard_cards
from dashboard.insights import generate_dashboard_insights
from website_scanner.report import generate_report
from dashboard.charts import show_lead_score_chart
from ui.theme import apply_theme
from website_scanner.health import calculate_health_score
from ui.sidebar import show_sidebar
from ai_engine.recommendation_engine import generate_ai_actions

from ui.website_cards import (
    show_overview_card,
    show_seo_card,
    show_security_card
)


from business_intelligence.engine import (
    estimate_project_value,
    recommend_services
)
from pages.dashboard import show as dashboard_page
from pages.lead_finder import show as lead_finder_page
from pages.reports import show as reports_page
from pages.ai_consultant import show as ai_consultant_page
from pages.website_intelligence import show as website_page
from pages.social_intelligence import show as social_page
from pages.trend_intelligence import show as trend_page
from lead_engine.database import create_tables
def generate_audit(business):

    score = business["lead_score"]

    if score >= 80:

        audit = """
✅ Strong Business Presence

Website: Good
Reputation: Strong
Growth Opportunity: Medium

Recommended Services:
• Meta Ads
• Video Marketing

Potential:
20-50 Leads / Month
"""

    elif score >= 50:

        audit = """
⚠ Moderate Online Presence

Website: Average
Reputation: Average
Growth Opportunity: High

Recommended Services:
• Meta Ads
• Google Ads
• SEO

Potential:
30-70 Leads / Month
"""

    else:

        audit = """
🚀 High Growth Opportunity

Website: Weak
Reputation: Low
Growth Opportunity: Very High

Recommended Services:
• Full Digital Marketing
• Meta Ads
• SEO
• Video Marketing

Potential:
50-100 Leads / Month
"""

    return audit
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
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)
create_tables()
apply_theme()
page = show_sidebar()
if page == "🏠 Dashboard":
    dashboard_page()
    st.stop()

elif page == "🔍 Business Finder":
    lead_finder_page()
    st.stop()

elif page == "🌐 Website Intelligence":
    website_page()
    st.stop()

elif page == "📱 Social Intelligence":
    social_page()
    st.stop()

elif page == "📈 Trend Intelligence":
    trend_page()
    st.stop()

elif page == "📄 Reports":
    reports_page()
    st.stop()

elif page == "⚙ Settings":
    from pages.settings import show
    show()
    st.stop()
st.title("🚀 Growth Radar AI")

st.caption(
    "AI Powered Business Intelligence Platform"
)



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# PDF REPORT
# =========================
def generate_pdf_report(df):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Growth Radar AI Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Total Leads: {len(df)}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Best Score: {df['score'].max()}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            "Top Leads",
            styles["Heading2"]
        )
    )

    for _, row in df.head(5).iterrows():

        elements.append(
          Paragraph(
    str(row.to_dict()),
    styles["Normal"]
)
        )

    doc.build(elements)

    buffer.seek(0)

    return buffer

if not st.session_state.logged_in:

    st.title("🔐 Growth Radar AI Login")

    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if login_user(email, password):

                st.session_state.logged_in = True

                st.success("Login Successful")

                st.rerun()

            else:

                st.error("Invalid Email or Password")

    with tab2:

        new_email = st.text_input(
            "New Email"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        if st.button("Create Account"):

            if register_user(
                new_email,
                new_password
            ):

                st.success(
                    "Account Created Successfully"
                )

            else:

                st.warning(
                    "Email already exists"
                )

    st.stop()
    # =========================
# NAVIGATION
# =========================

    page = st.sidebar.radio(
        "📂 Navigation",
    [
            "Dashboard",
            "Lead Finder",
            "Reports",
            "AI Consultant"
    ]
)
# =========================
# HEADER
# =========================
st.markdown("""
<div style="
background: linear-gradient(135deg,#2563eb,#7c3aed);
padding:35px;
border-radius:20px;
text-align:center;
margin-bottom:20px;
box-shadow:0px 10px 30px rgba(0,0,0,0.3);
">

<h1 style="color:white;">
🚀 Growth Radar AI
</h1>

<h3 style="color:white;">
Find Leads • Analyze Trends • Generate Outreach
</h3>

<p style="color:white;">
Built for Agencies, Freelancers & Growth Teams
</p>

</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style="
display:flex;
gap:15px;
margin-bottom:20px;
">

<div style="
background:#1e293b;
padding:20px;
border-radius:15px;
flex:1;
text-align:center;
">
<h3>🔍 Lead Finder</h3>
<p>Find local businesses instantly</p>
</div>

<div style="
background:#1e293b;
padding:20px;
border-radius:15px;
flex:1;
text-align:center;
">
<h3>📈 Trend Radar</h3>
<p>Analyze Google Trends data</p>
</div>

<div style="
background:#1e293b;
padding:20px;
border-radius:15px;
flex:1;
text-align:center;
">
<h3>📄 AI Reports</h3>
<p>Generate PDF reports automatically</p>
</div>

</div>
""", unsafe_allow_html=True)
st.caption(
    "AI Lead Finder + Trend Analyzer + SaaS Tool"
)

st.info("""
✔ Lead Scoring

✔ AI Insights

✔ Trend Radar

✔ PDF Reports

✔ Outreach Messages
""")

# =========================
# LOGOUT
# =========================

col1, col2 = st.columns([8, 1])

with col2:

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.rerun()
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
# CSV UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "📂 Upload Business CSV",
    type=["csv"]
)

if uploaded_file is None:

    st.warning(
        "Upload CSV file to start analysis"
    )

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
            c for c in required_columns
            if c not in df.columns
        ]

        if missing:

            st.error(
                f"Missing columns: {', '.join(missing)}"
            )

            st.stop()

        # =========================
        # SCORING
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
        # OVERVIEW
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
        # LEADS DASHBOARD
        # =========================
        st.subheader("📋 Leads Dashboard")

        st.dataframe(
            df,
            use_container_width=True
        )

        # =========================
        # OUTREACH
        # =========================
        if st.button(
            "Generate Outreach Message"
        ):

            best = df.iloc[0]

            message = f"""
Hi {best['name']},

I analyzed your online presence.

Your current lead score is {best['score']}.

Category:
{best['recommendation']}

We help businesses improve visibility and generate more leads.

Would you be open to a quick discussion?

Best regards,
Growth Radar AI
"""

            st.text_area(
                "AI Outreach Message",
                message,
                height=250
            )

        # =========================
        # DOWNLOAD CSV
        # =========================
        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇ Download CSV Report",
            csv,
            "report.csv",
            "text/csv"
        )

        # =========================
        # DOWNLOAD PDF
        # =========================
        pdf_file = generate_pdf_report(
            df
        )

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

        st.success(
            f"{best['name']} | Score: {best['score']} | {best['recommendation']}"
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
                "Low presence - Easy target"
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
        # TREND RADAR
        # =========================
        st.header("📈 Trend Radar AI")

        trend_keyword = st.text_input(
            "Enter Trend Keyword",
            placeholder="AI, Crypto, Fitness, Real Estate"
        )

        if TREND_RADAR_AVAILABLE:

            if st.button(
                "Analyze Trends"
            ):

                if not trend_keyword:

                    st.warning(
                        "Please enter a keyword."
                    )

                else:

                    df_trends = analyze_trends(
                        trend_keyword
                    )

                    if df_trends.empty:

                        st.warning(
                            "No trend data found."
                        )

                    else:

                        st.dataframe(
                            df_trends
                        )

                        top = get_top_trend(
                            df_trends
                        )

                        st.success(
                            f"Peak Trend Score: {top['trend_score']}"
                        )

                        st.line_chart(
                            df_trends.set_index(
                                "date"
                            )["trend_score"]
                        )

        else:

            st.warning(
                "Trend Radar module not available."
            )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )
        st.divider()

st.divider()

st.markdown("""
<center>

<h4>
🚀 Growth Radar AI © 2026
</h4>

<p>
Developed by <b>Wahaj Ali</b>
</p>

</center>
""", unsafe_allow_html=True)