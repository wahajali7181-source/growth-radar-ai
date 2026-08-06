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

    df = load_crm()

    if df.empty:

        st.info("No CRM records available.")

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
        df["estimated_value"].fillna(0).sum()
    )

    revenue = int(
        df["revenue"].fillna(0).sum()
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

    if search:

        keyword = search.lower()

        if "business_name" in df.columns:

            df = df[
                df["business_name"]
                .fillna("")
                .str.lower()
                .str.contains(keyword)
            ]

        else:

            df = df[
                df["business_id"]
                .astype(str)
                .str.contains(keyword)
            ]

    if status_filter != "All":

        df = df[
            df["status"] == status_filter
        ]

    st.divider()
    # ==========================================
    # CRM TABLE
    # ==========================================

    st.subheader("📋 CRM Records")

    display_columns = [

        "business_id",

        "status",

        "priority",

        "estimated_value",

        "revenue",

        "assigned_to",

        "followup_date"

    ]

    available = [

        c for c in display_columns

        if c in df.columns

    ]

    st.dataframe(

        df[available],

        width="stretch"

    )

    st.divider()

    # ==========================================
    # FOLLOW UPS
    # ==========================================

    st.subheader("📅 Upcoming Follow-ups")

    if "followup_date" in df.columns:

        followups = df[

            df["followup_date"]

            .fillna("")

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

            c for c in [

                "business_id",

                "business_name",

                "followup_date",

                "status"

            ]

            if c in followups.columns

        ]

        st.dataframe(

            followups[cols],

            width="stretch"

        )

    st.divider()

    # ==========================================
    # EDIT RECORD
    # ==========================================

    st.subheader("✏ Edit CRM")

    if len(df) == 0:

        return

    selected = st.selectbox(

        "Select Business",

        df["business_id"]

    )

    record = df[

        df["business_id"] == selected

    ].iloc[0]
    starred = st.checkbox(

        "⭐ Starred",

        value=bool(record.get("starred", 0))

    )

    notes = st.text_area(

        "Notes",

        value=str(record.get("notes", ""))

    )

    try:

        default_date = pd.to_datetime(

            record.get("followup_date", "")

        )

    except Exception:

        default_date = pd.Timestamp.today()

    followup = st.date_input(

        "Follow-up Date",

        value=default_date

    )

    proposal = st.checkbox(

        "Proposal Sent",

        value=bool(record.get("proposal_sent", 0))

    )

    status_options = [

        "New",

        "Contacted",

        "Meeting",

        "Proposal",

        "Won",

        "Lost"

    ]

    status = st.selectbox(

        "Status",

        status_options,

        index=status_options.index(

            record["status"]

            if record["status"] in status_options

            else "New"

        )

    )

    value = st.number_input(

        "Estimated Value ($)",

        value=float(record.get("estimated_value", 0))

    )

    revenue = st.number_input(

        "Revenue ($)",

        value=float(record.get("revenue", 0))

    )

    priority = st.selectbox(

        "Priority",

        [

            "Low",

            "Medium",

            "High"

        ],

        index=[

            "Low",

            "Medium",

            "High"

        ].index(

            record.get(

                "priority",

                "Medium"

            )

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

    stage = st.selectbox(

        "Deal Stage",

        [

            "Open",

            "Negotiation",

            "Closed"

        ],

        index=[

            "Open",

            "Negotiation",

            "Closed"

        ].index(

            record.get(

                "deal_stage",

                "Open"

            )

        )

    )

    left, right = st.columns(2)

    with left:

        if st.button(

            "💾 Save",

            width="stretch"

        ):

            save_crm(

                selected,

                starred,

                notes,

                str(followup),

                proposal,

                status,

                value,

                business_name=str(

                    record.get(

                        "business_name",

                        ""

                    )

                ),

                industry=str(

                    record.get(

                        "industry",

                        ""

                    )

                ),

                priority=priority,

                assigned_to=assigned,

                meeting_date=meeting,

                revenue=revenue,

                deal_stage=stage

            )

            st.success(

                "CRM Updated Successfully"

            )

            st.rerun()

    with right:

        if st.button(

            "🗑 Delete",

            width="stretch"

        ):

            delete_crm(selected)

            st.success(

                "Record Deleted"

            )

            st.rerun()    