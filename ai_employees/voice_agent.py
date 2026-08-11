import streamlit as st

from ai_employees.ai_provider import (
    generate_ai_response,
)
from crm.engine import (
    save_call_result,
)

# ==========================================================
# VOICE AGENT STATE
# ==========================================================

def initialize_voice_agent(
    lead,
    service,
    objective="Book a Meeting",
    tone="Professional",
):

    st.session_state["voice_agent"] = {

        "active": True,

        "lead": lead,

        "service": service,

        "objective": objective,

        "tone": tone,

        "conversation": [],

        "status": "Ready",

        "outcome": None,

        "intent": "Unknown",

        "interest_level": "Unknown",

        "notes": [],

        "summary": "",

    }


# ==========================================================
# GET AGENT
# ==========================================================

def get_voice_agent():

    return st.session_state.get(
        "voice_agent"
    )


# ==========================================================
# RESET AGENT
# ==========================================================

def reset_voice_agent():

    if "voice_agent" in st.session_state:

        del st.session_state[
            "voice_agent"
        ]


# ==========================================================
# SYSTEM PROMPT
# ==========================================================

def build_voice_system_prompt(agent):

    lead = agent.get(
        "lead",
        {}
    )

    business_name = lead.get(
        "business_name",
        "the business"
    )

    industry = lead.get(
        "industry",
        "their industry"
    )

    location = lead.get(
        "location",
        "their location"
    )

    lead_score = lead.get(
        "lead_score",
        "Unknown"
    )

    service = agent.get(
        "service",
        ""
    )

    objective = agent.get(
        "objective",
        "Book a Meeting"
    )

    tone = agent.get(
        "tone",
        "Professional"
    )

    return f"""
You are an AI sales representative working for Growth Radar AI.

You are having a professional B2B sales conversation.

TARGET BUSINESS:
{business_name}

INDUSTRY:
{industry}

LOCATION:
{location}

LEAD SCORE:
{lead_score}

SERVICE BEING OFFERED:
{service}

TONE:
{tone}

PRIMARY OBJECTIVE:
{objective}

IMPORTANT RULES:

- Speak naturally.
- Keep responses concise.
- Sound like a professional human sales representative.
- Do not use unnecessary corporate language.
- Ask one useful question at a time.
- Listen before pitching.
- Personalize the conversation using the available business information.
- Never invent information.
- Never make false guarantees.
- Never promise specific results unless they are explicitly provided.
- Never pressure the prospect aggressively.
- Respect a clear "no".
- If the prospect has an objection, acknowledge it first.
- Then respond to the objection naturally.
- If the prospect is interested, move toward the objective.
- If the prospect wants a meeting, help arrange the next step.
- If the prospect wants a callback, acknowledge and capture the intent.
- If the prospect asks for information by email, acknowledge it.
- If the prospect is not interested, end politely.
- Do not pretend to be the business owner.
- Do not impersonate a specific human.
- Be transparent that you are an AI/automated representative when appropriate or required.

Your goal is to create a useful, respectful business conversation.
"""


# ==========================================================
# CONVERSATION TEXT
# ==========================================================

def _conversation_text(agent):

    conversation = agent.get(
        "conversation",
        []
    )

    if not conversation:

        return "No previous conversation."

    text = []

    for message in conversation:

        role = message.get(
            "role",
            "unknown"
        )

        content = message.get(
            "content",
            ""
        )

        text.append(
            f"{role.upper()}: {content}"
        )

    return "\n".join(text)


# ==========================================================
# DETECT PROSPECT INTENT
# ==========================================================

def analyze_prospect_intent(
    prospect_message
):

    message = prospect_message.lower()

    # Meeting
    if any(
        phrase in message
        for phrase in [
            "book a meeting",
            "schedule a meeting",
            "set up a meeting",
            "let's meet",
            "schedule a call",
            "book a call",
        ]
    ):

        return {
            "intent": "Meeting",
            "interest_level": "High",
        }

    # Callback
    if any(
        phrase in message
        for phrase in [
            "call me back",
            "callback",
            "call back",
            "call later",
            "try me later",
        ]
    ):

        return {
            "intent": "Callback",
            "interest_level": "Medium",
        }

    # Information
    if any(
        phrase in message
        for phrase in [
            "send me",
            "send information",
            "email me",
            "more information",
            "more details",
        ]
    ):

        return {
            "intent": "Information",
            "interest_level": "Medium",
        }

    # Positive
    if any(
        phrase in message
        for phrase in [
            "interested",
            "sounds good",
            "tell me more",
            "i'm interested",
            "yes",
            "sure",
            "sounds interesting",
        ]
    ):

        return {
            "intent": "Interested",
            "interest_level": "High",
        }

    # Negative
    if any(
        phrase in message
        for phrase in [
            "not interested",
            "no thanks",
            "don't need",
            "do not need",
            "remove me",
            "stop calling",
        ]
    ):

        return {
            "intent": "Not Interested",
            "interest_level": "Low",
        }

    # Objection
    if any(
        phrase in message
        for phrase in [
            "too expensive",
            "no budget",
            "already have",
            "already working with",
            "not the right time",
            "busy",
            "too busy",
        ]
    ):

        return {
            "intent": "Objection",
            "interest_level": "Medium",
        }

    return {
        "intent": "Unknown",
        "interest_level": "Unknown",
    }


