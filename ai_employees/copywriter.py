import streamlit as st

from ai_employees.ai_provider import generate_ai_response


def show():

    st.title("✍️ AI Copywriter")

    st.caption(
        "Create high-converting marketing copy for websites, "
        "ads, social media, emails and business campaigns."
    )

    st.divider()

    # ==========================================================
    # BUSINESS INFORMATION
    # ==========================================================

    st.subheader("🏢 Business Information")

    col1, col2 = st.columns(2)

    with col1:

        business_name = st.text_input(
            "Business Name",
            placeholder="Example: Bright Dental Clinic",
            key="copy_business_name"
        )

        business_type = st.text_input(
            "Business Type",
            placeholder="Example: Dentist, Real Estate, Gym",
            key="copy_business_type"
        )

    with col2:

        target_audience = st.text_input(
            "Target Audience",
            placeholder="Example: Local patients aged 25-55",
            key="copy_target_audience"
        )

        location = st.text_input(
            "Target Location",
            placeholder="Example: Lahore, Pakistan",
            key="copy_location"
        )

    st.divider()

    # ==========================================================
    # COPY TYPE
    # ==========================================================

    st.subheader("📝 Copy Requirements")

    copy_type = st.selectbox(
        "What do you want to create?",
        [
            "Facebook Ad",
            "Instagram Ad",
            "Google Ad",
            "Social Media Post",
            "Instagram Caption",
            "Website Homepage",
            "Landing Page",
            "Product Description",
            "Email",
            "Cold Outreach Message",
            "Sales Message",
            "Video / Reel Script",
            "Headline & Hook",
            "Call To Action",
            "Custom Copy",
        ],
        key="copy_type"
    )

    tone = st.selectbox(
        "Tone",
        [
            "Professional",
            "Persuasive",
            "Friendly",
            "Premium",
            "Bold",
            "Trustworthy",
            "Emotional",
            "Educational",
            "Conversational",
        ],
        key="copy_tone"
    )

    objective = st.selectbox(
        "Primary Objective",
        [
            "Generate Leads",
            "Generate Sales",
            "Get More Calls",
            "Get More Bookings",
            "Increase Engagement",
            "Build Trust",
            "Increase Brand Awareness",
            "Drive Website Traffic",
            "Promote an Offer",
        ],
        key="copy_objective"
    )

    st.divider()

    # ==========================================================
    # OFFER / DETAILS
    # ==========================================================

    st.subheader("🎯 Campaign Details")

    offer = st.text_area(
        "Offer / Service / Product",
        placeholder=(
            "Example: Teeth whitening, free consultation, "
            "20% discount for new patients..."
        ),
        height=100,
        key="copy_offer"
    )

    key_points = st.text_area(
        "Important Details / USPs",
        placeholder=(
            "Enter the important things you want included. "
            "Example: experienced team, convenient location, "
            "same-day appointments..."
        ),
        height=120,
        key="copy_key_points"
    )

    additional_instructions = st.text_area(
        "Additional Instructions",
        placeholder=(
            "Optional. Tell the AI exactly what you want "
            "included or avoided."
        ),
        height=100,
        key="copy_instructions"
    )

    st.divider()

    # ==========================================================
    # GENERATE
    # ==========================================================

    if st.button(
        "🚀 Generate Copy",
        use_container_width=True,
        key="copy_generate"
    ):

        if not business_name.strip():

            st.warning(
                "Please enter the Business Name."
            )

            return

        if not business_type.strip():

            st.warning(
                "Please enter the Business Type."
            )

            return

        if not target_audience.strip():

            st.warning(
                "Please enter the Target Audience."
            )

            return

        if not offer.strip():

            st.warning(
                "Please enter the Offer / Service / Product."
            )

            return

        # ======================================================
        # SYSTEM PROMPT
        # ======================================================

        system_prompt = """
You are an elite international marketing copywriter.

You work as the AI Copywriter inside Growth Radar AI.

Your job is to create persuasive, professional and
conversion-focused marketing copy.

Think like a senior copywriter working with premium
international brands.

QUALITY RULES:

1. Use ONLY information provided by the user.

2. NEVER invent:
- prices
- discounts
- guarantees
- testimonials
- statistics
- awards
- certifications
- customer numbers
- business achievements
- product features

unless explicitly provided.

3. Do not make unsupported claims.

4. Write specifically for the supplied:
- business
- industry
- audience
- location
- offer
- objective
- tone

5. Focus on the desired business outcome.

6. Use strong hooks and clear messaging.

7. Avoid generic filler.

8. Make the copy natural and human.

9. Do not sound robotic or overly AI-generated.

10. Use clear calls to action.

11. Do not mention that you are an AI.

12. Do not mention internal Growth Radar AI systems.

13. Return clean Markdown only.

14. Do not wrap the entire response inside a markdown code block.

COPY STRUCTURE:

Hook
→ Problem / Desire
→ Value
→ Offer
→ Trust / Reason to Act
→ Call To Action

Adapt the structure naturally to the requested copy type.

For ads:
- Give multiple hooks where useful.
- Keep the copy platform-appropriate.
- Make the CTA clear.

For website copy:
- Focus on clarity, trust and conversion.
- Use useful headings and sections.

For social media:
- Make the opening line strong.
- Keep the content engaging.
- Include an appropriate CTA.

For emails:
- Provide a subject line.
- Write a strong opening.
- Keep the message concise and persuasive.

For video scripts:
- Start with a strong hook.
- Build curiosity.
- Deliver the value.
- Finish with a CTA.
"""

        # ======================================================
        # USER PROMPT
        # ======================================================

        user_prompt = f"""
Create high-converting marketing copy.

==================================================
BUSINESS
==================================================

Business Name:
{business_name}

Business Type:
{business_type}

Target Audience:
{target_audience}

Location:
{location if location.strip() else "Not provided"}

==================================================
COPY REQUIREMENTS
==================================================

Copy Type:
{copy_type}

Tone:
{tone}

Primary Objective:
{objective}

Offer / Service / Product:
{offer}

Important Details / USPs:
{
    key_points
    if key_points.strip()
    else "Not provided"
}

Additional Instructions:
{
    additional_instructions
    if additional_instructions.strip()
    else "Not provided"
}

==================================================
TASK
==================================================

Create the best possible copy for this business.

Make it:

- Specific
- Persuasive
- Clear
- Human
- Conversion-focused
- Appropriate for the selected platform
- Appropriate for the target audience

Explain or present the copy in a way that the business
owner can immediately use.

Do not invent facts.

"""

        # ======================================================
        # GENERATE AI
        # ======================================================

        with st.spinner(
            "🤖 AI Copywriter is creating your copy..."
        ):

            result = generate_ai_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )

        # ======================================================
        # HANDLE RESULT
        # ======================================================

        if result["success"]:

            copy_result = result["response"]

            st.session_state[
                "copywriter_result"
            ] = copy_result

            st.session_state[
                "copywriter_business"
            ] = business_name

            if result.get("demo"):

                st.info(
                    "ℹ️ Demo AI mode is active."
                )

            st.success(
                "✅ Marketing Copy Generated."
            )

        else:

            st.error(
                f"❌ AI Error: {result.get('error', 'Unknown error')}"
            )

    # ==========================================================
    # DISPLAY RESULT
    # ==========================================================

    copy_result = st.session_state.get(
        "copywriter_result"
    )

    result_business = st.session_state.get(
        "copywriter_business",
        business_name
        if "business_name" in locals()
        else ""
    )

    if copy_result:

        st.divider()

        st.subheader(
            f"📋 Copy — {result_business}"
        )

        st.markdown(copy_result)

        st.divider()

        st.download_button(
            "📥 Download Copy",
            data=copy_result,
            file_name=(
                f"{result_business}_copy.md"
            ),
            mime="text/markdown",
            use_container_width=True
        )