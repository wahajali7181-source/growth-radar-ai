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
    layout="wide"
)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.stApp {
    background-color: #0f172a;
}

h1,h2,h3 {
    color: white !important;
}

p,label,div {
    color: white !important;
}

[data-testid="stMetric"] {
    background: #1e293b;
    padding: 15px;
    border-radius: 15px;
}

.stButton>button {
    background: linear-gradient(
        90deg,
        #3b82f6,
        #8b5cf6
    );

    color: white;
    border: none;
    border-radius: 12px;
    font-weight: bold;
}

.stDownloadButton>button {
    background: linear-gradient(
        90deg,
        #10b981,
        #14b8a6
    );

    color: white;
    border: none;
    border-radius: 12px;
}
.stDataFrame {
    border-radius: 15px;
}

.stTextInput > div > div > input {
    border-radius: 12px;
    background-color: #1e293b;
    color: white;
}

.stFileUploader {
    background-color: #1e293b;
    padding: 10px;
    border-radius: 15px;
}

.stAlert {
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)
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
# QUICK LEAD FINDER
# =========================
st.subheader("🔍 Quick Lead Finder")

business_type = st.text_input(
    "Business Type",
    placeholder="Dentist, Gym, Restaurant"
)

city = st.text_input(
    "City",
    placeholder="Lahore"
)

if st.button("Find Businesses"):

    if business_type and city:

        df_businesses = find_businesses(
            business_type,
            city
        )

        if len(df_businesses) > 0:

            st.success(
                f"Found {len(df_businesses)} results"
            )

         # =========================
# REAL LEAD SCORE
# =========================

        lead_scores = []
        opportunities = []

        for _, business in df_businesses.iterrows():

            score = calculate_lead_score(
             business
    )

            level = opportunity_level(
            score
    )

            lead_scores.append(score)

            opportunities.append(level)

        df_businesses["lead_score"] = lead_scores

        df_businesses["opportunity"] = opportunities

        df_businesses = df_businesses.sort_values(
             by="lead_score",
            ascending=False
        )
          
            

        st.subheader("📋 Found Businesses")

        st.dataframe(
                df_businesses,
                use_container_width=True
            )
            

            # Best Lead
        best = df_businesses.iloc[0]

        st.subheader("🏆 Best Opportunity")

        st.success(
                f"{best['name']} | Lead Score: {best['lead_score']} | {best['opportunity']}"
            )

            # Outreach Message
        outreach = f'''
Hi {best['name']},

I found your business while analyzing businesses in {city}.

I help companies improve their online visibility,
lead generation and customer acquisition.

Would you be interested in a quick discussion?

Best regards,
Wahaj Ali
'''

        st.subheader("✉ Outreach Message")

        st.text_area(
                "Copy & Send",
                outreach,
                height=220
            )

        st.subheader("🧠 AI Business Audit")

        audit = generate_audit(best)
            

        st.text_area(
                "Audit Report",
                audit,
                height=300
              )
        st.subheader("💡 AI Opportunity Recommendation")

        advice = get_business_advice(best)

        st.text_area(
    "Business Growth Plan",
    advice,
    height=220
)    
                
    else:

        st.warning(
                "No businesses found."
            )
else:

    st.warning(
            "Please enter Business Type and City."
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