# ==========================================================
# AUTO OUTCOME
# ==========================================================

def _update_intent(agent, prospect_message):

    analysis = analyze_prospect_intent(
        prospect_message
    )

    agent["intent"] = analysis[
        "intent"
    ]

    agent["interest_level"] = analysis[
        "interest_level"
    ]

    # Automatically update obvious outcomes

    if analysis["intent"] == "Meeting":

        agent["outcome"] = "Meeting Booked"

    elif analysis["intent"] == "Callback":

        agent["outcome"] = "Callback Requested"

    elif analysis["intent"] == "Not Interested":

        agent["outcome"] = "Not Interested"

    return analysis


# ==========================================================
# AI RESPONSE
# ==========================================================

def generate_voice_response(
    prospect_message
):

    agent = get_voice_agent()

    if not agent:

        return {
            "success": False,
            "response": "",
            "error": (
                "Voice agent is not initialized."
            ),
        }

    if not prospect_message.strip():

        return {
            "success": False,
            "response": "",
            "error": (
                "Prospect message cannot be empty."
            ),
        }

    # ------------------------------------------------------
    # ANALYZE PROSPECT
    # ------------------------------------------------------

    analysis = _update_intent(
        agent,
        prospect_message
    )

    # ------------------------------------------------------
    # BUILD PROMPT
    # ------------------------------------------------------

    system_prompt = build_voice_system_prompt(
        agent
    )

    conversation_text = _conversation_text(
        agent
    )

    user_prompt = f"""
Previous conversation:

{conversation_text}

The prospect just said:

{prospect_message}

Detected intent:
{analysis["intent"]}

Detected interest level:
{analysis["interest_level"]}

Respond as the sales representative.

Return ONLY the next spoken response.

Requirements:

- Keep it natural.
- Keep it concise.
- Do not repeat the prospect's entire statement.
- If there is an objection, acknowledge it before responding.
- Ask at most one question.
- Move naturally toward the objective.
"""

    # ------------------------------------------------------
    # AI PROVIDER
    # ------------------------------------------------------

    result = generate_ai_response(

        system_prompt=system_prompt,

        user_prompt=user_prompt,

    )

    if not result["success"]:

        return result

    ai_message = result[
        "response"
    ].strip()

    if not ai_message:

        return {
            "success": False,
            "response": "",
            "error": (
                "AI returned an empty response."
            ),
        }

    # ------------------------------------------------------
    # SAVE PROSPECT MESSAGE
    # ------------------------------------------------------

    agent[
        "conversation"
    ].append({

        "role": "prospect",

        "content": prospect_message,

    })

    # ------------------------------------------------------
    # SAVE AI MESSAGE
    # ------------------------------------------------------

    agent[
        "conversation"
    ].append({

        "role": "assistant",

        "content": ai_message,

    })

    agent[
        "status"
    ] = "Conversation Active"

    st.session_state[
        "voice_agent"
    ] = agent

    return {

        "success": True,

        "response": ai_message,

        "error": "",

        "intent": analysis[
            "intent"
        ],

        "interest_level": analysis[
            "interest_level"
        ],

    }


# ==========================================================
# START CONVERSATION
# ==========================================================

def generate_opening():

    agent = get_voice_agent()

    if not agent:

        return {
            "success": False,
            "response": "",
            "error": (
                "Voice agent is not initialized."
            ),
        }

    system_prompt = build_voice_system_prompt(
        agent
    )

    lead = agent.get(
        "lead",
        {}
    )

    business_name = lead.get(
        "business_name",
        "the business"
    )

    user_prompt = f"""
Create the opening line for a professional
sales conversation with {business_name}.

The opening should:

- Be brief.
- Sound natural when spoken.
- Clearly identify the representative honestly.
- Give a simple reason for the call.
- Ask permission to continue.
- Avoid sounding like a scripted advertisement.

Return ONLY the spoken opening.
"""

    result = generate_ai_response(

        system_prompt=system_prompt,

        user_prompt=user_prompt,

    )

    if not result["success"]:

        return result

    opening = result[
        "response"
    ].strip()

    agent[
        "conversation"
    ].append({

        "role": "assistant",

        "content": opening,

    })

    agent[
        "status"
    ] = "Conversation Active"

    st.session_state[
        "voice_agent"
    ] = agent

    return {

        "success": True,

        "response": opening,

        "error": "",

    }


# ==========================================================
# ADD NOTE
# ==========================================================

def add_voice_note(note):

    agent = get_voice_agent()

    if not agent:

        return False

    if not note:

        return False

    agent[
        "notes"
    ].append(
        str(note)
    )

    st.session_state[
        "voice_agent"
    ] = agent

    return True


# ==========================================================
# SET OUTCOME
# ==========================================================

