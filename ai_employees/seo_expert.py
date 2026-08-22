import streamlit as st

from ai_employees.ai_provider import generate_ai_response


def show():

    st.title("📈 AI SEO Expert")

    st.caption(
        "Build a complete, business-specific SEO strategy, "
        "local SEO plan, keyword strategy and 30-day roadmap."
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
            key="seo_business_name"
        )

        business_type = st.text_input(
            "Business Type",
            placeholder="Example: Dentist, Real Estate, Gym",
            key="seo_business_type"
        )

        website = st.text_input(
            "Website",
            placeholder="https://example.com",
            key="seo_website"
        )

    with col2:

        city = st.text_input(
            "Target City",
            placeholder="Example: Lahore, Pakistan",
            key="seo_city"
        )

        target_audience = st.text_input(
            "Target Audience",
            placeholder="Example: Local patients aged 25-55",
            key="seo_audience"
        )

        seo_goal = st.selectbox(
            "Primary SEO Goal",
            [
                "Generate More Local Leads",
                "Increase Organic Traffic",
                "Rank Higher on Google",
                "Improve Local SEO",
                "Increase Website Visibility",
                "Generate More Calls",
                "Generate More Website Enquiries"
            ],
            key="seo_goal"
        )

    st.divider()

    # ==========================================================
    # CURRENT SEO SITUATION
    # ==========================================================

    st.subheader("🔎 Current SEO Situation")

    current_problems = st.text_area(
        "Current SEO Problems",
        placeholder=(
            "Example: Website gets very little traffic, "
            "not ranking on Google, weak Google Business Profile, "
            "few backlinks, poor content..."
        ),
        height=120,
        key="seo_problems"
    )

    competitors = st.text_area(
        "Known Competitors",
        placeholder=(
            "Optional: Enter competitor websites or names."
        ),
        height=100,
        key="seo_competitors"
    )

    additional_information = st.text_area(
        "Additional Business Information",
        placeholder=(
            "Services, locations served, special offers, "
            "USPs, pricing, certifications, etc."
        ),
        height=120,
        key="seo_extra"
    )

    st.divider()

    # ==========================================================
    # GENERATE
    # ==========================================================

    if st.button(
        "🚀 Generate Complete SEO Strategy",
        use_container_width=True,
        key="seo_generate"
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

        if not website.strip():

            st.warning(
                "Please enter the Website."
            )

            return

        if not city.strip():

            st.warning(
                "Please enter the Target City."
            )

            return

        # ======================================================
        # SYSTEM PROMPT
        # ======================================================

        system_prompt = """

You are an elite international SEO Consultant.

You work as an AI employee inside Growth Radar AI.

Your job is to create premium, practical and
business-specific SEO strategies.

Think like a senior SEO consultant charging
$5,000+ per month.

Never provide generic filler advice.

Use ONLY the information provided by the user.

Never invent website facts, rankings, traffic,
backlinks, competitors or technical problems.

If actual website data was not provided,
clearly label recommendations as recommended
actions rather than claiming they already exist.

Focus heavily on business outcomes:

- Organic traffic
- Local visibility
- Google rankings
- Leads
- Calls
- Enquiries
- Conversions

Write the final report in professional Markdown.

"""

        # ======================================================
        # USER PROMPT
        # ======================================================

        user_prompt = f"""

Create a complete SEO strategy for the following business.

==================================================
BUSINESS INFORMATION
==================================================

Business Name:
{business_name}

Business Type:
{business_type}

Website:
{website}

Target City:
{city}

Target Audience:
{
    target_audience
    if target_audience.strip()
    else "Not provided"
}

Primary SEO Goal:
{seo_goal}

Current SEO Problems:
{
    current_problems
    if current_problems.strip()
    else "Not provided"
}

Known Competitors:
{
    competitors
    if competitors.strip()
    else "Not provided"
}

Additional Information:
{
    additional_information
    if additional_information.strip()
    else "Not provided"
}


==================================================
CREATE THIS SEO REPORT
==================================================

# 1. SEO Executive Summary

Explain:

- Current opportunity
- Main SEO objective
- Biggest growth opportunity
- Recommended SEO direction


# 2. Business & Search Intent Analysis

Explain:

- What customers are likely searching for
- High-intent searches
- Commercial searches
- Informational searches
- Local searches
- Conversion-focused searches


# 3. Website SEO Audit

Since no live crawl data may be available, clearly separate:

- Known information
- Likely risks
- Recommended checks

Cover:

- Website structure
- Page quality
- Navigation
- UX
- Mobile experience
- Conversion elements
- Trust signals


# 4. Technical SEO

Provide a practical checklist covering:

- Indexing
- Crawlability
- Sitemap
- Robots.txt
- HTTPS
- Page speed
- Core Web Vitals
- Mobile usability
- Canonicals
- Redirects
- Broken links
- Structured data
- Image optimization


# 5. On-Page SEO

Explain how to optimize:

- Homepage
- Service pages
- Location pages
- Title tags
- Meta descriptions
- H1/H2 structure
- URLs
- Images
- Internal links
- CTAs


# 6. Local SEO Strategy

Create a detailed local SEO strategy for the target city.

Include:

- Local landing pages
- Local keywords
- NAP consistency
- Local citations
- Reviews
- Local content
- Location signals
- Local backlinks


# 7. Google Business Profile Strategy

Provide recommendations for:

- Business category
- Business description
- Services
- Photos
- Posts
- Reviews
- Q&A
- Profile completeness
- Review acquisition system


# 8. Keyword Strategy

Create 20 keyword opportunities.

For each keyword include:

- Keyword
- Search intent
- Funnel stage
- Recommended page
- Priority

Separate keywords into:

- Primary keywords
- Local keywords
- Service keywords
- Long-tail keywords


# 9. Content Strategy

Create:

- 5 SEO content pillars
- Content themes
- Search intent
- Recommended formats
- Conversion opportunities


# 10. Blog Ideas

Create 15 highly specific blog topics.

For each topic include:

- Title
- Search intent
- Primary keyword
- Supporting keywords
- CTA


# 11. Competitor SEO Strategy

Based only on competitor information provided.

Explain:

- What to investigate
- Keyword gaps
- Content gaps
- Backlink opportunities
- Local ranking opportunities
- Differentiation strategy

Do not invent competitor data.


# 12. Backlink Strategy

Create a practical backlink plan.

Include:

- Local directories
- Industry directories
- Local businesses
- Partnerships
- Guest content
- Digital PR
- Community opportunities
- Link-worthy content


# 13. Internal Linking Strategy

Explain:

- Which pages should link together
- Anchor text strategy
- Service-to-blog links
- Blog-to-service links
- Location-to-service links


# 14. Conversion SEO

Explain how SEO traffic should become:

Visitor
→ Engaged Visitor
→ Enquiry
→ Lead
→ Customer

Include:

- CTA strategy
- Contact forms
- Phone CTAs
- WhatsApp
- Booking
- Trust signals


# 15. 30-Day SEO Content Calendar

Create a day-by-day plan.

For every day include:

- Day
- Task
- Page/content
- Keyword
- SEO objective
- Expected outcome


# 16. 30-Day SEO Execution Plan

Divide into:

## Week 1 — Foundation

## Week 2 — On-Page SEO

## Week 3 — Content & Local SEO

## Week 4 — Authority & Optimization


# 17. Priority Fixes

Give the top 10 SEO actions.

Rank them:

1 = Highest priority

10 = Lowest priority

For every action explain:

- What to do
- Why it matters
- Expected business impact


# 18. SEO KPI Dashboard

Recommend KPIs for:

### Visibility

- Impressions
- Rankings
- Search visibility

### Traffic

- Organic sessions
- Landing page traffic

### Leads

- Calls
- Forms
- WhatsApp enquiries
- Bookings

### Conversion

- Lead conversion rate
- Cost per organic lead
- Customer acquisition


# 19. Final Consultant Recommendation

Finish with:

- Biggest opportunity
- Biggest risk
- First 3 actions to take
- 30-day priority
- 90-day direction

IMPORTANT:

Be specific.

Do not say only "improve SEO".

Explain exactly:

WHAT to do,
WHERE to do it,
WHY it matters,
and HOW it can contribute to business growth.

"""

        # ======================================================
        # GENERATE AI
        # ======================================================

        with st.spinner(
            "🤖 AI SEO Expert is building your strategy..."
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
                "seo_strategy"
            ] = result["response"]

            st.session_state[
                "seo_strategy_business"
            ] = business_name

            if result.get("demo"):

                st.info(
                    "ℹ️ Demo AI mode is active. "
                    "The SEO strategy engine is working "
                    "without paid AI credits."
                )

            st.success(
                "✅ Complete SEO Strategy Generated."
            )

        else:

            st.error(
                f"❌ AI Error: {result['error']}"
            )

    # ==========================================================
    # DISPLAY RESULT
    # ==========================================================

    strategy = st.session_state.get(
        "seo_strategy"
    )

    strategy_business = st.session_state.get(
        "seo_strategy_business",
        business_name
        if "business_name" in locals()
        else ""
    )

    if strategy:

        st.divider()

        st.subheader(
            f"📋 SEO Strategy — {strategy_business}"
        )

        st.markdown(strategy)

        st.divider()

        st.download_button(
            "📥 Download SEO Strategy",
            data=strategy,
            file_name=(
                f"{strategy_business}_seo_strategy.md"
            ),
            mime="text/markdown",
            use_container_width=True
        )