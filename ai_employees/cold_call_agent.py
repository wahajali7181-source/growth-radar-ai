import streamlit as st
import pandas as pd

from auth.session import require_auth, current_user
from crm.engine import load_crm, save_crm


def generate_call_script(
    business_name,
    industry,
    contact_name,
    objective,
    notes
):
    contact = contact_name.strip() if contact_name.strip() else "there"

    return f"""
COLD CALL SCRIPT
==================================================

Business:
{business_name}

Industry:
{industry}

Contact:
{contact}

Objective:
{objective}

==================================================
OPENING
==================================================

AI AGENT:

"Hi, may I speak with {contact}?

Hi, this is a representative from Growth Radar AI.
I hope I'm not catching you at a bad time.

I'll keep this very brief.

We help businesses improve their online presence,
generate more qualified leads, and automate parts
of their sales and marketing process.

I was looking at {business_name} and noticed that
there may be some opportunities worth discussing."

==================================================
DISCOVERY QUESTIONS
==================================================

1. "How are you currently generating most of your
   new customers?"

2. "Are you currently running any paid advertising?"

3. "How satisfied are you with the number of leads
   you're getting each month?"

4. "Are there any areas of your online marketing
   that you feel could be performing better?"

5. "Would you be open to hearing a few ideas that
   could potentially improve your results?"

==================================================
VALUE PROPOSITION
==================================================

"Based on what you've shared, I believe there may be
a few areas where we could help.

We can look at your lead generation, advertising,
website conversion, social media presence and
automation opportunities.

The goal isn't simply to generate traffic.

The goal is to generate better-qualified opportunities
and turn more of them into customers."

==================================================
CALL TO ACTION
==================================================

"If you're interested, we can arrange a short
strategy discussion where we can show you exactly
what we found and what we'd recommend."

==================================================
IF THEY SAY YES
==================================================

"Excellent.

What would be a convenient time for you for a short
strategy call?"

==================================================
IF THEY ARE BUSY
==================================================

"No problem at all.

Would you prefer that I call you back at another
time, or would it be easier if I sent you the
information first?"

==================================================
IF THEY SAY NO
==================================================

"Absolutely, I understand.

Thank you for your time and I hope you have a
great day."

==================================================
AGENT NOTES
==================================================

Objective:
{objective}

CRM Notes:
{notes}
"""