def set_call_outcome(
    outcome
):

    agent = get_voice_agent()

    if not agent:

        return False

    valid_outcomes = [

        "Interested",

        "Meeting Booked",

        "Callback Requested",

        "Not Interested",

        "No Answer",

        "Follow Up",

        "Closed",

    ]

    if outcome not in valid_outcomes:

        return False

    agent[
        "outcome"
    ] = outcome

    agent[
        "status"
    ] = "Completed"

    st.session_state[
        "voice_agent"
    ] = agent

    return True


# ==========================================================
# GET CONVERSATION
# ==========================================================

def get_conversation():

    agent = get_voice_agent()

    if not agent:

        return []

    return agent.get(
        "conversation",
        []
    )


# ==========================================================
# GET CALL SUMMARY
# ==========================================================

def get_call_summary():

    agent = get_voice_agent()

    if not agent:

        return {}

    return {

        "business": agent.get(
            "lead",
            {}
        ).get(
            "business_name",
            ""
        ),

        "industry": agent.get(
            "lead",
            {}
        ).get(
            "industry",
            ""
        ),

        "location": agent.get(
            "lead",
            {}
        ).get(
            "location",
            ""
        ),

        "lead_score": agent.get(
            "lead",
            {}
        ).get(
            "lead_score",
            0
        ),

        "service": agent.get(
            "service",
            ""
        ),

        "objective": agent.get(
            "objective",
            ""
        ),

        "tone": agent.get(
            "tone",
            ""
        ),

        "status": agent.get(
            "status",
            ""
        ),

        "outcome": agent.get(
            "outcome"
        ),

        "intent": agent.get(
            "intent",
            "Unknown"
        ),

        "interest_level": agent.get(
            "interest_level",
            "Unknown"
        ),

        "conversation": agent.get(
            "conversation",
            []
        ),

        "notes": agent.get(
            "notes",
            []
        ),

        "summary": agent.get(
            "summary",
            ""
        ),

    }
# ==========================================================
# GENERATE AI CALL SUMMARY
# ==========================================================

def generate_call_summary():

    agent = get_voice_agent()

    if not agent:

        return {
            "success": False,
            "summary": "",
            "error": "Voice agent is not initialized.",
        }

    conversation = agent.get(
        "conversation",
        []
    )

    if not conversation:

        return {
            "success": False,
            "summary": "",
            "error": "No conversation available.",
        }

    conversation_text = ""

    for message in conversation:

        role = message.get(
            "role",
            "unknown"
        )

        content = message.get(
            "content",
            ""
        )

        conversation_text += (
            f"{role.upper()}: {content}\n"
        )

    lead = agent.get(
        "lead",
        {}
    )

    business_name = lead.get(
        "business_name",
        "Business"
    )

    prompt = f"""
Create a concise CRM sales-call summary.

Business:
{business_name}

Service:
{agent.get("service", "")}

Objective:
{agent.get("objective", "")}

Conversation:

{conversation_text}

Detected intent:
{agent.get("intent", "Unknown")}

Interest level:
{agent.get("interest_level", "Unknown")}

Outcome:
{agent.get("outcome", "Unknown")}

Return a professional CRM summary.

Include:

1. What the prospect said
2. Main need or objection
3. Interest level
4. Recommended next step

Keep it concise.

Do not invent information.
"""

    result = generate_ai_response(

        system_prompt=(
            "You are a professional CRM sales analyst."
        ),

        user_prompt=prompt,

    )

    if not result["success"]:

        return {
            "success": False,
            "summary": "",
            "error": result["error"],
        }

    summary = result[
        "response"
    ].strip()

    agent[
        "summary"
    ] = summary

    st.session_state[
        "voice_agent"
    ] = agent

    return {

        "success": True,

        "summary": summary,

        "error": "",

    }
# ==========================================================
# SAVE VOICE CALL TO CRM
# ==========================================================

def save_voice_call_to_crm():

    agent = get_voice_agent()

    if not agent:

        return {
            "success": False,
            "error": (
                "Voice agent is not initialized."
            ),
        }

    lead = agent.get(
        "lead",
        {}
    )

    business_id = lead.get(
        "business_id"
    )

    if not business_id:

        return {
            "success": False,
            "error": (
                "Business ID is missing from the lead."
            ),
        }

    outcome = agent.get(
        "outcome",
        ""
    )

    intent = agent.get(
        "intent",
        "Unknown"
    )

    interest_level = agent.get(
        "interest_level",
        "Unknown"
    )

    summary = agent.get(
        "summary",
        ""
    )

    callback_requested = (
        outcome == "Callback Requested"
        or intent == "Callback"
    )

    saved = save_call_result(

        business_id=business_id,

        call_outcome=outcome,

        call_intent=intent,

        interest_level=interest_level,

        call_summary=summary,

        callback_requested=callback_requested,

    )

    if not saved:

        return {
            "success": False,
            "error": (
                "Unable to save call result to CRM."
            ),
        }

    agent[
        "status"
    ] = "Saved to CRM"

    st.session_state[
        "voice_agent"
    ] = agent

    return {

        "success": True,

        "error": "",

    }