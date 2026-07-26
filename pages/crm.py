import streamlit as st
import pandas as pd

from crm.engine import load_crm
from crm.engine import save_crm


def show():

    st.title("📋 CRM")

    df = load_crm()

    if df.empty:

        st.info("No CRM records found.")
        return

    # ==========================
    # CRM OVERVIEW
    # ==========================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Leads",
        len(df)
    )

    col2.metric(
        "Won Deals",
        len(df[df["status"] == "Won"])
    )

    col3.metric(
        "Open Deals",
        len(df[df["status"] != "Won"])
    )

    col4.metric(
        "Pipeline Value",
        f"${int(df['estimated_value'].sum()):,}"
    )

    st.divider()

    # ==========================
    # SEARCH
    # ==========================

    search = st.text_input(
        "🔍 Search Business ID"
    )

    if search:

        df = df[
            df["business_id"]
            .astype(str)
            .str.contains(search)
        ]

    # ==========================
    # FILTER
    # ==========================

    pipeline_filter = st.selectbox(
        "Pipeline Filter",
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

    if pipeline_filter != "All":

        df = df[
            df["status"] == pipeline_filter
        ]

    # ==========================
    # TABLE
    # ==========================

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    # ==========================
    # FOLLOW UPS
    # ==========================

    st.subheader("📅 Upcoming Follow Ups")

    followups = df[
        df["followup_date"] != ""
    ]

    if followups.empty:

        st.success(
            "No Follow Ups Scheduled"
        )

    else:

        st.dataframe(
            followups[
                [
                    "business_id",
                    "followup_date",
                    "status"
                ]
            ],
            use_container_width=True
        )

    st.divider()

    # ==========================
    # EDIT CRM
    # ==========================

    st.subheader("✏ Edit CRM Record")

    if len(df) > 0:

        selected = st.selectbox(
            "Select Business",
            df["business_id"]
        )

        record = df[
            df["business_id"] == selected
        ].iloc[0]

        starred = st.checkbox(
            "⭐ Starred",
            value=bool(record["starred"])
        )

        notes = st.text_area(
            "Notes",
            value="" if pd.isna(record["notes"]) else str(record["notes"])
        )

        try:
            followup_default = pd.to_datetime(
                record["followup_date"]
            )
        except Exception:
            followup_default = pd.Timestamp.today()

        followup = st.date_input(
            "Follow-up Date",
            value=followup_default
        )

        proposal = st.checkbox(
            "Proposal Sent",
            value=bool(record["proposal_sent"])
        )

        status_options = [
            "New",
            "Contacted",
            "Meeting",
            "Proposal",
            "Won",
            "Lost"
        ]

        current_status = (
            record["status"]
            if record["status"] in status_options
            else "New"
        )

        status = st.selectbox(
            "Status",
            status_options,
            index=status_options.index(current_status)
        )

        value = st.number_input(
            "Estimated Value ($)",
            value=float(record["estimated_value"])
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("💾 Save Changes"):

                save_crm(
                    selected,
                    starred,
                    notes,
                    str(followup),
                    proposal,
                    status,
                    value
                )

                st.success(
                    "CRM Updated Successfully"
                )

                st.rerun()

        with col2:

            if st.button("🗑 Delete Record"):

                st.info(
                    "Delete feature will be enabled in the next update."
                )