def show():

    require_auth()

    user = current_user()

    email = user.get("email")

    st.title("📞 AI Cold Call Agent")

    st.caption(
        "Prepare and manage professional AI-powered sales calls."
    )

    st.divider()

    # ==========================================================
    # LOAD CRM
    # ==========================================================

    df = load_crm()

    if df.empty:

        st.info(
            "No CRM leads available."
        )

        st.caption(
            "Add businesses to CRM first."
        )

        return

    # ==========================================================
    # NORMALIZE DATA
    # ==========================================================

    df = df.copy()

    required_columns = {

        "business_name": "",
        "industry": "",
        "email": "",
        "phone": "",
        "status": "New",
        "notes": ""

    }

    for column, default in required_columns.items():

        if column not in df.columns:

            df[column] = default

    # ==========================================================
    # LEAD SELECTOR
    # ==========================================================

    st.subheader("🏢 Select CRM Lead")

    lead_labels = []

    for index, row in df.iterrows():

        name = str(
            row.get(
                "business_name",
                ""
            )
        ).strip()

        if not name:

            name = f"Business #{index + 1}"

        phone = str(
            row.get(
                "phone",
                ""
            )
        ).strip()

        lead_labels.append(
            f"{name} | {phone if phone else 'No phone'}"
        )

    selected_label = st.selectbox(

        "Select Business",

        lead_labels

    )

    selected_index = lead_labels.index(
        selected_label
    )

    lead = df.iloc[selected_index]

    business_name = str(
        lead.get(
            "business_name",
            ""
        )
    )

    industry = str(
        lead.get(
            "industry",
            ""
        )
    )

    phone = str(
        lead.get(
            "phone",
            ""
        )
    )

    email_address = str(
        lead.get(
            "email",
            ""
        )
    )

    current_status = str(
        lead.get(
            "status",
            "New"
        )
    )

    existing_notes = str(
        lead.get(
            "notes",
            ""
        )
    )

    # ==========================================================
    # LEAD INFORMATION
    # ==========================================================

    st.divider()

    st.subheader("📋 Lead Information")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Business",
        business_name
    )

    c2.metric(
        "Status",
        current_status
    )

    c3.metric(
        "Phone",
        phone if phone else "Not Available"
    )

    if email_address:

        st.caption(
            f"📧 {email_address}"
        )

    if industry:

        st.caption(
            f"🏷️ Industry: {industry}"
        )

    st.divider()

    # ==========================================================
    # CALL SETTINGS
    # ==========================================================

    st.subheader("🎯 Call Settings")

    col1, col2 = st.columns(2)

    with col1:

        contact_name = st.text_input(
            "Contact Name",
            placeholder="John"
        )

        objective = st.selectbox(

            "Call Objective",

            [

                "Introduce Growth Radar AI",

                "Qualify Business",

                "Generate Sales Opportunity",

                "Book Strategy Call",

                "Follow Up Existing Lead",

                "Close Potential Client"

            ]

        )

    with col2:

        call_tone = st.selectbox(

            "AI Agent Tone",

            [

                "Professional",

                "Friendly",

                "Consultative",

                "Confident"

            ]

        )

        call_language = st.selectbox(

            "Call Language",

            [

                "English",

                "English - US",

                "English - UK",

                "English - Australia"

            ]

        )

    call_notes = st.text_area(

        "Additional Instructions",

        placeholder=(
            "Example: Focus on their lead generation "
            "and website conversion problems."
        ),

        height=120

    )

    # ==========================================================
    # GENERATE SCRIPT
    # ==========================================================

    if st.button(

        "🤖 Prepare AI Call",

        use_container_width=True

    ):

        if not phone.strip():

            st.warning(
                "This CRM lead does not have a phone number."
            )

            return

        with st.spinner(
            "Preparing professional AI call..."
        ):

            script = generate_call_script(

                business_name,
                industry,
                contact_name,
                objective,
                call_notes

            )

        st.session_state[
            "cold_call_script"
        ] = script

        st.session_state[
            "cold_call_business_id"
        ] = lead.get(
            "business_id",
            None
        )

        st.session_state[
            "cold_call_phone"
        ] = phone

        st.success(
            "AI Call prepared successfully ✅"
        )

    # ==========================================================
    # CALL SCRIPT
    # ==========================================================

    if "cold_call_script" not in st.session_state:

        return

    st.divider()

    st.subheader("🧠 AI Call Preparation")

    st.text_area(

        "Professional Call Script",

        st.session_state[
            "cold_call_script"
        ],

        height=600

    )

    st.divider()

    # ==========================================================
    # CALL STATUS
    # ==========================================================

    st.subheader("📞 Call Center")

    st.info(
        f"Target: {business_name} | "
        f"Phone: {st.session_state['cold_call_phone']}"
    )

    st.warning(
        "Real phone calling is not connected yet. "
        "This module is currently in preparation mode."
    )

    call_status = st.selectbox(

        "Call Result",

        [

            "Not Called",

            "Interested",

            "Callback Requested",

            "Meeting Booked",

            "Not Interested",

            "No Answer",

            "Wrong Number"

        ]

    )

    call_summary = st.text_area(

        "Call Summary",

        placeholder=(
            "Write what happened during the call..."
        ),

        height=150

    )

    # ==========================================================
    # CRM UPDATE
    # ==========================================================

    if st.button(

        "💾 Save Call Result to CRM",

        use_container_width=True

    ):

        business_id = (
            st.session_state.get(
                "cold_call_business_id"
            )
        )

        if business_id is None:

            st.error(
                "Business ID not found."
            )

            return

        status_mapping = {

            "Interested":
                "Contacted",

            "Callback Requested":
                "Contacted",

            "Meeting Booked":
                "Meeting",

            "Not Interested":
                "Lost",

            "No Answer":
                "Contacted",

            "Wrong Number":
                "Lost",

            "Not Called":
                current_status

        }

        new_status = status_mapping.get(

            call_status,

            current_status

        )

        combined_notes = existing_notes

        if call_summary.strip():

            if combined_notes.strip():

                combined_notes += (
                    "\n\n"
                )

            combined_notes += (
                "AI Cold Call:\n"
                + call_summary.strip()
            )

        try:

            estimated_value = float(
                lead.get(
                    "estimated_value",
                    0
                )
                or 0
            )

        except Exception:

            estimated_value = 0

        try:

            revenue = float(
                lead.get(
                    "revenue",
                    0
                )
                or 0
            )

        except Exception:

            revenue = 0

        result = save_crm(

            business_id,

            bool(
                lead.get(
                    "starred",
                    0
                )
            ),

            combined_notes,

            str(
                lead.get(
                    "followup_date",
                    ""
                )
                or ""
            ),

            bool(
                lead.get(
                    "proposal_sent",
                    0
                )
            ),

            new_status,

            estimated_value,

            business_name=business_name,

            industry=industry,

            priority=str(
                lead.get(
                    "priority",
                    "Medium"
                )
            ),

            assigned_to=str(
                lead.get(
                    "assigned_to",
                    ""
                )
            ),

            meeting_date=str(
                lead.get(
                    "meeting_date",
                    ""
                )
            ),

            revenue=revenue,

            deal_stage=str(
                lead.get(
                    "deal_stage",
                    "Open"
                )
            ),

            website=str(
                lead.get(
                    "website",
                    ""
                )
            ),

            location=str(
                lead.get(
                    "location",
                    ""
                )
            ),

            email=email_address,

            phone=phone,

            lead_score=int(
                lead.get(
                    "lead_score",
                    0
                )
                or 0
            )

        )

        if result:

            st.success(
                f"Call result saved: {call_status} ✅"
            )

            st.info(
                f"CRM status updated to: {new_status}"
            )

        else:

            st.error(
                "Unable to update CRM."
            )