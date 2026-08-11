import streamlit as st
import pandas as pd

from auth.session import require_auth, current_user
from crm.engine import load_crm
from subscriptions.engine import get_remaining, needs_upgrade


def show():

    # ==========================================================
    # AUTH
    # ==========================================================

    require_auth()

    user = current_user()

    if not user:
        st.error("Please login first.")
        return

    email = user["email"]

    # ==========================================================
    # PAGE HEADER
    # ==========================================================

    st.title("📞 AI Cold Call Agent")

    st.caption(
        "Let AI handle professional business calls using your CRM leads."
    )

    st.divider()

    # ==========================================================
    # SUBSCRIPTION
    # ==========================================================

    remaining = get_remaining(
        email,
        "ai_calls"
    )

    col1, col2 = st.columns([3, 1])

    with col1:

        if remaining == "Unlimited":

            st.success(
                "📞 AI Calls Remaining: Unlimited"
            )

        else:

            st.info(
                f"📞 AI Calls Remaining: {remaining}"
            )

    with col2:

        if st.button(
            "⭐ Upgrade",
            use_container_width=True
        ):

            st.info(
                "Upgrade Plan is available from the sidebar."
            )

    st.divider()

    # ==========================================================
    # AI AGENT SETTINGS
    # ==========================================================

    st.subheader("🤖 AI Agent Settings")

    col1, col2 = st.columns(2)

    with col1:

        agent_name = st.text_input(
            "Agent Name",
            value="Alex"
        )

        language = st.selectbox(
            "Call Language",
            [
                "English",
                "English (US)",
                "English (UK)",
                "English (Australia)"
            ]
        )

    with col2:

        call_tone = st.selectbox(
            "Call Style",
            [
                "Professional",
                "Friendly",
                "Confident",
                "Sales Professional"
            ]
        )

        max_call_duration = st.number_input(
            "Maximum Call Duration (minutes)",
            min_value=1,
            max_value=30,
            value=5,
            step=1
        )

    st.divider()

    # ==========================================================
    # CALL OBJECTIVE
    # ==========================================================

    st.subheader("🎯 Call Objective")

    objective = st.selectbox(
        "What should the AI try to achieve?",
        [
            "Introduce our services",
            "Generate a sales lead",
            "Book a meeting",
            "Qualify the business",
            "Follow up on proposal",
            "Custom"
        ]
    )

    custom_objective = ""

    if objective == "Custom":

        custom_objective = st.text_area(
            "Custom Objective",
            placeholder=(
                "Example: Ask the business owner if "
                "they are interested in Meta Ads."
            )
        )

    st.divider()

    # ==========================================================
    # CRM LEADS
    # ==========================================================

    st.subheader("📋 Select Leads")

    crm = load_crm()

    if crm.empty:

        st.info(
            "No CRM leads available."
        )

        st.caption(
            "Add businesses to CRM first, then return here "
            "to start AI cold calls."
        )

        return

    # ==========================================================
    # FILTER AVAILABLE LEADS
    # ==========================================================

    available_crm = crm.copy()

    if "status" in available_crm.columns:

        available_crm = available_crm[
            available_crm["status"].isin(
                [
                    "New",
                    "Contacted",
                    "Meeting",
                    "Proposal"
                ]
            )
        ]

    if available_crm.empty:

        st.warning(
            "No suitable CRM leads are available for calling."
        )

        return

    # ==========================================================
    # BUSINESS LABELS
    # ==========================================================

    lead_options = []

    for index, row in available_crm.iterrows():

        business_name = str(
            row.get(
                "business_name",
                "Unknown Business"
            )
        ).strip()

        business_id = row.get(
            "business_id",
            index
        )

        lead_options.append(
            f"{business_name} | ID: {business_id}"
        )

    selected_leads = st.multiselect(
        "Choose businesses to call",
        lead_options
    )

    st.divider()

    # ==========================================================
    # CALL PREVIEW
    # ==========================================================

    st.subheader("📝 AI Call Preview")

    if selected_leads:

        selected_indexes = [
            lead_options.index(item)
            for item in selected_leads
        ]

        preview_leads = available_crm.iloc[
            selected_indexes
        ]

        for _, row in preview_leads.iterrows():

            business_name = str(
                row.get(
                    "business_name",
                    "Unknown Business"
                )
            )

            phone = str(
                row.get(
                    "phone",
                    "Not Available"
                )
            )

            st.markdown(
                f"""
### 🏢 {business_name}

**Phone:** {phone}

**Agent:** {agent_name}

**Language:** {language}

**Tone:** {call_tone}

**Objective:** {custom_objective if objective == "Custom" else objective}

**Maximum Duration:** {max_call_duration} minutes
"""
            )

            st.divider()

    else:

        st.info(
            "Select one or more businesses to preview the calls."
        )

    # ==========================================================
    # START CALLING
    # ==========================================================

    st.subheader("🚀 AI Calling")

    if not selected_leads:

        st.warning(
            "Select at least one CRM lead first."
        )

        return

    # ==========================================================
    # SUBSCRIPTION CHECK
    # ==========================================================

    number_of_calls = len(selected_leads)

    if remaining != "Unlimited":

        try:

            remaining_calls = int(
                remaining
            )

        except Exception:

            remaining_calls = 0

        if number_of_calls > remaining_calls:

            st.error(
                f"You selected {number_of_calls} leads, "
                f"but only {remaining_calls} AI calls remain."
            )

            st.info(
                "Reduce the number of leads or upgrade your plan."
            )

            return

    # ==========================================================
    # START BUTTON
    # ==========================================================

    if st.button(
        "📞 Start AI Calling",
        use_container_width=True,
        type="primary"
    ):

        st.session_state[
            "cold_call_campaign"
        ] = {

            "agent_name": agent_name,

            "language": language,

            "tone": call_tone,

            "objective": (
                custom_objective
                if objective == "Custom"
                else objective
            ),

            "max_duration": max_call_duration,

            "leads": selected_leads

        }

        st.success(
            f"AI Calling Campaign Ready — "
            f"{number_of_calls} lead(s) selected."
        )

        st.info(
            "📞 Voice engine will be connected in the next stage."
        )

    # ==========================================================
    # CAMPAIGN STATUS
    # ==========================================================

    if "cold_call_campaign" in st.session_state:

        st.divider()

        st.subheader("📡 Campaign Status")

        campaign = st.session_state[
            "cold_call_campaign"
        ]

        st.success(
            "Campaign prepared successfully."
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Leads",
            len(campaign["leads"])
        )

        c2.metric(
            "Agent",
            campaign["agent_name"]
        )

        c3.metric(
            "Duration",
            f'{campaign["max_duration"]} min'
        )

        st.caption(
            "The actual voice calling engine will be connected "
            "after the campaign workflow is finalized."
        )