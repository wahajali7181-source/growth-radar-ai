import streamlit as st

from ai_employees.ai_provider import generate_ai_response


def show():

    st.title("📱 AI Social Media Manager")

    st.caption(
        "Build a complete, business-specific social media "
        "strategy, content calendar and growth plan."
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
            key="smm_business_name"
        )

        industry = st.text_input(
            "Industry",
            placeholder="Example: Dentist, Real Estate, Gym",
            key="smm_industry"
        )

        location = st.text_input(
            "Location",
            placeholder="Example: Lahore, Pakistan",
            key="smm_location"
        )

    with col2:

        website = st.text_input(
            "Website",
            placeholder="https://example.com",
            key="smm_website"
        )

        target_audience = st.text_input(
            "Target Audience",
            placeholder="Example: Local homeowners aged 30-55",
            key="smm_target_audience"
        )

        business_goal = st.selectbox(

            "Main Business Goal",

            [
                "Generate More Leads",
                "Increase Brand Awareness",
                "Increase Engagement",
                "Grow Followers",
                "Promote Services",
                "Generate Website Traffic",
                "Build Trust & Authority"
            ],

            key="smm_goal"
        )

    st.divider()

    # ==========================================================
    # SOCIAL PLATFORMS
    # ==========================================================

    st.subheader("📱 Social Media Platforms")

    platforms = st.multiselect(

        "Select platforms you want to focus on",

        [
            "Instagram",
            "Facebook",
            "LinkedIn",
            "TikTok",
            "YouTube",
            "X / Twitter"
        ],

        default=[
            "Instagram",
            "Facebook"
        ],

        key="smm_platforms"

    )

    # ==========================================================
    # CURRENT PROBLEMS
    # ==========================================================

    st.subheader("⚠️ Current Social Media Situation")

    social_problems = st.text_area(

        "What problems are you currently facing?",

        placeholder=(
            "Example: Low engagement, very few leads, "
            "inconsistent posting, no clear content strategy..."
        ),

        height=120,

        key="smm_problems"

    )

    # ==========================================================
    # ADDITIONAL INFORMATION
    # ==========================================================

    additional_information = st.text_area(

        "Additional Business Information",

        placeholder=(
            "Services, offers, competitors, unique selling points, "
            "pricing, audience details, etc."
        ),

        height=120,

        key="smm_extra"

    )

    st.divider()

    # ==========================================================
    # VALIDATION
    # ==========================================================

    if st.button(

        "🚀 Generate Complete Social Media Strategy",

        use_container_width=True,

        key="smm_generate"

    ):

        if not business_name.strip():

            st.warning(
                "Please enter the Business Name."
            )

            return

        if not industry.strip():

            st.warning(
                "Please enter the Industry."
            )

            return

        if not platforms:

            st.warning(
                "Please select at least one social media platform."
            )

            return

        # ======================================================
        # PLATFORM TEXT
        # ======================================================

        platform_text = ", ".join(
            platforms
        )

        # ======================================================
        # SYSTEM PROMPT
        # ======================================================

        system_prompt = """

You are an elite senior Social Media Marketing Manager.

You work as an AI employee inside Growth Radar AI.

Your job is to create practical, specific and
conversion-focused social media strategies.

Never give generic filler advice.

Use the business information provided by the user.

Do not invent facts about the business.

If information is missing, clearly state that
the information was not provided.

Think like a senior marketing strategist,
content strategist and social media growth manager.

Your recommendations must focus on business outcomes,
not vanity metrics only.

Write the final answer in professional Markdown.

"""

        # ======================================================
        # USER PROMPT
        # ======================================================

        user_prompt = f"""

Create a complete social media marketing strategy
for the following business.

==================================================
BUSINESS INFORMATION
==================================================

Business Name:
{business_name}

Industry:
{industry}

Location:
{location if location.strip() else "Not provided"}

Website:
{website if website.strip() else "Not provided"}

Target Audience:
{
    target_audience
    if target_audience.strip()
    else "Not provided"
}

Main Business Goal:
{business_goal}

Social Platforms:
{platform_text}

Current Social Media Problems:
{
    social_problems
    if social_problems.strip()
    else "Not provided"
}

Additional Business Information:
{
    additional_information
    if additional_information.strip()
    else "Not provided"
}


==================================================
CREATE THIS REPORT
==================================================


# 1. Social Media Executive Summary

Give a short strategic assessment of the business
and explain the most important social media opportunity.


# 2. Target Audience

Explain:

- Primary audience
- Secondary audience
- Customer needs
- Pain points
- Buying motivations
- Content that is likely to attract them


# 3. Brand Positioning

Explain:

- How the brand should position itself
- Core message
- Trust-building angle
- Differentiation strategy
- Recommended tone of voice


# 4. Social Media Strategy

Create an overall strategy based on the business goal.

Explain:

- Awareness
- Engagement
- Lead generation
- Conversion
- Retention


# 5. Platform Strategy

Create a separate strategy for every selected platform.

For each platform include:

## Content Types

## Posting Frequency

## Best Content Formats

## Growth Strategy

## Lead Generation Strategy

## CTA Strategy


# 6. Content Pillars

Create 5 strong content pillars.

For every pillar include:

- Pillar name
- Purpose
- Content examples
- Business objective


# 7. 30-Day Content Calendar

Create a complete 30-day calendar.

For EVERY day include:

- Day
- Platform
- Content format
- Topic
- Hook
- Main idea
- CTA

Make the topics specific to this business.

Do not repeat the same idea unnecessarily.


# 8. Reel / Short-Form Video Ideas

Create 10 short-form video ideas.

For every idea include:

- Hook
- Video concept
- Suggested structure
- CTA


# 9. Caption Strategy

Explain how captions should be written.

Then provide 5 example captions
specific to this business.


# 10. Lead Generation Strategy

Explain how social media can generate actual customers.

Include:

- Lead magnets
- DM strategy
- CTA strategy
- Offer strategy
- Landing page strategy
- Follow-up strategy


# 11. Engagement Strategy

Explain how to increase:

- Comments
- Shares
- Saves
- DMs
- Community interaction


# 12. Growth Strategy

Explain:

- Organic growth
- Collaboration opportunities
- User-generated content
- Community building
- Short-form video strategy


# 13. Conversion Strategy

Explain how to turn:

Follower
→ Engaged follower
→ Lead
→ Customer


# 14. KPI Dashboard

Recommend the most important KPIs.

Separate:

- Awareness KPIs
- Engagement KPIs
- Lead KPIs
- Conversion KPIs


# 15. 30-Day Execution Plan

Break the strategy into:

Week 1:
Foundation

Week 2:
Content & Engagement

Week 3:
Lead Generation

Week 4:
Optimization & Conversion


# 16. Priority Actions

Finish with the 10 most important actions
the business should take immediately.

Rank them from highest priority to lowest priority.


IMPORTANT:

Make everything practical.

Avoid generic statements like
"post consistently" unless you explain
exactly what should be posted, where,
how often and why.

"""

        # ======================================================
        # GENERATE AI
        # ======================================================

        with st.spinner(
            "🤖 AI Social Media Manager is building your strategy..."
        ):

            result = generate_ai_response(

                system_prompt=system_prompt,

                user_prompt=user_prompt

            )

        # ======================================================
        # HANDLE RESULT
        # ======================================================

        if result["success"]:

            st.session_state[
                "social_media_strategy"
            ] = result["response"]

            st.session_state[
                "social_media_strategy_business"
            ] = business_name

            if result.get("demo"):

                st.info(
                    "ℹ️ Demo AI mode is active. "
                    "The strategy engine is working without paid AI credits."
                )

            st.success(
                "✅ Complete Social Media Strategy Generated."
            )

        else:

            st.error(
                f"❌ AI Error: {result['error']}"
            )

    # ==========================================================
    # DISPLAY RESULT
    # ==========================================================

    strategy = st.session_state.get(
        "social_media_strategy"
    )

    strategy_business = st.session_state.get(
        "social_media_strategy_business",
        business_name if "business_name" in locals() else ""
    )

    if strategy:

        st.divider()

        st.subheader(
            f"📋 Social Media Strategy — {strategy_business}"
        )

        st.markdown(
            strategy
        )

        st.divider()

        # ======================================================
        # DOWNLOAD
        # ======================================================

        st.download_button(

            "📥 Download Strategy",

            data=strategy,

            file_name=(
                f"{strategy_business}_social_media_strategy.md"
            ),

            mime="text/markdown",

            use_container_width=True

        )