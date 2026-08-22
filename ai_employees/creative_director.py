import streamlit as st

from ai_employees.ai_client import generate_response


def _build_prompt(
    business_name,
    business_type,
    offer,
    target_city,
    target_audience,
    platform,
    campaign_goal,
    monthly_budget,
    brand_tone,
    additional_information,
):
    return f"""
Create a complete, premium advertising creative strategy.

BUSINESS INFORMATION
--------------------
Business Name:
{business_name}

Business Type:
{business_type}

Offer:
{offer if offer.strip() else "Not provided"}

Target City:
{target_city if target_city.strip() else "Not provided"}

Target Audience:
{target_audience if target_audience.strip() else "Not provided"}

Platform:
{platform}

Campaign Goal:
{campaign_goal}

Monthly Budget:
{monthly_budget}

Brand Tone:
{brand_tone}

Additional Information:
{additional_information if additional_information.strip() else "Not provided"}


YOUR ROLE
---------
You are the Creative Director and paid advertising strategist
inside Growth Radar AI.

Think like a senior creative strategist working with established
brands.

Your job is to create advertising concepts that can realistically
generate attention, leads, enquiries and sales.

Never invent business facts.

If information is missing, clearly label it as:
- Recommended
- Suggested
- To be tested
- To be confirmed

Do not claim that a campaign has already generated results.

Do not guarantee leads, sales, ROAS or revenue.

Every recommendation should follow:

WHAT → WHY → EXPECTED BUSINESS IMPACT


CREATE THE FOLLOWING


# 1. Creative Strategy

Explain:
- Core marketing angle
- Main customer pain point
- Desired customer action
- Main value proposition
- Primary creative direction
- Recommended communication style


# 2. Campaign Strategy

Recommend:
- Campaign objective
- Funnel stage
- Recommended campaign structure
- Prospecting strategy
- Retargeting strategy
- Conversion strategy


# 3. Audience Strategy

Include:
- Primary audience
- Secondary audience
- Age recommendation
- Geographic targeting
- Customer intent
- Pain points
- Buying motivations
- Objections


# 4. Audience Testing

Create at least 5 audience testing ideas.

For each:
- Audience
- Why test it
- Creative angle
- Expected purpose


# 5. Budget Strategy

Explain how the supplied budget could be distributed between:

- Prospecting
- Retargeting
- Creative testing
- Winning campaign scaling

Clearly label percentages as recommendations,
not guaranteed optimal allocations.


# 6. Creative Angles

Create 7 different advertising angles.

Examples:
- Problem → Solution
- Transformation
- Social Proof
- Educational
- Offer
- Fear of missing out
- Convenience

For every angle explain:
- Hook
- Core message
- Visual direction
- CTA


# 7. Ad Headlines

Create 10 strong headlines.

Keep them:
- Clear
- Specific
- Benefit-focused
- Suitable for paid advertising


# 8. Primary Ad Copy

Create 5 different versions:

### Version 1 — Direct Response

### Version 2 — Problem / Solution

### Version 3 — Educational

### Version 4 — Trust Building

### Version 5 — Offer Focused


# 9. CTA Strategy

Recommend 5 CTA options.

Explain when each CTA should be used.


# 10. Facebook Creative

Create one complete Facebook ad concept.

Include:
- Hook
- Main message
- Visual concept
- Headline
- Primary text
- CTA


# 11. Instagram Creative

Create one Instagram-focused concept.

Include:
- Visual direction
- Hook
- Caption
- CTA
- On-screen text


# 12. Carousel Ad

Create a 6-card carousel.

For every card provide:
- Card headline
- Supporting text
- Visual idea
- CTA or transition


# 13. Short Video Advertisement

Create a 30-second video ad.

Use this structure:

0–3 sec:
Hook

3–8 sec:
Problem

8–15 sec:
Solution

15–23 sec:
Benefits / proof concept

23–27 sec:
Offer

27–30 sec:
CTA

Include:
- Voiceover
- On-screen text
- Visual direction


# 14. Reel Script

Create a 30–45 second Reel.

Include:
- Hook
- Scene-by-scene direction
- Dialogue/voiceover
- On-screen text
- B-roll suggestions
- CTA


# 15. UGC Ad Concept

Create one realistic UGC-style advertisement.

Include:
- Creator opening
- Problem
- Personal experience
- Solution
- CTA


# 16. Image Generation Prompt

Create one detailed prompt suitable for an image-generation model.

The prompt must specify:
- Subject
- Composition
- Environment
- Lighting
- Camera angle
- Mood
- Brand positioning
- Text placement area

Do not generate fake testimonials or fake results.


# 17. Canva Design Prompt

Create a practical Canva design specification.

Include:
- Canvas size
- Layout
- Typography direction
- Visual hierarchy
- Image placement
- CTA placement
- Brand elements


# 18. Creative Testing Matrix

Create 5 tests.

Columns:

| Test | Variable A | Variable B | What We Learn |

Test:
- Hook
- Creative format
- Offer
- CTA
- Audience angle


# 19. Marketing Psychology

Explain the psychological principles behind the campaign.

Cover:
- Attention
- Pain
- Desire
- Trust
- Proof
- Urgency
- Action


# 20. 30-Day Creative Plan

Create a practical 30-day plan.

For every day include:
- Day
- Creative task
- Content/ad format
- Objective
- CTA


# 21. Final Creative Director Recommendation

Finish with:

- Best creative angle
- Best audience to test first
- Best format to launch first
- First 3 creatives to produce
- Biggest testing priority
- Recommended next action


IMPORTANT
---------
Make this practical enough that a marketing team can directly
turn the strategy into ads, graphics, videos and campaigns.

Return ONLY clean Markdown.

NEVER wrap the complete response inside a markdown code block.
"""


