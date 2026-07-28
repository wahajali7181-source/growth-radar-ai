import streamlit as st

from lead_engine.database import (
    total_businesses,
    load_businesses
)

from crm.engine import load_crm


def show():

    st.title("🚀 Growth Radar AI")

    st.caption("AI Powered Business Intelligence Platform")

    businesses = load_businesses()
    crm = load_crm()

    total = total_businesses()

    if crm.empty:
        total_pipeline = 0
        total_crm = 0
    else:
        total_pipeline = crm["estimated_value"].fillna(0).sum()
        total_crm = len(crm)

    high_priority = 0

    if not businesses.empty:

        if "opportunity" in businesses.columns:

            high_priority = len(

                businesses[
                    businesses["opportunity"] == "High"
                ]

            )

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Businesses",
        total
    )

    c2.metric(
        "CRM Leads",
        total_crm
    )

    c3.metric(
        "High Priority",
        high_priority
    )

    c4.metric(
        "Pipeline Value",
        f"${int(total_pipeline):,}"
    )

    st.divider()

    st.subheader("Recent Businesses")

    if businesses.empty:

        st.info("No businesses found.")

    else:

        st.dataframe(

            businesses.tail(10),

            use_container_width=True

        )

    st.divider()

    st.subheader("Recent CRM")

    if crm.empty:

        st.info("No CRM data found.")

    else:

        st.dataframe(

            crm.tail(10),

            use_container_width=True

        )