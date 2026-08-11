from io import BytesIO

import streamlit as st
import pandas as pd

from auth.session import require_auth
from crm.engine import (
    load_crm,
    mark_proposal_sent,
)

from proposal_generator.generator import generate_proposal
from proposal_generator.pdf import generate_pdf


def show():

    require_auth()

    st.title("📊 Reports Dashboard")

    st.caption(
        "Business Analytics, Performance & Proposal Intelligence"
    )

    st.divider()

    # ==========================================================
    # LOAD CRM
    # ==========================================================

    df = load_crm()

    # ==========================================================
    # EMPTY STATE
    # ==========================================================

    if df.empty:

        st.info(
            "No CRM Data Available"
        )

        st.caption(
            "Add businesses to CRM first to unlock reports and proposal generation."
        )

        return

    # ==========================================================
    # CLEAN DATA
    # ==========================================================

    df = df.copy()

    if "estimated_value" not in df.columns:
        df["estimated_value"] = 0

    if "revenue" not in df.columns:
        df["revenue"] = 0

    if "status" not in df.columns:
        df["status"] = "New"

    if "proposal_sent" not in df.columns:
        df["proposal_sent"] = 0

    if "priority" not in df.columns:
        df["priority"] = "Medium"

    if "industry" not in df.columns:
        df["industry"] = ""

    if "business_name" not in df.columns:
        df["business_name"] = ""

    if "website" not in df.columns:
        df["website"] = ""

    if "location" not in df.columns:
        df["location"] = ""

    if "email" not in df.columns:
        df["email"] = ""

    if "phone" not in df.columns:
        df["phone"] = ""

    if "lead_score" not in df.columns:
        df["lead_score"] = 0

    df["estimated_value"] = pd.to_numeric(
        df["estimated_value"],
        errors="coerce"
    ).fillna(0)

    df["revenue"] = pd.to_numeric(
        df["revenue"],
        errors="coerce"
    ).fillna(0)

    df["proposal_sent"] = pd.to_numeric(
        df["proposal_sent"],
        errors="coerce"
    ).fillna(0)

    # ==========================================================
    # MAIN METRICS
    # ==========================================================

    total = len(df)

    won = len(
        df[df["status"] == "Won"]
    )

    proposal_count = len(
        df[df["proposal_sent"] == 1]
    )

    pipeline_value = int(
        df["estimated_value"].sum()
    )

    won_revenue = int(
        df.loc[
            df["status"] == "Won",
            "estimated_value"
        ].sum()
    )

    revenue = int(
        df["revenue"].sum()
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total Leads",
        total
    )

    c2.metric(
        "Won Deals",
        won
    )

    c3.metric(
        "Proposal Sent",
        proposal_count
    )

    c4.metric(
        "Pipeline Value",
        f"${pipeline_value:,}"
    )

    c5.metric(
        "Won Revenue",
        f"${won_revenue:,}"
    )

    st.divider()

    # ==========================================================
    # CRM DATA
    # ==========================================================

    st.subheader("📋 CRM Data")

    display_columns = [

        "business_id",
        "business_name",
        "industry",
        "lead_score",
        "status",
        "priority",
        "estimated_value",
        "revenue",
        "proposal_sent",
        "followup_date",
        "deal_stage"

    ]

    available_columns = [

        column
        for column in display_columns
        if column in df.columns

    ]

    if available_columns:

        st.dataframe(

            df[available_columns],

            use_container_width=True,

            hide_index=True

        )

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ==========================================================
    # LEAD STATUS DISTRIBUTION
    # ==========================================================

    st.subheader(
        "📊 Lead Status Distribution"
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

        df["status"]
        .fillna("Unknown")
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

    # ==========================================================
    # ESTIMATED REVENUE BY STATUS
    # ==========================================================

    st.subheader(
        "💰 Estimated Revenue by Status"
    )

    revenue_by_status = (

        df.groupby("status")[
            "estimated_value"
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

    # ==========================================================
    # PRIORITY DISTRIBUTION
    # ==========================================================

    st.subheader(
        "⭐ Priority Distribution"
    )

    priority_order = [

        "High",
        "Medium",
        "Low"

    ]

    priority_counts = (

        df["priority"]
        .fillna("Unknown")
        .value_counts()
        .reindex(
            priority_order,
            fill_value=0
        )

    )

    st.bar_chart(
        priority_counts
    )

    st.divider()

    # ==========================================================
    # CONVERSION FUNNEL
    # ==========================================================

    st.subheader(
        "🎯 Conversion Funnel"
    )

    funnel_data = pd.DataFrame(

        {
            "Stage": [

                "New",
                "Contacted",
                "Meeting",
                "Proposal",
                "Won"

            ],

            "Leads": [

                len(
                    df[df["status"] == "New"]
                ),

                len(
                    df[df["status"] == "Contacted"]
                ),

                len(
                    df[df["status"] == "Meeting"]
                ),

                len(
                    df[df["status"] == "Proposal"]
                ),

                len(
                    df[df["status"] == "Won"]
                )

            ]

        }

    )

    st.bar_chart(
        funnel_data.set_index("Stage")
    )

    st.divider()

    # ==========================================================
    # TOP INDUSTRIES
    # ==========================================================

    st.subheader(
        "🏆 Top Industries"
    )

    if "industry" in df.columns:

        industry_counts = (

            df["industry"]
            .fillna("Unknown")
            .replace("", "Unknown")
            .value_counts()
            .head(10)

        )

        st.bar_chart(
            industry_counts
        )

    else:

        st.info(
            "Industry data is not available."
        )

    st.divider()

    # ==========================================================
    # REVENUE
    # ==========================================================

    st.subheader(
        "💰 Revenue Overview"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Estimated Pipeline",
        f"${pipeline_value:,}"
    )

    c2.metric(
        "Won Revenue",
        f"${won_revenue:,}"
    )

    c3.metric(
        "Recorded Revenue",
        f"${revenue:,}"
    )

    st.divider()

    # ==========================================================
    # EXPORT REPORT
    # ==========================================================

    st.subheader(
        "📥 Export Reports"
    )

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(

            writer,

            index=False,

            sheet_name="CRM Report"

        )

        funnel_data.to_excel(

            writer,

            index=False,

            sheet_name="Conversion Funnel"

        )

        revenue_by_status.to_frame(
            name="Estimated Value"
        ).to_excel(

            writer,

            sheet_name="Revenue by Status"

        )

    excel_data = buffer.getvalue()

    st.download_button(

        "📊 Download Excel Report",

        data=excel_data,

        file_name="GrowthRadar_CRM_Report.xlsx",

        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),

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
        "Select a CRM business and generate a professional proposal."
    )

    # ==========================================================
    # SELECT BUSINESS
    # ==========================================================

    business_options = []

    for index, row in df.iterrows():

        business_name = str(
            row.get(
                "business_name",
                ""
            )
        ).strip()

        if not business_name:

            business_name = (
                f"Business #{row.get('business_id', index)}"
            )

        business_id = row.get(
            "business_id",
            index
        )

        business_options.append(

            f"{business_name} | ID: {business_id}"

        )

    selected_option = st.selectbox(

        "🔗 Select CRM Business",

        [

            "➕ Create New Proposal"

        ] + business_options,

        key="reports_proposal_business"

    )

    selected_record = None

    if selected_option != "➕ Create New Proposal":

        selected_index = business_options.index(
            selected_option
        )

        selected_record = df.iloc[
            selected_index
        ]

        st.success(
            "Business loaded from CRM ✅"
        )

    st.divider()

    # ==========================================================
    # PROPOSAL FORM
    # ==========================================================

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

    with st.form(
        "reports_proposal_form"
    ):

        st.markdown(
            "### 🏢 Business Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            business = st.text_input(

                "Business Name",

                value=default_business,

                key="proposal_business_name"

            )

            industry = st.text_input(

                "Industry",

                value=default_industry,

                key="proposal_industry"

            )

        with col2:

            website = st.text_input(

                "Website",

                value=default_website,

                key="proposal_website"

            )

            location = st.text_input(

                "Location",

                value=default_location,

                key="proposal_location"

            )

        project_value = st.number_input(

            "Estimated Project Value ($)",

            min_value=100,

            value=max(
                100,
                default_value
            ),

            step=100,

            key="proposal_project_value"

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

            ],

            key="proposal_services"

        )

        generate_button = st.form_submit_button(

            "🚀 Generate Professional Proposal",

            use_container_width=True

        )

    # ==========================================================
    # GENERATE PROPOSAL
    # ==========================================================

    if generate_button:

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

        # ------------------------------------------------------
        # LEAD SCORE
        # ------------------------------------------------------

        lead_score = 90

        if selected_record is not None:

            try:

                lead_score = int(
                    selected_record.get(
                        "lead_score",
                        90
                    )
                    or 90
                )

            except Exception:

                lead_score = 90

        # ------------------------------------------------------
        # CONTACT INFORMATION
        # ------------------------------------------------------

        if selected_record is not None:

            selected_email = str(
                selected_record.get(
                    "email",
                    "Not Available"
                )
            )

            selected_phone = str(
                selected_record.get(
                    "phone",
                    "Not Available"
                )
            )

        else:

            selected_email = "Not Available"
            selected_phone = "Not Available"

        business_data = {

            "name": business,

            "lead_score": lead_score,

            "website": website,

            "email": selected_email,

            "phone": selected_phone

        }

        # ------------------------------------------------------
        # GENERATE
        # ------------------------------------------------------

        with st.spinner(
            "🤖 Generating professional proposal..."
        ):

            proposal_text = generate_proposal(

                business_data,

                services,

                project_value

            )

        st.session_state[
            "generated_proposal"
        ] = proposal_text

        st.session_state[
            "proposal_business_id"
        ] = (

            selected_record.get(
                "business_id"
            )

            if selected_record is not None

            else None

        )

        st.success(
            "Proposal Generated Successfully ✅"
        )

    # ==========================================================
    # SHOW GENERATED PROPOSAL
    # ==========================================================

    if "generated_proposal" in st.session_state:

        proposal_text = st.session_state[
            "generated_proposal"
        ]

        st.divider()

        st.subheader(
            "📄 Proposal Preview"
        )

        st.text_area(

            "Generated Proposal",

            proposal_text,

            height=550,

            key="proposal_preview"

        )

        # ======================================================
        # PDF
        # ======================================================

        st.divider()

        st.subheader(
            "📥 Export Proposal"
        )

        with st.spinner(
            "Preparing PDF..."
        ):

            pdf = generate_pdf(
                proposal_text
            )

        proposal_business_name = business.strip()

        safe_name = (

            proposal_business_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")

        )

        filename = (

            f"{safe_name}_Proposal.pdf"

        )

        st.download_button(

            "📄 Download Proposal PDF",

            data=pdf,

            file_name=filename,

            mime="application/pdf",

            use_container_width=True,

            key="download_proposal_pdf"

        )

        # ======================================================
        # MARK PROPOSAL SENT
        # ======================================================

        proposal_business_id = st.session_state.get(
            "proposal_business_id"
        )

        if proposal_business_id is not None:

            st.divider()

            st.subheader(
                "📤 Proposal Status"
            )

            st.caption(
                "After sending the proposal to the client, "
                "mark it as sent so CRM tracking stays updated."
            )

            if st.button(

                "📤 Mark Proposal as Sent",

                use_container_width=True,

                key="mark_proposal_sent_button"

            ):

                result = mark_proposal_sent(
                    proposal_business_id
                )

                if result:

                    st.success(
                        "Proposal marked as sent ✅"
                    )

                    st.session_state.pop(
                        "generated_proposal",
                        None
                    )

                    st.session_state.pop(
                        "proposal_business_id",
                        None
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to update proposal status."
                    )

        else:

            st.info(
                "This is a new proposal. "
                "It is not linked to a CRM record."
            )