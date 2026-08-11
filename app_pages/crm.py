import streamlit as st
import pandas as pd

from crm.engine import (
    load_crm,
    save_crm,
    delete_crm
)

from auth.session import require_auth


def show():

    require_auth()

    st.title("📋 CRM 2.0")

    st.caption(
        "Manage your complete sales pipeline."
    )

    # ==========================================
    # LOAD CRM
    # ==========================================

    df = load_crm()

    # ==========================================
    # ADD NEW LEAD
    # ==========================================

    with st.expander("➕ Add Lead Manually"):

        with st.form("manual_lead_form"):

            st.subheader("🏢 Business Information")

            col1, col2 = st.columns(2)

            with col1:

                new_business_id = st.number_input(
                    "Business ID",
                    min_value=1,
                    value=100000,
                    step=1
                )

                new_business_name = st.text_input(
                    "Business Name"
                )

                new_industry = st.text_input(
                    "Industry"
                )

                new_website = st.text_input(
                    "Website",
                    placeholder="https://example.com"
                )

                new_location = st.text_input(
                    "Location"
                )

            with col2:

                new_email = st.text_input(
                    "Business Email"
                )

                new_phone = st.text_input(
                    "Phone"
                )

                new_lead_score = st.number_input(
                    "Lead Score",
                    min_value=0,
                    max_value=100,
                    value=0,
                    step=1
                )

                new_priority = st.selectbox(
                    "Priority",
                    [
                        "Low",
                        "Medium",
                        "High"
                    ]
                )

                new_status = st.selectbox(
                    "Status",
                    [
                        "New",
                        "Contacted",
                        "Meeting",
                        "Proposal",
                        "Won",
                        "Lost"
                    ]
                )

            st.divider()

            st.subheader("💰 Deal Information")

            col1, col2, col3 = st.columns(3)

            with col1:

                new_value = st.number_input(
                    "Estimated Value ($)",
                    min_value=0,
                    value=1000,
                    step=100
                )

            with col2:

                new_revenue = st.number_input(
                    "Revenue ($)",
                    min_value=0,
                    value=0,
                    step=100
                )

            with col3:

                new_assigned = st.text_input(
                    "Assigned To"
                )

            new_notes = st.text_area(
                "Notes"
            )

            add_lead = st.form_submit_button(
                "➕ Add Lead",
                use_container_width=True
            )

            if add_lead:

                if not new_business_name.strip():

                    st.warning(
                        "Please enter Business Name."
                    )

                else:

                    result = save_crm(

                        new_business_id,

                        False,

                        new_notes,

                        "",

                        False,

                        new_status,

                        new_value,

                        business_name=new_business_name,

                        industry=new_industry,

                        priority=new_priority,

                        assigned_to=new_assigned,

                        meeting_date="",

                        revenue=new_revenue,

                        deal_stage="Open",

                        website=new_website,

                        location=new_location,

                        email=new_email,

                        phone=new_phone,

                        lead_score=new_lead_score

                    )

                    if result:

                        st.success(
                            "Lead added to CRM successfully ✅"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Unable to save CRM lead."
                        )

    # ==========================================
    # EMPTY STATE
    # ==========================================

    if df.empty:

        st.info(
            "No CRM records available yet."
        )

        st.caption(
            "Use '➕ Add Lead Manually' above "
            "to create your first lead."
        )

        return

    # ==========================================
    # DASHBOARD
    # ==========================================

    total = len(df)

    won = len(
        df[df["status"] == "Won"]
    )

    lost = len(
        df[df["status"] == "Lost"]
    )

    open_deals = total - won - lost

    pipeline = int(
        df["estimated_value"]
        .fillna(0)
        .sum()
    )

    revenue = int(
        df["revenue"]
        .fillna(0)
        .sum()
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Businesses",
        total
    )

    c2.metric(
        "Open",
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

    st.divider()

    # ==========================================
    # FILTERS
    # ==========================================

    left, right = st.columns(2)

    with left:

        search = st.text_input(
            "🔍 Search Business"
        )

    with right:

        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "New",
                "Contacted",
                "Meeting",
                "Proposal",
                "Won",
                "Lost"
            ]
        )

    filtered_df = df.copy()

    if search:

        keyword = search.lower()

        if "business_name" in filtered_df.columns:

            filtered_df = filtered_df[
                filtered_df["business_name"]
                .fillna("")
                .str.lower()
                .str.contains(
                    keyword,
                    na=False
                )
            ]

        else:

            filtered_df = filtered_df[
                filtered_df["business_id"]
                .astype(str)
                .str.contains(
                    keyword,
                    na=False
                )
            ]

    if status_filter != "All":

        filtered_df = filtered_df[
            filtered_df["status"] == status_filter
        ]

    st.divider()

    # ==========================================
    # CRM TABLE
    # ==========================================

    st.subheader("📋 CRM Records")

    display_columns = [

        "business_id",
        "business_name",
        "industry",
        "website",
        "location",
        "email",
        "phone",
        "lead_score",
        "status",
        "priority",
        "estimated_value",
        "revenue",
        "assigned_to",
        "followup_date"

    ]

    available = [

        c
        for c in display_columns
        if c in filtered_df.columns

    ]

    st.dataframe(
        filtered_df[available],
        use_container_width=True
    )

    st.divider()

    # ==========================================
    # FOLLOW UPS
    # ==========================================

    st.subheader("📅 Upcoming Follow-ups")

    if "followup_date" in filtered_df.columns:

        followups = filtered_df[
            filtered_df["followup_date"]
            .fillna("")
            .astype(str)
            .str.strip()
            != ""
        ]

    else:

        followups = pd.DataFrame()

    if followups.empty:

        st.success(
            "No Follow-ups Scheduled"
        )

    else:

        cols = [

            c
            for c in [
                "business_id",
                "business_name",
                "followup_date",
                "status"
            ]
            if c in followups.columns

        ]

        st.dataframe(
            followups[cols],
            use_container_width=True
        )

    st.divider()

    # ==========================================
    # EDIT RECORD
    # ==========================================

    st.subheader("✏️ Edit CRM")

    if len(filtered_df) == 0:

        st.info(
            "No CRM records match your filters."
        )

        return

    selected = st.selectbox(
        "Select Business",
        filtered_df["business_id"].tolist()
    )

    record = filtered_df[
        filtered_df["business_id"] == selected
    ].iloc[0]

    # ==========================================
    # BUSINESS INFORMATION
    # ==========================================

    st.markdown(
        "### 🏢 Business Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        edit_business_name = st.text_input(
            "Business Name",
            value=str(
                record.get(
                    "business_name",
                    ""
                )
            )
        )

        edit_industry = st.text_input(
            "Industry",
            value=str(
                record.get(
                    "industry",
                    ""
                )
            )
        )

        edit_website = st.text_input(
            "Website",
            value=str(
                record.get(
                    "website",
                    ""
                )
            )
        )

        edit_location = st.text_input(
            "Location",
            value=str(
                record.get(
                    "location",
                    ""
                )
            )
        )

    with col2:

        edit_email = st.text_input(
            "Business Email",
            value=str(
                record.get(
                    "email",
                    ""
                )
            )
        )

        edit_phone = st.text_input(
            "Phone",
            value=str(
                record.get(
                    "phone",
                    ""
                )
            )
        )

        try:

            current_lead_score = int(
                record.get(
                    "lead_score",
                    0
                )
                or 0
            )

        except Exception:

            current_lead_score = 0

        edit_lead_score = st.number_input(
            "Lead Score",
            min_value=0,
            max_value=100,
            value=current_lead_score,
            step=1
        )

    st.divider()

    # ==========================================
    # CRM DETAILS
    # ==========================================

    starred = st.checkbox(
        "⭐ Starred",
        value=bool(
            record.get(
                "starred",
                0
            )
        )
    )

    notes = st.text_area(
        "Notes",
        value=str(
            record.get(
                "notes",
                ""
            )
        )
    )

    # ==========================================
    # FOLLOW-UP DATE
    # ==========================================

    try:

        default_date = pd.to_datetime(
            record.get(
                "followup_date",
                ""
            )
        )

        if pd.isna(default_date):

            default_date = pd.Timestamp.today()

    except Exception:

        default_date = pd.Timestamp.today()

    followup = st.date_input(
        "Follow-up Date",
        value=default_date.date()
    )

    # ==========================================
    # PROPOSAL SENT
    # ==========================================

    proposal = st.checkbox(
        "📄 Proposal Sent",
        value=bool(
            record.get(
                "proposal_sent",
                0
            )
        )
    )

    # ==========================================
    # STATUS
    # ==========================================

    status_options = [

        "New",
        "Contacted",
        "Meeting",
        "Proposal",
        "Won",
        "Lost"

    ]

    current_status = record.get(
        "status",
        "New"
    )

    if current_status not in status_options:

        current_status = "New"

    status = st.selectbox(
        "Status",
        status_options,
        index=status_options.index(
            current_status
        )
    )

    # ==========================================
    # FINANCIALS
    # ==========================================

    value = st.number_input(
        "Estimated Value ($)",
        min_value=0.0,
        value=float(
            record.get(
                "estimated_value",
                0
            )
            or 0
        )
    )

    revenue_value = st.number_input(
        "Revenue ($)",
        min_value=0.0,
        value=float(
            record.get(
                "revenue",
                0
            )
            or 0
        )
    )

    # ==========================================
    # PRIORITY
    # ==========================================

    priority_options = [

        "Low",
        "Medium",
        "High"

    ]

    current_priority = record.get(
        "priority",
        "Medium"
    )

    if current_priority not in priority_options:

        current_priority = "Medium"

    priority = st.selectbox(
        "Priority",
        priority_options,
        index=priority_options.index(
            current_priority
        )
    )

    assigned = st.text_input(
        "Assigned To",
        value=str(
            record.get(
                "assigned_to",
                ""
            )
        )
    )

    meeting = st.text_input(
        "Meeting Date",
        value=str(
            record.get(
                "meeting_date",
                ""
            )
        )
    )

    # ==========================================
    # DEAL STAGE
    # ==========================================

    stage_options = [

        "Open",
        "Negotiation",
        "Closed"

    ]

    current_stage = record.get(
        "deal_stage",
        "Open"
    )

    if current_stage not in stage_options:

        current_stage = "Open"

    stage = st.selectbox(
        "Deal Stage",
        stage_options,
        index=stage_options.index(
            current_stage
        )
    )

    # ==========================================
    # ACTIONS
    # ==========================================

    st.divider()

    st.subheader("⚡ CRM Actions")

    col1, col2, col3 = st.columns(3)

    # ==========================================
    # SAVE
    # ==========================================

    with col1:

        if st.button(
            "💾 Save",
            use_container_width=True
        ):

            result = save_crm(

                selected,

                starred,

                notes,

                str(followup),

                proposal,

                status,

                value,

                business_name=edit_business_name,

                industry=edit_industry,

                priority=priority,

                assigned_to=assigned,

                meeting_date=meeting,

                revenue=revenue_value,

                deal_stage=stage,

                website=edit_website,

                location=edit_location,

                email=edit_email,

                phone=edit_phone,

                lead_score=edit_lead_score

            )

            if result:

                st.success(
                    "CRM Updated Successfully ✅"
                )

                st.rerun()

            else:

                st.error(
                    "Unable to update CRM."
                )

    # ==========================================
    # GENERATE PROPOSAL
    # ==========================================

    with col2:

        if st.button(
            "📄 Generate Proposal",
            use_container_width=True
    ):

            st.session_state[
                "proposal_business_id"
            ] = int(selected)

            st.session_state[
                "proposal_from_crm"
            ] = True

            st.session_state[
                "requested_page"
            ] = "📄 Reports"

            st.rerun()
    # ==========================================
    # DELETE
    # ==========================================

    with col3:

        if st.button(
            "🗑 Delete",
            use_container_width=True
        ):

            delete_crm(selected)

            st.success(
                "Record Deleted"
            )

            st.rerun()