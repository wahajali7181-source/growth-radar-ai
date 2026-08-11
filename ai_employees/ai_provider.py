import os

import streamlit as st


# ==========================================================
# AI PROVIDER CONFIGURATION
# ==========================================================

def get_openai_api_key():

    # First try Streamlit secrets
    try:

        key = st.secrets.get(
            "OPENAI_API_KEY",
            ""
        )

        if key:

            return key

    except Exception:

        pass

    # Then try environment variable
    return os.getenv(
        "OPENAI_API_KEY",
        ""
    )


# ==========================================================
# DEMO MODE
# ==========================================================

def is_demo_mode():

    return True


# ==========================================================
# CHECK AI AVAILABILITY
# ==========================================================

def is_ai_available():

    return bool(
        get_openai_api_key()
    )


# ==========================================================
# DEMO RESPONSE
# ==========================================================

def generate_demo_response(
    system_prompt,
    user_prompt,
):

    prompt = user_prompt.lower()

    # ------------------------------------------------------
    # OPENING
    # ------------------------------------------------------

    if (
        "opening line" in prompt
        or "opening" in prompt
    ):

        return {
            "success": True,

            "response": (
                "Hi, this is Wahaj from Growth Radar AI. "
                "I’m reaching out because we help businesses "
                "improve their online growth and lead generation. "
                "Do you have a quick minute?"
            ),

            "error": "",

            "demo": True,
        }

    # ------------------------------------------------------
    # COMMON OBJECTIONS
    # ------------------------------------------------------

    if (
        "already have" in prompt
        or "someone handling" in prompt
        or "already working" in prompt
    ):

        response = (
            "Absolutely, I understand. A lot of businesses "
            "we speak with already have someone handling their "
            "marketing. I'm not looking to replace them "
            "immediately. I'd simply like to understand what "
            "you're currently doing and see if there is an area "
            "where we could add value. Would that be worth a "
            "quick conversation?"
        )

    elif (
        "not interested" in prompt
        or "not interested" in user_prompt.lower()
    ):

        response = (
            "No problem at all. I appreciate your time. "
            "If things change in the future, we'd be happy "
            "to help. Have a great day."
        )

    elif (
        "too expensive" in prompt
        or "expensive" in prompt
        or "budget" in prompt
    ):

        response = (
            "I completely understand. Budget is important. "
            "Before discussing pricing, it would make sense "
            "to understand your current goals and see whether "
            "there is actually a potential return for you. "
            "Would you be open to a short discussion about that?"
        )

    elif (
        "send email" in prompt
        or "send me information" in prompt
        or "email me" in prompt
    ):

        response = (
            "Absolutely. I can send you a concise overview "
            "with the key details. What would be the best "
            "email address to send it to?"
        )

    elif (
        "interested" in prompt
        or "sounds good" in prompt
        or "tell me more" in prompt
    ):

        response = (
            "Great. I'd be happy to explain. We first look at "
            "where your business is currently getting customers "
            "from, identify the biggest growth opportunities, "
            "and then recommend the most practical approach. "
            "What is your biggest challenge with getting new "
            "customers right now?"
        )

    elif (
        "meeting" in prompt
        or "call tomorrow" in prompt
        or "schedule" in prompt
    ):

        response = (
            "That sounds good. Let's arrange a short meeting "
            "so we can understand your goals and show you "
            "exactly what we could do. What day and time "
            "would work best for you?"
        )

    else:

        response = (
            "That's a good point. I'd like to understand your "
            "business a little better before recommending "
            "anything. What is the main challenge you're "
            "currently facing with your marketing or customer "
            "acquisition?"
        )

    return {

        "success": True,

        "response": response,

        "error": "",

        "demo": True,

    }


# ==========================================================
# AI RESPONSE
# ==========================================================

def generate_ai_response(
    system_prompt,
    user_prompt,
    model="gpt-4o-mini",
):

    api_key = get_openai_api_key()

    # ======================================================
    # NO API KEY
    # ======================================================

    if not api_key:

        if is_demo_mode():

            return generate_demo_response(
                system_prompt,
                user_prompt,
            )

        return {

            "success": False,

            "response": "",

            "error": (
                "OPENAI_API_KEY is not configured."
            ),

        }

    try:

        from openai import OpenAI

        client = OpenAI(
            api_key=api_key
        )

        response = client.chat.completions.create(

            model=model,

            messages=[

                {
                    "role": "system",
                    "content": system_prompt,
                },

                {
                    "role": "user",
                    "content": user_prompt,
                },

            ],

            temperature=0.7,

        )

        content = (
            response.choices[0]
            .message
            .content
        )

        return {

            "success": True,

            "response": content or "",

            "error": "",

            "demo": False,

        }

    except Exception as e:

        error_text = str(e)

        # ==================================================
        # API QUOTA / CREDIT EXHAUSTED
        # ==================================================

        quota_error = (

            "insufficient_quota" in error_text.lower()

            or "credit_balance_exhausted"
            in error_text.lower()

            or "no credits remaining"
            in error_text.lower()

            or "quota" in error_text.lower()

        )

        if quota_error and is_demo_mode():

            return generate_demo_response(

                system_prompt,

                user_prompt,

            )

        return {

            "success": False,

            "response": "",

            "error": error_text,

        }


# ==========================================================
# SIMPLE AI GENERATOR
# ==========================================================

def ask_ai(
    prompt,
    system_prompt=(
        "You are a professional B2B sales assistant."
    ),
):

    result = generate_ai_response(

        system_prompt=system_prompt,

        user_prompt=prompt,

    )

    if not result["success"]:

        return None

    return result["response"]