import streamlit as st

from auth.session import require_auth, current_user
from crm.engine import load_crm

from ai_employees.ai_provider import (
    generate_ai_response,
    is_ai_available,
)

from ai_employees.lead_context import (
    create_ai_lead_context,
)


# ==========================================================
# AI COLD OUTREACH
# ==========================================================

def show():

    # ======================================================
    # AUTH
    # ======================================================

    require_auth()

    user = current_user()

    if not user:

        st.error(
            "User session not found."
        )

        return

    # ======================================================
    # PAGE HEADER
    # ======================================================

    st.title(
        "📧 AI Cold Outreach"
    )

    st.caption(
        "AI-powered personalized sales conversations for your CRM leads."
    )

    st.divider()

    # ======================================================
    # LOAD CRM
    # ======================================================

    df = load_crm()

    if df.empty:

        st.info(
            "No CRM leads available."
        )

        st.caption(
            "Add leads to CRM first, then return here."
        )

        return

    # ======================================================
    # SELECT BUSINESS
    # ======================================================

    st.subheader(
        "🎯 Select Lead"
    )

    if "business_name" in df.columns:

        business_names = (
            df["business_name"]
            .fillna("Unknown Business")
            .astype(str)
            .tolist()
        )

    else:

        business_names = (
            df["business_id"]
            .astype(str)
            .tolist()
        )

    selected_name = st.selectbox(

        "Choose a business",

        business_names,

        key="smart_outreach_business",

    )

    # ======================================================
    # GET SELECTED LEAD
    # ======================================================

    if "business_name" in df.columns:

        selected_rows = df[
            df["business_name"]
            .fillna("")
            .astype(str)
            == selected_name
        ]

    else:

        selected_rows = df[
            df["business_id"]
            .astype(str)
            == selected_name
        ]

    if selected_rows.empty:

        st.error(
            "Unable to load selected business."
        )

        return

    selected = selected_rows.iloc[0]

    # ======================================================
    # BUILD SMART CONTEXT
    # ======================================================

    ai_context = create_ai_lead_context(
        selected
    )

    lead_context = ai_context["lead"]

    research_summary = ai_context[
        "research_summary"
    ]

    # ======================================================
    # BUSINESS INFORMATION
    # ======================================================

    st.divider()

    st.subheader(
        "🏢 Business Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Business:** "
            f"{lead_context.get('business_name', 'Unknown')}"
        )

        st.write(
            f"**Industry:** "
            f"{lead_context.get('industry', 'Unknown')}"
        )

        st.write(
            f"**Location:** "
            f"{lead_context.get('location', 'Unknown')}"
        )

        st.write(
            f"**Lead Score:** "
            f"{lead_context.get('lead_score', '0')}"
        )

    with col2:

        st.write(
            f"**Website:** "
            f"{lead_context.get('website', 'Not available')}"
        )

        st.write(
            f"**Phone:** "
            f"{lead_context.get('phone', 'Not available')}"
        )

        st.write(
            f"**Priority:** "
            f"{lead_context.get('priority', 'Not available')}"
        )

        st.write(
            f"**CRM Status:** "
            f"{lead_context.get('status', 'Not available')}"
        )

    # ======================================================
    # RESEARCH CONTEXT
    # ======================================================

    with st.expander(
        "🔎 View AI Lead Research Context"
    ):

        st.text(
            research_summary
        )

    # ======================================================
    # OUTREACH SETTINGS
    # ======================================================

    st.divider()

    st.subheader(
        "📞 Outreach Setup"
    )

    outreach_type = st.selectbox(

        "Outreach Channel",

        [
            "Cold Call",
            "Cold Email",
            "WhatsApp Message",
            "LinkedIn Message",
        ],

        key="smart_outreach_channel",

    )

    service = st.text_input(

        "Service You Want To Offer",

        placeholder=(
            "Meta Ads, SEO, Video Editing, "
            "Website Development..."
        ),

        key="smart_outreach_service",

    )

    tone = st.selectbox(

        "Conversation Tone",

        [
            "Professional",
            "Friendly",
            "Confident",
            "Consultative",
        ],

        key="smart_outreach_tone",

    )

    objective = st.selectbox(

        "Primary Objective",

        [
            "Book a Meeting",
            "Generate Interest",
            "Close a Sale",
            "Get a Callback",
        ],

        key="smart_outreach_objective",

    )

    # ======================================================
    # EXTRA SALES CONTEXT
    # ======================================================

    extra_context = st.text_area(

        "Additional Sales Context",

        placeholder=(
            "Add anything you already know about this prospect..."
        ),

        key="smart_outreach_extra_context",

    )

    # ======================================================
    # AI STATUS
    # ======================================================

    st.divider()

    if is_ai_available():

        st.success(
            "🟢 AI Engine Connected"
        )

    else:

        st.warning(
            "🟡 AI Engine is not configured yet."
        )

    # ======================================================
    # GENERATE OUTREACH
    # ======================================================

    if st.button(

        "🤖 Generate Smart AI Outreach",

        use_container_width=True,

        type="primary",

        key="generate_smart_outreach",

    ):

        # --------------------------------------------------
        # Validate service
        # --------------------------------------------------

        if not service.strip():

            st.warning(
                "Please enter the service you want to offer."
            )

            return

        # --------------------------------------------------
        # Validate AI
        # --------------------------------------------------

        if not is_ai_available():

            st.error(
                "AI Engine is not configured. "
                "Please configure OPENAI_API_KEY first."
            )

            return

        # --------------------------------------------------
        # System Instructions
        # --------------------------------------------------

        system_prompt = """
You are Growth Radar AI's professional B2B sales representative.

You help businesses start genuine sales conversations.

Your behavior must follow these rules:

1. Never invent facts about a prospect.
2. Only use information supplied in the lead context.
3. If information is missing, do not pretend it exists.
4. Never claim that you personally visited or contacted the business.
5. Do not make fake guarantees about results.
6. Keep sales language natural and professional.
7. Ask useful discovery questions before pushing a sale.
8. Adapt the pitch to the prospect's industry.
9. Handle objections respectfully.
10. The goal is to create a qualified sales opportunity.

For cold calls, write language that sounds natural when spoken.
Avoid robotic paragraphs.
Keep the opening concise.
"""

        # --------------------------------------------------
        # User Prompt
        # --------------------------------------------------

        user_prompt = f"""
Create a highly personalized B2B sales outreach for this lead.

========================
LEAD RESEARCH
========================

{research_summary}

========================
SERVICE
========================

{service}

========================
CHANNEL
========================

{outreach_type}

========================
TONE
========================

{tone}

========================
OBJECTIVE
========================

{objective}

========================
EXTRA CONTEXT
========================

{extra_context}

========================
OUTPUT
========================

Return exactly these sections:

1. OPENING

Create a natural opening for the selected channel.

2. DISCOVERY QUESTIONS

Give 3-5 questions that help understand the prospect's situation.

3. PERSONALIZED PITCH

Connect the service to the actual information available about
the business.

Do not invent weaknesses.

4. VALUE PROPOSITION

Explain why the prospect should consider the service.

5. COMMON OBJECTIONS

Give at least 5 realistic objections and professional responses.

6. CLOSING

Create a natural close matching the selected objective.

7. FOLLOW-UP

Create a concise follow-up message.

8. CRM NOTES

List the important information the salesperson should record
after the conversation.

Keep everything practical and ready to use.
"""

        # --------------------------------------------------
        # Generate
        # --------------------------------------------------

        with st.spinner(
            "🧠 AI is analyzing the lead context..."
        ):

            result = generate_ai_response(

                system_prompt=system_prompt,

                user_prompt=user_prompt,

            )

        # --------------------------------------------------
        # Failure
        # --------------------------------------------------

        if not result["success"]:

            st.error(
                "AI generation failed."
            )

            st.caption(
                result["error"]
            )

            return

        # --------------------------------------------------
        # Save
        # --------------------------------------------------

        st.session_state[
            "smart_outreach_result"
        ] = result["response"]

        st.session_state[
            "smart_outreach_lead"
        ] = lead_context

        st.session_state[
            "smart_outreach_service"
        ] = service

        st.session_state[
            "smart_outreach_channel"
        ] = outreach_type

        st.session_state[
            "smart_outreach_objective"
        ] = objective

        st.success(
            "✅ Personalized AI outreach generated."
        )

    # ======================================================
    # DISPLAY AI RESULT
    # ======================================================

    if "smart_outreach_result" in st.session_state:

        st.divider()

        st.subheader(
            "🧠 AI Sales Conversation"
        )

        st.markdown(
            st.session_state[
                "smart_outreach_result"
            ]
        )

        # ==================================================
        # LEAD SUMMARY
        # ==================================================

        st.divider()

        st.subheader(
            "📋 Outreach Summary"
        )

        saved_lead = st.session_state.get(
            "smart_outreach_lead",
            {}
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Business:** "
                f"{saved_lead.get('business_name', '')}"
            )

            st.write(
                f"**Industry:** "
                f"{saved_lead.get('industry', '')}"
            )

            st.write(
                f"**Lead Score:** "
                f"{saved_lead.get('lead_score', '0')}"
            )

        with col2:

            st.write(
                f"**Channel:** "
                f"{st.session_state.get('smart_outreach_channel', '')}"
            )

            st.write(
                f"**Service:** "
                f"{st.session_state.get('smart_outreach_service', '')}"
            )

            st.write(
                f"**Objective:** "
                f"{st.session_state.get('smart_outreach_objective', '')}"
            )

        # ==================================================
        # DOWNLOAD
        # ==================================================

        st.divider()

        st.download_button(

            "📥 Download Outreach",

            data=st.session_state[
                "smart_outreach_result"
            ],

            file_name=(
                "GrowthRadar_AI_Outreach.txt"
            ),

            mime="text/plain",

            use_container_width=True,

        )