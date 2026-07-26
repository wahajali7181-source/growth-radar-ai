from ai_employees.ai_client import generate_response


def generate_react_website(

    business_name,
    business_type,
    website_plan

):

    prompt = f"""
Business Name:
{business_name}

Business Type:
{business_type}

Website Plan:

{website_plan}

Generate a COMPLETE production-ready website.

Requirements:

- React 19

- TailwindCSS

- Responsive

- Hero Section

- About

- Services

- Testimonials

- FAQ

- Contact

- Footer

Return ONLY React JSX code.

No explanations.

No markdown.

No comments.
"""

    return generate_response(

        prompt=prompt,

        system_prompt="""
You are a Senior React Developer.

Generate premium production-ready React websites.

Follow best UI/UX practices.

Return clean JSX only.
"""

    )