def show():

    st.title("🎨 AI Creative Director")

    st.caption(
        "Create complete advertising concepts, Meta campaigns, "
        "creative assets, scripts and testing strategies."
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
            key="creative_business_name",
        )

        business_type = st.text_input(
            "Business Type",
            placeholder="Example: Dentist, Real Estate, Gym",
            key="creative_business_type",
        )

        offer = st.text_input(
            "Offer",
            placeholder="Example: 20% OFF, Free Consultation",
            key="creative_offer",
        )

        target_city = st.text_input(
            "Target City",
            placeholder="Example: Lahore, Pakistan",
            key="creative_city",
        )

    with col2:

        target_audience = st.text_input(
            "Target Audience",
            placeholder="Example: Local patients aged 25–55",
            key="creative_audience",
        )

        platform = st.selectbox(
            "Primary Platform",
            [
                "Facebook",
                "Instagram",
                "Facebook + Instagram",
            ],
            key="creative_platform",
        )

        campaign_goal = st.selectbox(
            "Campaign Goal",
            [
                "Generate Leads",
                "Generate Sales",
                "Increase Website Enquiries",
                "Generate Calls",
                "Increase Bookings",
                "Brand Awareness",
                "Retarget Existing Visitors",
            ],
            key="creative_campaign_goal",
        )

        monthly_budget = st.selectbox(
            "Monthly Advertising Budget",
            [
                "$300",
                "$500",
                "$1,000",
                "$2,000",
                "$5,000",
                "Custom",
            ],
            key="creative_budget",
        )

    brand_tone = st.selectbox(
        "Brand Tone",
        [
            "Professional",
            "Premium",
            "Friendly",
            "Modern",
            "Bold",
            "Trustworthy",
            "Educational",
        ],
        key="creative_brand_tone",
    )

    additional_information = st.text_area(
        "Additional Business Information",
        placeholder=(
            "Services, USP, pricing, certifications, "
            "special features, existing creative ideas, etc."
        ),
        height=120,
        key="creative_extra",
    )

    st.divider()

    # ==========================================================
    # GENERATE
    # ==========================================================

    if st.button(
        "🚀 Generate Complete Creative Campaign",
        use_container_width=True,
        key="creative_generate",
    ):

        if not business_name.strip():

            st.warning("Please enter the Business Name.")
            return

        if not business_type.strip():

            st.warning("Please enter the Business Type.")
            return

        prompt = _build_prompt(
            business_name=business_name,
            business_type=business_type,
            offer=offer,
            target_city=target_city,
            target_audience=target_audience,
            platform=platform,
            campaign_goal=campaign_goal,
            monthly_budget=monthly_budget,
            brand_tone=brand_tone,
            additional_information=additional_information,
        )

        with st.spinner(
            "🎨 AI Creative Director is building the campaign..."
        ):

            result = generate_response(
                prompt=prompt,
                system_prompt="""
You are a senior international Creative Director,
performance advertising strategist and campaign architect
inside Growth Radar AI.

Create premium, practical and conversion-focused advertising
strategies.

Never invent business facts.

Never claim existing campaign performance unless it was
explicitly supplied.

Never guarantee results.

When information is missing, provide recommendations and
testing hypotheses instead.

Use WHAT → WHY → BUSINESS IMPACT.

Think creatively, but keep every recommendation realistic.

Return ONLY clean Markdown.

Never wrap the complete response inside a markdown code block.
""",
            )

        if not result:

            st.error(
                "❌ Creative Director returned an empty response."
            )

            return

        st.session_state[
            "creative_director_result"
        ] = result

        st.session_state[
            "creative_director_business"
        ] = business_name

        st.success(
            "✅ Complete Creative Campaign Generated."
        )

    # ==========================================================
    # DISPLAY RESULT
    # ==========================================================

    result = st.session_state.get(
        "creative_director_result"
    )

    result_business = st.session_state.get(
        "creative_director_business",
        "",
    )

    if result:

        st.divider()

        st.subheader(
            f"📋 Creative Campaign — {result_business}"
        )

        st.markdown(result)

        st.divider()

        st.download_button(
            "📥 Download Creative Strategy",
            data=result,
            file_name=(
                f"{result_business}_creative_strategy.md"
            ),
            mime="text/markdown",
            use_container_width=True,
        )