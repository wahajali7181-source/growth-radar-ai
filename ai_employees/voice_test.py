import streamlit as st

from auth.session import require_auth
from crm.engine import load_crm

from ai_employees.voice_agent import (
    initialize_voice_agent,
    get_voice_agent,
    generate_opening,
    generate_voice_response,
    reset_voice_agent,
    set_call_outcome,
)


def show():

    require_auth()

    st.title("🎙 AI Voice Agent")

    st.caption(
        "Test the AI sales agent before connecting a real phone provider."
    )

    st.divider()

    # ======================================================
    # ACTIVE AGENT
    # ======================================================

    agent = get_voice_agent()

    if not agent:

        df = load_crm()

        if df.empty:

            st.info(
                "No CRM leads available."
            )

            return

        st.subheader(
            "🎯 Start Test Call"
        )

        if "business_name" in df.columns:

            businesses = (
                df["business_name"]
                .fillna("Unknown Business")
                .astype(str)
                .tolist()
            )

        else:

            businesses = (
                df["business_id"]
                .astype(str)
                .tolist()
            )

        selected_name = st.selectbox(
            "Select Lead",
            businesses,
            key="voice_test_business",
        )

        if "business_name" in df.columns:

            rows = df[
                df["business_name"]
                .fillna("")
                .astype(str)
                == selected_name
            ]

        else:

            rows = df[
                df["business_id"]
                .astype(str)
                == selected_name
            ]

        if rows.empty:

            st.error(
                "Unable to load lead."
            )

            return

        lead = rows.iloc[0].to_dict()

        service = st.text_input(
            "Service",
            placeholder="Meta Ads, SEO, Web Development...",
            key="voice_test_service",
        )

        tone = st.selectbox(
            "Tone",
            [
                "Professional",
                "Friendly",
                "Confident",
                "Consultative",
            ],
            key="voice_test_tone",
        )

        objective = st.selectbox(
            "Objective",
            [
                "Book a Meeting",
                "Generate Interest",
                "Close a Sale",
                "Get a Callback",
            ],
            key="voice_test_objective",
        )

        if st.button(
            "🎙 Start AI Call",
            use_container_width=True,
            type="primary",
        ):

            if not service.strip():

                st.warning(
                    "Enter the service first."
                )

                return

            initialize_voice_agent(

                lead=lead,

                service=service,

                objective=objective,

                tone=tone,

            )

            result = generate_opening()

            if not result["success"]:

                st.error(
                    result["error"]
                )

                reset_voice_agent()

                return

            st.rerun()

        return

    # ======================================================
    # ACTIVE CALL
    # ======================================================

    lead = agent.get(
        "lead",
        {}
    )

    st.success(
        "🟢 AI Call Simulation Active"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Business",
            lead.get(
                "business_name",
                "Unknown",
            ),
        )

    with col2:

        st.metric(
            "Service",
            agent.get(
                "service",
                "",
            ),
        )

    with col3:

        st.metric(
            "Status",
            agent.get(
                "status",
                "",
            ),
        )

    st.divider()

    # ======================================================
    # CONVERSATION
    # ======================================================

    st.subheader(
        "💬 Conversation"
    )

    conversation = agent.get(
        "conversation",
        [],
    )

    for message in conversation:

        role = message.get(
            "role",
            "",
        )

        content = message.get(
            "content",
            "",
        )

        if role == "assistant":

            st.chat_message(
                "assistant"
            ).write(
                content
            )

        else:

            st.chat_message(
                "user"
            ).write(
                content
            )

    # ======================================================
    # PROSPECT RESPONSE
    # ======================================================

    st.divider()

    st.subheader(
        "🗣 Prospect Response"
    )

    prospect_message = st.text_area(

        "Type what the prospect says",

        placeholder=(
            "Example: I'm interested, but I already "
            "have someone handling our marketing."
        ),

        key="voice_test_prospect_message",

    )

    if st.button(
        "▶ Send Response",
        use_container_width=True,
    ):

        if not prospect_message.strip():

            st.warning(
                "Enter the prospect's response."
            )

            return

        result = generate_voice_response(
            prospect_message
        )

        if not result["success"]:

            st.error(
                result["error"]
            )

            return

        st.rerun()

    # ======================================================
    # CALL OUTCOME
    # ======================================================

    st.divider()

    st.subheader(
        "📌 Call Outcome"
    )

    outcome = st.selectbox(

        "Select outcome",

        [
            "Interested",
            "Meeting Booked",
            "Callback Requested",
            "Not Interested",
            "No Answer",
            "Follow Up",
            "Closed",
        ],

        key="voice_test_outcome",

    )

    if st.button(
        "✅ Complete Call",
        use_container_width=True,
    ):

        set_call_outcome(
            outcome
        )

        st.success(
            f"Call completed: {outcome}"
        )

    # ======================================================
    # RESET
    # ======================================================

    if st.button(
        "🔄 Start New Test Call",
        use_container_width=True,
    ):

        reset_voice_agent()

        st.rerun()