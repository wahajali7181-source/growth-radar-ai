from ai_employees.ai_client import generate_response


def generate_website_plan(

    business_name,
    business_type,
    target_audience,
    style,
    colors,
    pages,
    cta

):

    prompt = f"""
Business Name:
{business_name}

Industry:
{business_type}

Target Audience:
{target_audience}

Style:
{style}

Primary Colors:
{colors}

Pages:
{pages}

CTA:
{cta}

Create a professional website plan.

Generate:

1. Website Structure

2. Hero Section

3. Sections

4. Navigation

5. Color Suggestions

6. Fonts

7. SEO Structure

8. Conversion Tips

9. User Journey

10. Call To Actions

Use markdown.
"""

    return generate_response(

        prompt=prompt,

        system_prompt="""
You are one of the world's best Website UX Designers.

Design premium websites.

Think like Apple, Stripe, Framer, Linear and Webflow.

Focus on conversion and clean UI.
"""

    )