import streamlit as st

from auth.session import (
    require_auth,
    current_user
)

from subscriptions.engine import (
    get_remaining,
    needs_upgrade
)

from subscriptions.usage import (
    increase_usage
)

from website_scanner.engine import analyze_website
from website_scanner.advisor import generate_ai_summary
from website_reports.report_builder import build_report
from website_reports.pdf_generator import generate_pdf


def show():

    # ===================================
    # AUTH
    # ===================================

    require_auth()

    user = current_user()

    email = user["email"]

    # ===================================
    # PAGE
    # ===================================

    st.title("🌐 Website Intelligence")

    st.caption(
        "Complete Website Audit & AI Analysis"
    )

    st.divider()

    # ===================================
    # SUBSCRIPTION
    # ===================================

    remaining = get_remaining(

        email,

        "website_scanner"

    )

    col1, col2 = st.columns([3, 1])

    with col1:

        st.info(

            f"Remaining Website Scans : {remaining}"

        )

    with col2:

        st.button(

            "⭐ Upgrade",

            width="stretch"

        )

    st.divider()

    # ===================================
    # INPUT
    # ===================================

    website = st.text_input(

        "Website URL",

        placeholder="https://example.com"

    )

    st.divider()

    # ===================================
    # BUTTON
    # ===================================

    if st.button(

        "🚀 Analyze Website",

        width="stretch"

    ):

        if not website:

            st.warning(

                "Please enter a website."

            )

            return

        # ===============================
        # SUBSCRIPTION LIMIT
        # ===============================

        if needs_upgrade(

            email,

            "website_scanner"

        ):

            st.error(

                "⭐ Monthly Website Scan limit reached."

            )

            st.warning(

                "Upgrade your plan."

            )

            st.button(

                "🚀 Upgrade Plan",

                width="stretch"

            )

            return

        if not website.startswith(("http://", "https://")):

            website = "https://" + website

        # ===============================
        # SCAN
        # ===============================

        with st.spinner(

            "Scanning Website..."

        ):

            report = analyze_website(

                website

            )

            ai = generate_ai_summary(

                report

            )
        pdf_report = build_report(

            report,

            ai

)

        pdf_file = generate_pdf(

            pdf_report,

            "website_report.pdf"

)
    
        # ===============================
        # USAGE +1
        # ===============================

        increase_usage(

            email,

            "website_scanner"

        )

        st.success(

            "Website analysis completed."

        )

        st.divider()

        # ===================================
        # OVERVIEW
        # ===================================

        c1, c2, c3 = st.columns(3)

        c1.metric(

            "Overall Score",

            f"{report['overall_score']}%"

        )

        c2.metric(

            "Grade",

            ai["grade"]

        )

        c3.metric(

            "Priority",

            ai["priority"]

        )

        st.divider()

        # ===================================
        # SCORES
        # ===================================

        st.subheader("📊 Website Scores")

        for icon, name, key in [

            ("❤️", "Health", "health"),

            ("🔍", "SEO", "seo"),

            ("🛡", "Security", "security"),

            ("⚡", "Performance", "performance")

        ]:

            st.write(f"{icon} {name}")

            st.progress(

                report[key]["score"] / 100

            )

            st.caption(

                f"{report[key]['score']}%"

            )

        st.divider()

        # ===================================
        # TECHNOLOGY
        # ===================================

        st.subheader("🛠 Technology Stack")

        if report["technologies"]:

            cols = st.columns(3)

            for i, tech in enumerate(

                report["technologies"]

            ):

                cols[i % 3].success(

                    f"✅ {tech}"

                )

        else:

            st.info(

                "No technologies detected."

            )

        st.divider()

        # ===================================
        # AI SUMMARY
        # ===================================

        st.subheader(

            "🧠 AI Executive Summary"

        )

        st.info(

            ai["summary"]

        )

        st.divider()

        # ===================================
        # RECOMMENDATIONS
        # ===================================

        st.subheader(

            "📋 Improvement Recommendations"

        )

        sections = {

            "❤️ Health": report["health"],

            "🔍 SEO": report["seo"],

            "🛡 Security": report["security"],

            "⚡ Performance": report["performance"]

        }

        for title, section in sections.items():

            with st.expander(

                title,

                expanded=False

            ):

                if section["recommendations"]:

                    for item in section["recommendations"]:

                        st.write(

                            f"• {item}"

                        )

                else:

                    st.success(

                        "No issues found."

                    )
        st.subheader("📄 Export Report")

        with open(

            pdf_file,

            "rb"

        ) as file:

            st.download_button(

                "⬇ Download PDF Report",

                data=file,

                file_name="GrowthRadar_Website_Report.pdf",

                mime="application/pdf",

                use_container_width=True

    )            