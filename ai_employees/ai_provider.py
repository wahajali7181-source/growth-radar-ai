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
    # ======================================================
    # SEO CONSULTANT
    # ======================================================

    if (
        "complete seo strategy" in prompt
        or "seo strategy" in prompt
        or "seo consultant" in system_prompt.lower()
    ):

        # --------------------------------------------------
        # Extract business information
        # --------------------------------------------------

        business_name = "the business"
        business_type = "the business type"
        website = "Not provided"
        city = "the target city"
        audience = "local customers"
        seo_goal = "Improve organic visibility"

        for line in user_prompt.splitlines():

            line_clean = line.strip()

            if line_clean.startswith("Business Name:"):
                value = line_clean.split(
                    "Business Name:",
                    1
                )[1].strip()

                if value:
                    business_name = value

            elif line_clean.startswith("Business Type:"):
                value = line_clean.split(
                    "Business Type:",
                    1
                )[1].strip()

                if value:
                    business_type = value

            elif line_clean.startswith("Website:"):
                value = line_clean.split(
                    "Website:",
                    1
                )[1].strip()

                if value:
                    website = value

            elif line_clean.startswith("Target City:"):
                value = line_clean.split(
                    "Target City:",
                    1
                )[1].strip()

                if value:
                    city = value

            elif line_clean.startswith("Target Audience:"):
                value = line_clean.split(
                    "Target Audience:",
                    1
                )[1].strip()

                if value:
                    audience = value

            elif line_clean.startswith("Primary SEO Goal:"):
                value = line_clean.split(
                    "Primary SEO Goal:",
                    1
                )[1].strip()

                if value:
                    seo_goal = value

        # --------------------------------------------------
        # Industry-specific SEO data
        # --------------------------------------------------

        industry = business_type.lower()

        if "dent" in industry:

            primary_keywords = [
                f"dentist in {city}",
                f"dental clinic in {city}",
                f"best dentist in {city}",
                f"dental clinic near me",
                f"dentist near me"
            ]

            service_keywords = [
                f"teeth whitening in {city}",
                f"dental implants in {city}",
                f"root canal dentist in {city}",
                f"cosmetic dentist in {city}",
                f"emergency dentist in {city}"
            ]

            long_tail_keywords = [
                f"affordable dentist in {city}",
                f"best dental clinic for families in {city}",
                f"dentist for teeth cleaning in {city}",
                f"how much does a dentist cost in {city}",
                f"how to choose a dentist in {city}"
            ]

            content_topics = [
                "Complete guide to choosing a dentist",
                "How often should you visit a dentist?",
                "Common signs you need a dental checkup",
                "Teeth whitening: what patients should know",
                "Dental implants explained",
                "Root canal treatment explained",
                "How to prevent cavities",
                "Best dental hygiene habits",
                "What to do during a dental emergency",
                "Questions to ask before choosing a dentist"
            ]

            local_actions = [
                f"Create a dedicated dentist page targeting {city}",
                f"Create service pages targeting {city}",
                f"Optimize Google Business Profile for {city}",
                "Build consistent local citations",
                "Collect genuine patient reviews",
                "Publish locally relevant dental content",
                "Add clear NAP information",
                "Build relationships with relevant local organizations"
            ]

        elif "real estate" in industry or "property" in industry:

            primary_keywords = [
                f"real estate agent in {city}",
                f"real estate company in {city}",
                f"properties for sale in {city}",
                f"houses for sale in {city}",
                f"property dealer in {city}"
            ]

            service_keywords = [
                f"commercial property in {city}",
                f"residential property in {city}",
                f"property investment in {city}",
                f"buy house in {city}",
                f"sell property in {city}"
            ]

            long_tail_keywords = [
                f"best areas to buy property in {city}",
                f"affordable houses for sale in {city}",
                f"best property investment in {city}",
                f"how to buy property in {city}",
                f"property prices in {city}"
            ]

            content_topics = [
                f"Complete guide to buying property in {city}",
                f"Best areas for property investment in {city}",
                f"How to choose a real estate agent",
                f"Common mistakes property buyers make",
                f"How to prepare a property for sale",
                f"Residential vs commercial property",
                f"Property investment guide",
                f"Questions to ask before buying property",
                f"Property viewing checklist",
                f"First-time buyer guide"
            ]

            local_actions = [
                f"Create location pages for major areas of {city}",
                "Create individual property landing pages",
                "Optimize Google Business Profile",
                "Build local real estate citations",
                "Publish local market content",
                "Collect genuine client reviews",
                "Build partnerships with local businesses",
                "Create neighborhood guides"
            ]

        elif "gym" in industry or "fitness" in industry:

            primary_keywords = [
                f"gym in {city}",
                f"fitness center in {city}",
                f"best gym in {city}",
                f"personal trainer in {city}",
                f"gym near me"
            ]

            service_keywords = [
                f"personal training in {city}",
                f"weight loss gym in {city}",
                f"strength training in {city}",
                f"fitness classes in {city}",
                f"women's gym in {city}"
            ]

            long_tail_keywords = [
                f"best gym for beginners in {city}",
                f"affordable gym membership in {city}",
                f"personal trainer for weight loss in {city}",
                f"best fitness center in {city}",
                f"how to choose a gym in {city}"
            ]

            content_topics = [
                "Beginner's guide to joining a gym",
                "How to choose the right gym",
                "Common workout mistakes",
                "Strength training for beginners",
                "How often should you train?",
                "Gym nutrition basics",
                "Personal training benefits",
                "How to stay consistent with workouts",
                "Weight-loss training mistakes",
                "Gym equipment guide"
            ]

            local_actions = [
                f"Create a location landing page for {city}",
                "Optimize Google Business Profile",
                "Collect genuine member reviews",
                "Publish local fitness content",
                "Build local citations",
                "Create service-specific pages",
                "Partner with local businesses",
                "Add strong booking CTAs"
            ]

        else:

            primary_keywords = [
                f"{business_type} in {city}",
                f"best {business_type} in {city}",
                f"{business_type} near me",
                f"{business_type} services in {city}",
                f"{business_type} company in {city}"
            ]

            service_keywords = [
                f"professional {business_type} in {city}",
                f"affordable {business_type} in {city}",
                f"local {business_type} in {city}",
                f"trusted {business_type} in {city}",
                f"top {business_type} services in {city}"
            ]

            long_tail_keywords = [
                f"how to choose a {business_type} in {city}",
                f"best {business_type} for local customers",
                f"affordable {business_type} near me",
                f"professional {business_type} near me",
                f"recommended {business_type} in {city}"
            ]

            content_topics = [
                f"Complete guide to choosing a {business_type}",
                f"Common mistakes customers make",
                f"How to choose the right {business_type}",
                f"Questions to ask before buying",
                f"How much does {business_type} cost?",
                f"Benefits of professional services",
                f"Beginner's guide to {business_type}",
                f"How to compare {business_type} providers",
                f"Important things customers should know",
                f"Local guide to {business_type}"
            ]

            local_actions = [
                f"Create a dedicated {business_type} page targeting {city}",
                "Optimize Google Business Profile",
                "Collect genuine customer reviews",
                "Build local citations",
                "Create local service pages",
                "Publish location-specific content",
                "Improve NAP consistency",
                "Build relevant local partnerships"
            ]

        # --------------------------------------------------
        # Build keyword table
        # --------------------------------------------------

        keywords = (
            primary_keywords
            + service_keywords
            + long_tail_keywords
        )

        keyword_rows = []

        for index, keyword in enumerate(keywords, start=1):

            if index <= 5:
                intent = "Commercial / Local"
                funnel = "Bottom"
                priority = "High"

            elif index <= 10:
                intent = "Commercial"
                funnel = "Bottom"
                priority = "High"

            elif index <= 15:
                intent = "Informational / Commercial"
                funnel = "Middle"
                priority = "Medium"

            else:
                intent = "Informational / Long-tail"
                funnel = "Top / Middle"
                priority = "Medium"

            keyword_rows.append(
                f"| {index} | {keyword} | {intent} | "
                f"{funnel} | {priority} |"
            )

        keyword_table = "\n".join(keyword_rows)

        # --------------------------------------------------
        # Blog table
        # --------------------------------------------------

        blog_rows = []

        for index, topic in enumerate(
            content_topics[:15],
            start=1
        ):

            keyword = keywords[
                (index - 1) % len(keywords)
            ]

            blog_rows.append(
                f"| {index} | {topic} | "
                f"{keyword} | Learn / Compare | "
                f"Contact {business_name} |"
            )

        blog_table = "\n".join(blog_rows)

        # --------------------------------------------------
        # 30-day plan
        # --------------------------------------------------

        seo_tasks = [
            "Audit website structure and indexing",
            "Check robots.txt and XML sitemap",
            "Review homepage title and meta description",
            "Optimize homepage headings",
            "Improve service page structure",
            "Create local service landing page",
            "Optimize Google Business Profile",
            "Review NAP consistency",
            "Create internal linking map",
            "Optimize image filenames and alt text",
            "Create first SEO blog article",
            "Create second SEO blog article",
            "Create third SEO blog article",
            "Add stronger conversion CTAs",
            "Collect genuine customer reviews",
            "Build local citation opportunities",
            "Research competitor keyword gaps",
            "Research competitor content gaps",
            "Create FAQ content",
            "Create location-specific content",
            "Publish service-focused content",
            "Build relevant local partnerships",
            "Review indexed pages",
            "Review Search Console performance",
            "Improve underperforming pages",
            "Update important title tags",
            "Strengthen internal links",
            "Review local rankings",
            "Measure organic leads and calls",
            "Prepare next 90-day SEO roadmap"
        ]

        day_rows = []

        for day, task in enumerate(
            seo_tasks,
            start=1
        ):

            keyword = keywords[
                (day - 1) % len(keywords)
            ]

            if day <= 7:
                objective = "Technical foundation"
                outcome = "Cleaner SEO foundation"

            elif day <= 14:
                objective = "On-page optimization"
                outcome = "Better relevance and crawlability"

            elif day <= 21:
                objective = "Content and local visibility"
                outcome = "More search opportunities"

            else:
                objective = "Authority and optimization"
                outcome = "Improved rankings and lead potential"

            day_rows.append(
                f"| {day} | {task} | {keyword} | "
                f"{objective} | {outcome} |"
            )

        day_table = "\n".join(day_rows)

        # --------------------------------------------------
        # Final report
        # --------------------------------------------------

        response = f"""
# 📈 SEO Strategy — {business_name}

## 1. SEO Executive Summary

**Business:** {business_name}  
**Business Type:** {business_type}  
**Website:** {website}  
**Target City:** {city}  
**Target Audience:** {audience}  
**Primary Goal:** {seo_goal}

The primary opportunity is to build a search strategy around **high-intent local searches**, service-specific pages, strong trust signals and conversion-focused landing pages.

Because this is Demo Mode and no live crawl data is available, the report does **not claim that specific technical issues already exist**.

Recommendations below should be treated as actions to verify and implement.

---

## 2. Business & Search Intent Analysis

The SEO strategy should target four major search groups:

### Local Intent

People searching for the service together with **{city}** or "near me".

### Commercial Intent

People comparing providers before contacting a business.

### Service Intent

People searching for a specific service offered by **{business_name}**.

### Informational Intent

People researching problems, solutions and buying decisions before becoming customers.

The strongest lead opportunity normally comes from combining **local + commercial + service intent**.

---

## 3. Website SEO Audit

### Known Information

- Business: {business_name}
- Industry: {business_type}
- Target location: {city}
- Website provided: {website}

### Recommended Checks

- Review website navigation.
- Check whether every major service has a dedicated page.
- Check mobile usability.
- Check page speed.
- Review homepage messaging.
- Ensure important services are clearly visible.
- Add strong contact and booking CTAs.
- Add trust signals, reviews and credentials where applicable.
- Make contact information easy to find.
- Review page structure and headings.

**Important:** These are recommended checks, not claims that the website currently has these problems.

---

## 4. Technical SEO

Priority checklist:

- Confirm HTTPS.
- Verify XML sitemap.
- Verify robots.txt.
- Check Google indexing.
- Check canonical URLs.
- Identify broken links.
- Check redirect chains.
- Review Core Web Vitals.
- Optimize mobile experience.
- Compress large images.
- Add appropriate structured data.
- Remove unnecessary duplicate pages.
- Verify important pages are crawlable.

---

## 5. On-Page SEO

### Homepage

Target the main commercial service + **{city}**.

### Service Pages

Create one strong page for each important service.

### Location Pages

Where genuinely useful, create location-specific pages rather than duplicating nearly identical content.

### Title Tags

Use:

**Primary Service + Location + Brand**

### Meta Descriptions

Explain the service, location and next action.

### Headings

Use one clear H1 followed by logical H2/H3 sections.

### URLs

Keep URLs short, descriptive and readable.

### Internal Links

Link:

**Homepage → Service → Location → Blog → Conversion page**

---

## 6. Local SEO Strategy

### Local SEO Priorities

"""

        for action in local_actions:

            response += f"- {action}.\n"

        response += f"""

### Local Trust

Focus on genuine customer reviews, consistent business information and useful local content.

Do not create fake reviews or misleading location pages.

---

## 7. Google Business Profile Strategy

Recommended actions:

1. Select the most accurate primary category.
2. Add relevant secondary categories where appropriate.
3. Complete every important profile field.
4. Add accurate services.
5. Upload high-quality real business photos.
6. Publish useful Google Business Profile posts.
7. Answer genuine customer questions.
8. Build a consistent review acquisition process.
9. Respond professionally to reviews.
10. Keep business information consistent with the website.

---

## 8. Keyword Strategy

| # | Keyword | Search Intent | Funnel Stage | Priority |
|---|---|---|---|---|
{keyword_table}

---

## 9. Content Strategy

### Content Pillar 1 — Education

Answer common customer questions.

### Content Pillar 2 — Services

Explain services, benefits and suitability.

### Content Pillar 3 — Local

Create useful content related to **{city}**.

### Content Pillar 4 — Trust

Demonstrate expertise, credentials, reviews and real experience.

### Content Pillar 5 — Conversion

Create pages and content that help users take the next step.

---

## 10. Blog Ideas

| # | Topic | Primary Keyword | Intent | CTA |
|---|---|---|---|---|
{blog_table}

---

## 11. Competitor SEO Strategy

No competitor data was supplied, so no competitor rankings or backlink profiles are being claimed.

When competitor data becomes available, investigate:

- Ranking keywords
- Service pages
- Location pages
- Content depth
- Internal linking
- Backlink sources
- Reviews
- Google Business Profile strength
- Content gaps
- Keyword gaps

The objective should be to find areas where **{business_name}** can create more useful and more conversion-focused content.

---

## 12. Backlink Strategy

Prioritize relevant and legitimate links from:

- Local business directories
- Industry directories
- Local organizations
- Professional associations
- Community websites
- Local partnerships
- Guest contributions
- Digital PR
- Useful original resources

Avoid:

- Purchased spam links
- Automated link networks
- Irrelevant bulk directories
- Manipulative link schemes

---

## 13. Internal Linking Strategy

Use a clear hierarchy:

**Homepage → Core Services → Supporting Content**

Then:

**Blog → Relevant Service Page**

And:

**Location Page → Relevant Service Page**

Use descriptive anchor text naturally rather than repeatedly using exact-match keywords.

---

## 14. Conversion SEO

SEO should ultimately produce business results.

### Visitor

↓

### Engaged Visitor

↓

### Enquiry

↓

### Qualified Lead

↓

### Customer

Recommended conversion elements:

- Click-to-call buttons
- WhatsApp CTA where appropriate
- Simple enquiry forms
- Appointment/booking CTA
- Clear service information
- Reviews and trust signals
- Strong above-the-fold messaging

---

## 15. 30-Day SEO Content & Execution Calendar

| Day | Task | Keyword | SEO Objective | Expected Outcome |
|---|---|---|---|---|
{day_table}

---

## 16. 30-Day SEO Execution Plan

### Week 1 — Foundation

- Technical checks
- Indexing verification
- Sitemap and robots.txt
- Website structure review
- Google Business Profile review

### Week 2 — On-Page SEO

- Homepage optimization
- Service page optimization
- Title/meta improvements
- Internal linking
- Image optimization

### Week 3 — Content & Local SEO

- Publish targeted content
- Build local signals
- Improve reviews
- Create useful local content
- Strengthen service/location relevance

### Week 4 — Authority & Optimization

- Competitor research
- Backlink opportunities
- Performance review
- Improve underperforming pages
- Prepare next 90-day roadmap

---

## 17. Priority Fixes

| Priority | Action | Why It Matters |
|---|---|---|
| 1 | Build/optimize core service pages | Captures high-intent searches |
| 2 | Strengthen local SEO | Improves local discovery |
| 3 | Optimize Google Business Profile | Supports local visibility |
| 4 | Improve conversion CTAs | Turns traffic into enquiries |
| 5 | Fix technical SEO issues found in audit | Improves crawlability |
| 6 | Build internal linking | Helps search engines understand site structure |
| 7 | Publish targeted content | Expands keyword coverage |
| 8 | Build relevant local authority | Supports trust and rankings |
| 9 | Improve review acquisition | Strengthens local trust |
| 10 | Track organic leads | Connects SEO to business outcomes |

---

## 18. SEO KPI Dashboard

### Visibility

- Keyword rankings
- Search impressions
- Search visibility
- Google Business Profile visibility

### Traffic

- Organic sessions
- Landing page traffic
- Organic engagement

### Leads

- Phone calls
- Forms
- WhatsApp enquiries
- Bookings

### Conversion

- Organic lead conversion rate
- Qualified leads
- Customers generated
- Revenue attributed to organic search

---

## 19. Final Consultant Recommendation

### Biggest Opportunity

Own the highest-intent **{business_type} + {city}** searches with strong service pages, local SEO and conversion-focused content.

### Biggest Risk

Implementing generic SEO tactics without measuring whether they generate qualified leads.

### First 3 Actions

1. Audit and optimize the highest-value service pages.
2. Strengthen Google Business Profile and local signals.
3. Build a keyword-driven content and internal-linking system.

### 30-Day Priority

Build the foundation first, then publish targeted content and strengthen local authority.

### 90-Day Direction

Move from basic optimization into continuous keyword expansion, content production, competitor gap analysis, authority building and conversion optimization.

---

## 🎯 Growth Radar AI Recommendation

For **{business_name}**, SEO should not be treated simply as a ranking exercise.

The ultimate objective is:

**Search Visibility → Qualified Traffic → Enquiries → Leads → Customers**

Every SEO action should eventually be evaluated against that business outcome.

---

### Demo Mode Notice

This report was generated by the **Growth Radar AI Demo Intelligence Engine**.

It uses the supplied business information and deterministic SEO intelligence because external AI credits are currently unavailable.

No unverified website rankings, traffic numbers, backlink counts or technical problems were presented as facts.
"""

        return {
            "success": True,
            "response": response,
            "error": "",
            "demo": True,
        }
    
    # ======================================================
    # SOCIAL MEDIA MANAGER
    # ======================================================

    if (
        "social media marketing strategy" in prompt
        or "social media strategy" in prompt
        or "30-day content calendar" in prompt
        or "social media manager" in system_prompt.lower()
    ):

        # --------------------------------------------------
        # Extract basic business information
        # --------------------------------------------------

        business_name = "the business"
        industry = "the business's industry"
        location = "the specified location"

        for line in user_prompt.splitlines():

            line_clean = line.strip()

            if line_clean.startswith("Business Name:"):
                value = line_clean.split(
                    "Business Name:",
                    1
                )[1].strip()

                if value:
                    business_name = value

            elif line_clean.startswith("Industry:"):
                value = line_clean.split(
                    "Industry:",
                    1
                )[1].strip()

                if value and value != "Not provided":
                    industry = value

            elif line_clean.startswith("Location:"):
                value = line_clean.split(
                    "Location:",
                    1
                )[1].strip()

                if value and value != "Not provided":
                    location = value

        # --------------------------------------------------
        # Industry-specific content
        # --------------------------------------------------

        industry_lower = industry.lower()

        if "dent" in industry_lower:

            content_examples = [
                "Patient education Reels",
                "Before/after treatment education",
                "Common dental mistakes",
                "Doctor Q&A videos",
                "Treatment explanation carousels"
            ]

            hooks = [
                "3 signs you should not ignore when it comes to your teeth",
                "Most people make this dental mistake every day",
                "What actually happens during a root canal?",
                "Before getting teeth whitening, know these 3 things",
                "Your dentist can spot these problems before they become serious"
            ]

            ctas = [
                "Book a consultation today.",
                "Send us a DM to learn more.",
                "Save this post for later.",
                "Contact the clinic for an appointment.",
                "Share this with someone who needs it."
            ]

        elif "real estate" in industry_lower:

            content_examples = [
                "Property walkthroughs",
                "Local market updates",
                "Buyer education",
                "Seller tips",
                "Neighborhood guides"
            ]

            hooks = [
                "3 things buyers should check before purchasing a property",
                "Would you buy this property?",
                "What $500,000 can get you in this area",
                "The biggest mistake first-time buyers make",
                "Is now a good time to buy?"
            ]

            ctas = [
                "DM us for available properties.",
                "Book a property consultation.",
                "Save this for your next property search.",
                "Send us your budget.",
                "Contact us for current listings."
            ]

        elif "gym" in industry_lower or "fitness" in industry_lower:

            content_examples = [
                "Workout education",
                "Transformation stories",
                "Exercise tutorials",
                "Nutrition tips",
                "Trainer Q&A"
            ]

            hooks = [
                "Stop doing this exercise like this",
                "3 mistakes slowing down your progress",
                "What beginners should actually do in the gym",
                "Do this instead of wasting hours on cardio",
                "The simple routine we recommend for beginners"
            ]

            ctas = [
                "DM us for a membership consultation.",
                "Book a free trial.",
                "Save this workout.",
                "Send us a message to get started.",
                "Visit us today."
            ]

        elif "restaurant" in industry_lower or "food" in industry_lower:

            content_examples = [
                "Food photography",
                "Behind-the-scenes content",
                "Customer reactions",
                "Chef content",
                "Special offers"
            ]

            hooks = [
                "You need to try this before leaving town",
                "POV: You finally found your new favorite meal",
                "Here's what our customers order most",
                "Behind the scenes in our kitchen",
                "Would you try this?"
            ]

            ctas = [
                "Visit us today.",
                "Tag someone you would bring here.",
                "DM us for reservations.",
                "Save this for your next visit.",
                "Order now."
            ]

        else:

            content_examples = [
                "Educational short-form videos",
                "Customer success stories",
                "Behind-the-scenes content",
                "Industry tips",
                "FAQ and problem-solving posts"
            ]

            hooks = [
                "The biggest mistake businesses make with this",
                "3 things you should know before choosing a service",
                "Here's what most people get wrong",
                "A simple way to improve your results",
                "What we would do if we were starting from zero"
            ]

            ctas = [
                "DM us to learn more.",
                "Book a consultation.",
                "Save this post for later.",
                "Contact us today.",
                "Share this with someone who needs it."
            ]

        # --------------------------------------------------
        # Build 30-day calendar
        # --------------------------------------------------

        calendar = []

        for day in range(1, 31):

            content_type = [
                "Reel",
                "Carousel",
                "Educational Post",
                "Story",
                "Customer/Trust Post"
            ][(day - 1) % 5]

            hook = hooks[(day - 1) % len(hooks)]
            cta = ctas[(day - 1) % len(ctas)]
            topic = content_examples[(day - 1) % len(content_examples)]

            calendar.append(
                f"| Day {day} | Instagram + Facebook | "
                f"{content_type} | {topic} | {hook} | {cta} |"
            )

        calendar_text = "\n".join(calendar)

        response = f"""
# 📋 Social Media Strategy — {business_name}

## 1. Executive Summary

**Business:** {business_name}  
**Industry:** {industry}  
**Location:** {location}

The primary social media opportunity for **{business_name}** is to turn social media from a simple visibility channel into a consistent **trust, engagement and lead-generation system**.

The strategy should focus on useful content, proof of expertise, customer trust, short-form video and clear conversion CTAs.

---

# 2. Target Audience

### Primary Audience

People actively looking for reliable solutions related to **{industry}**.

### Secondary Audience

- People researching before making a purchase
- Existing customers
- Local community members
- Referrals and recommendations
- People comparing competitors

### Main Customer Needs

- Trust
- Clear information
- Proof of quality
- Convenience
- Professional service
- Confidence before purchasing

### Content That Should Attract Them

{", ".join(content_examples)}.

---

# 3. Brand Positioning

{business_name} should position itself as a **trusted, knowledgeable and customer-focused {industry} business**.

### Core Message

> Make the customer's decision easier by showing expertise, proof and real value before asking for the sale.

### Recommended Tone

- Professional
- Helpful
- Confident
- Human
- Educational
- Not overly promotional

---

# 4. Social Media Strategy

## Awareness

Use Reels, educational videos and shareable content to reach new people.

## Engagement

Use questions, polls, quizzes, controversial-but-useful topics and comment-driven content.

## Lead Generation

Every week should contain content with a direct conversion opportunity.

Examples:

- DM us
- Book a consultation
- Request information
- Get a quote
- Schedule an appointment

## Conversion

Move people through:

**Follower → Engaged User → DM → Lead → Customer**

## Retention

Use customer stories, FAQs, educational content and community posts to remain useful after the first purchase.

---

# 5. Platform Strategy

## Instagram

### Content Types

{", ".join(content_examples)}

### Frequency

- 4–5 feed posts per week
- 3–5 Reels per week
- Stories almost daily

### Best Formats

- Reels
- Carousels
- Stories
- Testimonials
- Q&A

### Lead Strategy

Use profile CTAs and DM keywords.

Example:

> "DM **INFO** and we'll send you the details."

---

## Facebook

Focus on:

- Local audience
- Educational posts
- Testimonials
- Offers
- Community engagement
- Reposted short-form videos

Recommended frequency:

**4–5 posts per week.**

---

# 6. Content Pillars

## 1. Education

Teach customers something useful.

## 2. Trust & Authority

Show expertise, credentials, processes and knowledge.

## 3. Customer Proof

Show testimonials, reviews, transformations and experiences.

## 4. Behind The Scenes

Show the people and process behind the business.

## 5. Conversion

Promote services, offers, consultations and clear next steps.

---

# 7. 30-Day Content Calendar

| Day | Platform | Format | Topic | Hook | CTA |
|---|---|---|---|---|---|
{calendar_text}

---

# 8. 10 Short-Form Video Ideas

## 1. "The Biggest Mistake"

**Hook:** {hooks[0]}

Show the common mistake, explain why it matters and demonstrate the correct approach.

**CTA:** {ctas[0]}

## 2. "3 Things You Should Know"

**Hook:** {hooks[1]}

Give three practical points customers should know.

**CTA:** {ctas[1]}

## 3. FAQ Video

Answer one question customers repeatedly ask.

**CTA:** {ctas[2]}

## 4. Behind The Scenes

Show what customers normally don't see.

**CTA:** {ctas[3]}

## 5. Customer Story

Explain a customer problem and how the business helped.

**CTA:** {ctas[4]}

## 6. Myth vs Reality

Take a common misconception in the industry and explain the truth.

## 7. "What Nobody Tells You"

Share a useful industry insight.

## 8. Quick Expert Tip

Give one actionable recommendation in under 30 seconds.

## 9. Comparison

Compare two common choices customers face.

## 10. Direct Offer

Explain one service, its benefit and who it is for.

---

# 9. Caption Strategy

Captions should follow:

**Hook → Problem → Value → Proof → CTA**

Avoid writing long captions without a clear purpose.

### Example Caption 1

**{hooks[0]}**

Here's what you should know before making your decision.

Our goal is to make the process simpler and give customers the information they actually need.

**{ctas[0]}**

### Example Caption 2

**{hooks[1]}**

Most people don't realize how important this is.

Save this post and share it with someone who needs it.

### Example Caption 3

Good information creates better decisions.

Follow **{business_name}** for practical {industry} advice.

### Example Caption 4

Have a question about our services?

Send us a DM and we'll help you understand your options.

### Example Caption 5

Looking for a reliable {industry} business?

Start by asking the right questions.

**{ctas[1]}**

---

# 10. Lead Generation Strategy

### Lead Magnets

Depending on the business:

- Free consultation
- Free assessment
- Checklist
- Quote
- Guide
- Educational resource

### DM Strategy

Use simple CTAs:

> "DM INFO"

> "DM QUOTE"

> "DM CONSULTATION"

### Offer Strategy

Make the first step low-friction.

Instead of:

> "Buy now."

Use:

> "Book a free consultation."

or

> "Send us a message to discuss your options."

### Follow-Up

Every social lead should receive:

1. Fast response
2. Qualification question
3. Relevant information
4. Offer/next step
5. Follow-up

---

# 11. Engagement Strategy

Increase:

- Comments through questions
- Saves through educational content
- Shares through useful tips
- DMs through specific CTAs
- Community interaction through Stories

Respond to comments quickly and turn common questions into future content.

---

# 12. Growth Strategy

### Organic Growth

Prioritize short-form video and highly useful educational content.

### Collaboration

Partner with:

- Complementary local businesses
- Industry experts
- Micro-influencers
- Existing customers

### User-Generated Content

Encourage customers to share experiences and tag the business.

---

# 13. Conversion Strategy

### Stage 1 — Follower

Attract them with useful content.

↓

### Stage 2 — Engaged Follower

Build trust through education and proof.

↓

### Stage 3 — Lead

Use DMs, consultations, quotes and offers.

↓

### Stage 4 — Customer

Make the buying process simple.

---

# 14. KPI Dashboard

### Awareness

- Reach
- Impressions
- Video views
- Profile visits

### Engagement

- Comments
- Shares
- Saves
- Engagement rate

### Leads

- DMs
- Consultation requests
- Quote requests
- Contact form submissions

### Conversion

- Qualified leads
- Customers generated
- Conversion rate
- Revenue generated

---

# 15. 30-Day Execution Plan

## Week 1 — Foundation

- Optimize profiles
- Define content pillars
- Create visual templates
- Establish brand voice
- Prepare first batch of content

## Week 2 — Content & Engagement

- Publish educational content
- Increase Reels
- Respond to comments
- Use Stories daily
- Test different hooks

## Week 3 — Lead Generation

- Introduce lead magnets
- Add DM CTAs
- Publish service-focused content
- Promote consultations/offers
- Track incoming leads

## Week 4 — Optimization & Conversion

- Identify best-performing content
- Repeat winning formats
- Improve CTAs
- Follow up with leads
- Build next month's content plan

---

# 16. Priority Actions

1. Optimize Instagram and Facebook profiles.
2. Establish the five content pillars.
3. Publish educational short-form videos.
4. Create consistent CTA patterns.
5. Start collecting customer testimonials.
6. Introduce DM-based lead generation.
7. Build a 30-day content workflow.
8. Track leads rather than followers alone.
9. Identify the top-performing content formats.
10. Repeat successful content while improving the hooks.

---

### Demo Mode Notice

This strategy was generated by the **Growth Radar AI Demo Intelligence Engine** because the external AI provider is currently unavailable.

The production AI engine is ready to replace this deterministic strategy once API credits are available.
"""

        return {
            "success": True,
            "response": response,
            "error": "",
            "demo": True,
        }

    # ======================================================
    # SALES / GENERAL DEMO ENGINE
    # ======================================================

    if (
        "opening line" in prompt
        or "opening" in prompt
    ):

        response = (
            "Hi, this is Wahaj from Growth Radar AI. "
            "I'm reaching out because we help businesses "
            "improve their online growth and lead generation. "
            "Do you have a quick minute?"
        )

    elif (
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

    elif "not interested" in prompt:

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
            "What's your biggest challenge with getting new "
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
            "I'd like to understand the business a little "
            "better before recommending anything. What is "
            "the main challenge you're currently facing with "
            "marketing or customer acquisition?"
        )

    return {
        "success": True,
        "response": response,
        "error": "",
        "demo": True,
    }

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