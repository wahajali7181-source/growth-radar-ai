import streamlit as st

from crm.engine import save_crm


def crm_card(business):

    st.subheader("📋 CRM")

    starred = st.checkbox("⭐ Star Lead")

    notes = st.text_area("Notes")

    followup = st.date_input("Follow-up Date")

    proposal = st.checkbox("Proposal Sent")

    status = st.selectbox(
        "Pipeline",
        [
            "New",
            "Contacted",
            "Meeting",
            "Proposal",
            "Won",
            "Lost"
        ]
    )

    value = st.number_input(
        "Estimated Value ($)",
        0,
        1000000,
        0
    )

    if st.button("Save CRM"):

        save_crm(
            business["id"],
            int(starred),
            notes,
            str(followup),
            int(proposal),
            status,
            value
        )

        st.success("CRM Saved Successfully ✅")