import sqlite3
from datetime import datetime

import streamlit as st
import pandas as pd

from auth.session import (
    require_auth,
    current_user
)

from crm.engine import load_crm

from proposal_generator.generator import generate_proposal
from proposal_generator.pdf import generate_pdf


DB_NAME = "growthradar.db"


def mark_proposal_generated(business_id):

    user = current_user()

    if not user:

        return False

    user_email = user.get("email")

    if not user_email:

        return False

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            UPDATE crm

            SET
                proposal_generated = 1,
                proposal_generated_at = ?

            WHERE business_id=?
            AND user_email=?
            """,
            (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                business_id,
                user_email
            )
        )

        conn.commit()

        updated = cursor.rowcount > 0

    except Exception:

        updated = False

    finally:

        conn.close()

    return updated


def show():

    require_auth()

    st.title(
        "📊 Reports & Business Intelligence"
    )

    st.caption(
        "Turn your CRM data into actionable business insights."
    )

    st.divider()

    # ==========================================================
    # LOAD CRM
    # ==========================================================

    crm = load_crm()

    # ==========================================================
    # EMPTY STATE
    # ==========================================================

    if crm.empty:

        st.info(
            "No CRM data available yet."
        )

        st.caption(
            "Add businesses to CRM first to unlock Business Intelligence."
        )

        st.divider()

    else:

        # ======================================================
        # CLEAN DATA
        # ======================================================

        crm = crm.copy()

        if "estimated_value" in crm.columns:

            crm["estimated_value"] = pd.to_numeric(
                crm["estimated_value"],
                errors="coerce"
            ).fillna(0)

        else:

            crm["estimated_value"] = 0

        if "revenue" in crm.columns:

            crm["revenue"] = pd.to_numeric(
                crm["revenue"],
                errors="coerce"
            ).fillna(0)

        else:

            crm["revenue"] = 0

        if "status" not in crm.columns:

            crm["status"] = "New"

        if "priority" not in crm.columns:

            crm["priority"] = "Medium"

        if "proposal_generated" not in crm.columns:

            crm["proposal_generated"] = 0

        if "proposal_generated_at" not in crm.columns:

            crm["proposal_generated_at"] = ""

        # ======================================================
        # BUSINESS INTELLIGENCE
        # ======================================================

        st.subheader(
            "📈 Business Intelligence"
        )

        total_leads = len(crm)

        won = len(
            crm[
                crm["status"] == "Won"
            ]
        )

        lost = len(
            crm[
                crm["status"] == "Lost"
            ]
        )

        open_deals = (
            total_leads
            - won
            - lost
        )

        pipeline = int(
            crm["estimated_value"].sum()
        )

        revenue = int(
            crm["revenue"].sum()
        )

        proposals_generated = int(
            pd.to_numeric(
                crm["proposal_generated"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

        # ======================================================
        # MAIN METRICS
        # ======================================================

        c1, c2, c3, c4, c5, c6 = st.columns(6)

        c1.metric(
            "Total Leads",
            total_leads
        )

        c2.metric(
            "Open Deals",
            open_deals
        )

        c3.metric(
            "Won",
            won
        )

        c4.metric(
            "Pipeline",
            f"${pipeline:,}"
        )

        c5.metric(
            "Revenue",
            f"${revenue:,}"
        )

        c6.metric(
            "Proposals",
            proposals_generated
        )

        st.divider()

        # ======================================================
        # SALES PERFORMANCE
        # ======================================================

        st.subheader(
            "💰 Sales Performance"
        )

        if total_leads > 0:

            win_rate = round(
                (won / total_leads) * 100,
                1
            )

            average_deal = round(
                pipeline / total_leads
            )

        else:

            win_rate = 0
            average_deal = 0

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Win Rate",
            f"{win_rate}%"
        )

        c2.metric(
            "Average Deal",
            f"${average_deal:,}"
        )

        c3.metric(
            "Lost Deals",
            lost
        )

        st.divider()

        # ======================================================
        # PROPOSAL PERFORMANCE
        # ======================================================

        st.subheader(
            "📄 Proposal Performance"
        )

        proposal_rate = 0

        if total_leads > 0:

            proposal_rate = round(
                (
                    proposals_generated
                    / total_leads
                ) * 100,
                1
            )

        c1, c2 = st.columns(2)

        c1.metric(
            "Proposals Generated",
            proposals_generated
        )

        c2.metric(
            "Proposal Coverage",
            f"{proposal_rate}%"
        )

        st.divider()

        # ======================================================
        # STATUS ANALYSIS
        # ======================================================

        st.subheader(
            "📊 Lead Status"
        )

        status_order = [

            "New",
            "Contacted",
            "Meeting",
            "Proposal",
            "Won",
            "Lost"

        ]

        status_counts = (
            crm["status"]
            .value_counts()
            .reindex(
                status_order,
                fill_value=0
            )
        )

        st.bar_chart(
            status_counts
        )

        st.divider()

        # ======================================================
        # PIPELINE BY STATUS
        # ======================================================

        st.subheader(
            "💵 Pipeline by Status"
        )

        pipeline_by_status = (
            crm.groupby("status")[
                "estimated_value"
            ]
            .sum()
            .reindex(
                status_order,
                fill_value=0
            )
        )

        st.bar_chart(
            pipeline_by_status
        )

        st.divider()

        # ======================================================
        # REVENUE BY STATUS
        # ======================================================

        st.subheader(
            "💰 Revenue by Status"
        )

        revenue_by_status = (
            crm.groupby("status")[
                "revenue"
            ]
            .sum()
            .reindex(
                status_order,
                fill_value=0
            )
        )

        st.bar_chart(
            revenue_by_status
        )

        st.divider()

        # ======================================================
        # PRIORITY ANALYSIS
        # ======================================================

        st.subheader(
            "🔥 Priority Opportunities"
        )

        priority_order = [

            "High",
            "Medium",
            "Low"

        ]

        priority_counts = (
            crm["priority"]
            .value_counts()
            .reindex(
                priority_order,
                fill_value=0
            )
        )

        st.bar_chart(
            priority_counts
        )

        # ======================================================
        # HIGH VALUE OPPORTUNITIES
        # ======================================================

        st.subheader(
            "💎 Biggest Opportunities"
        )

        opportunity_columns = [

            "business_name",
            "industry",
            "status",
            "priority",
            "estimated_value",
            "revenue"

        ]

        opportunity_columns = [

            column
            for column in opportunity_columns
            if column in crm.columns

        ]

        opportunities = crm.sort_values(
            "estimated_value",
            ascending=False
        )

        if opportunity_columns:

            st.dataframe(
                opportunities[
                    opportunity_columns
                ].head(10),
                use_container_width=True
            )

        # ======================================================
        # PROPOSAL HISTORY
        # ======================================================

        st.divider()

        st.subheader(
            "📄 Proposal History"
        )

        proposal_history = crm[
            pd.to_numeric(
                crm["proposal_generated"],
                errors="coerce"
            )
            .fillna(0)
            == 1
        ].copy()

        if proposal_history.empty:

            st.info(
                "No proposals generated yet."
            )

        else:

            history_columns = [

                "business_name",
                "industry",
                "status",
                "estimated_value",
                "proposal_generated_at"

            ]

            history_columns = [

                column
                for column in history_columns
                if column in proposal_history.columns

            ]

            st.dataframe(
                proposal_history[
                    history_columns
                ],
                use_container_width=True
            )

        # ======================================================
        # FOLLOW UPS
        # ======================================================

        st.divider()

        st.subheader(
            "📅 Follow-up Intelligence"
        )

        if "followup_date" in crm.columns:

            followups = crm[
                crm["followup_date"]
                .fillna("")
                .astype(str)
                .str.strip()
                != ""
            ].copy()

        else:

            followups = pd.DataFrame()

        if followups.empty:

            st.success(
                "No follow-ups scheduled."
            )

        else:

            st.info(
                f"{len(followups)} lead(s) have scheduled follow-ups."
            )

            followup_columns = [

                "business_name",
                "status",
                "priority",
                "followup_date"

            ]

            followup_columns = [

                column
                for column in followup_columns
                if column in followups.columns

            ]

            st.dataframe(
                followups[
                    followup_columns
                ],
                use_container_width=True
            )

        # ======================================================
        # CRM TABLE
        # ======================================================

        st.divider()

        st.subheader(
            "📋 Complete CRM Data"
        )

        display_columns = [

            "business_name",
            "industry",
            "status",
            "priority",
            "estimated_value",
            "revenue",
            "assigned_to",
            "followup_date",
            "meeting_date",
            "deal_stage",
            "proposal_generated",
            "proposal_generated_at"

        ]

        available_columns = [

            column
            for column in display_columns
            if column in crm.columns

        ]

        if available_columns:

            st.dataframe(
                crm[
                    available_columns
                ],
                use_container_width=True
            )

    # ==========================================================
    # PROPOSAL GENERATOR
    # ==========================================================

    st.divider()

    st.subheader(
        "📄 Proposal Generator"
    )

    st.caption(
        "Generate a professional proposal directly from your CRM."
    )

    selected_record = None

    if not crm.empty:

        st.markdown(
            "### 🔗 Load Business From CRM"
        )

        crm_names = []

        for index, row in crm.iterrows():

            name = str(
                row.get(
                    "business_name",
                    ""
                )
            ).strip()

            if not name:

                name = (
                    f"Business #{row.get('business_id', index)}"
                )

            crm_names.append(

                f"{name} | ID: "
                f"{row.get('business_id', index)}"

            )

        selected_business = st.selectbox(

            "Select CRM Business",

            [
                "➕ Create New Proposal"
            ] + crm_names

        )

        if selected_business != "➕ Create New Proposal":

            selected_index = crm_names.index(
                selected_business
            )

            selected_record = crm.iloc[
                selected_index
            ]

            st.success(
                "Business loaded from CRM ✅"
            )

    st.divider()

    # ==========================================================
    # PROPOSAL FORM
    # ==========================================================

    with st.form(
        "proposal_form"
    ):

        st.markdown(
            "### 🏢 Business Information"
        )

        if selected_record is not None:

            default_business = str(
                selected_record.get(
                    "business_name",
                    ""
                )
            )

            default_industry = str(
                selected_record.get(
                    "industry",
                    ""
                )
            )

            default_website = str(
                selected_record.get(
                    "website",
                    ""
                )
            )

            default_location = str(
                selected_record.get(
                    "location",
                    ""
                )
            )

            try:

                default_value = int(
                    selected_record.get(
                        "estimated_value",
                        1000
                    )
                    or 1000
                )

            except Exception:

                default_value = 1000

        else:

            default_business = ""
            default_industry = ""
            default_website = ""
            default_location = ""
            default_value = 1000

        col1, col2 = st.columns(2)

        with col1:

            business = st.text_input(
                "Business Name",
                value=default_business
            )

            industry = st.text_input(
                "Industry",
                value=default_industry
            )

        with col2:

            website = st.text_input(
                "Website",
                value=default_website
            )

            location = st.text_input(
                "Location",
                value=default_location
            )

        project_value = st.number_input(

            "Estimated Project Value ($)",

            min_value=100,

            value=max(
                100,
                default_value
            ),

            step=100

        )

        services = st.multiselect(

            "Recommended Services",

            [

                "Meta Ads",
                "Google Ads",
                "SEO",
                "Website Development",
                "Landing Page",
                "Social Media Management",
                "Video Editing",
                "Graphic Design",
                "Branding",
                "AI Automation",
                "CRM Automation",
                "Lead Generation",
                "Website Intelligence",
                "Social Intelligence"

            ]

        )

        submit = st.form_submit_button(

            "🚀 Generate Professional Proposal",

            use_container_width=True

        )

    # ==========================================================
    # STOP
    # ==========================================================

    if not submit:

        return

    # ==========================================================
    # VALIDATION
    # ==========================================================

    if not business.strip():

        st.warning(
            "Please enter Business Name."
        )

        return

    if not services:

        st.warning(
            "Please select at least one service."
        )

        return

    # ==========================================================
    # LEAD SCORE
    # ==========================================================

    lead_score = 90

    if selected_record is not None:

        try:

            lead_score = int(
                selected_record.get(
                    "lead_score",
                    90
                )
            )

        except Exception:

            lead_score = 90

    # ==========================================================
    # BUSINESS DATA
    # ==========================================================

    business_data = {

        "name": business,

        "lead_score": lead_score,

        "website": website,

        "email": (

            selected_record.get(
                "email",
                "Not Available"
            )

            if selected_record is not None

            else "Not Available"

        ),

        "phone": (

            selected_record.get(
                "phone",
                "Not Available"
            )

            if selected_record is not None

            else "Not Available"

        )

    }

    # ==========================================================
    # GENERATE PROPOSAL
    # ==========================================================

    with st.spinner(
        "🤖 Generating professional proposal..."
    ):

        proposal = generate_proposal(

            business_data,

            services,

            project_value

        )

    # ==========================================================
    # MARK CRM PROPOSAL GENERATED
    # ==========================================================

    if selected_record is not None:

        business_id = selected_record.get(
            "business_id"
        )

        tracking_result = mark_proposal_generated(
            business_id
        )

        if tracking_result:

            st.success(
                "Proposal Generated & CRM Updated ✅"
            )

        else:

            st.warning(
                "Proposal generated, but CRM tracking could not be updated."
            )

    else:

        st.success(
            "Proposal Generated Successfully ✅"
        )

    st.divider()

    # ==========================================================
    # PREVIEW
    # ==========================================================

    st.subheader(
        "📄 Proposal Preview"
    )

    st.text_area(

        "Generated Proposal",

        proposal,

        height=550

    )

    st.divider()

    # ==========================================================
    # PDF
    # ==========================================================

    st.subheader(
        "📥 Export Proposal"
    )

    with st.spinner(
        "Preparing PDF..."
    ):

        pdf = generate_pdf(
            proposal
        )

    safe_name = (

        business
        .strip()
        .replace(" ", "_")

    )

    filename = (
        f"{safe_name}_Proposal.pdf"
    )

    st.download_button(

        "📄 Download Proposal PDF",

        data=pdf,

        file_name=filename,

        mime="application/pdf",

        use_container_width=True

    )

    st.success(
        "Your proposal is ready to send to the client. 🚀"
    )