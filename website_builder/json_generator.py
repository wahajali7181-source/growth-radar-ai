from ai_employees.ai_client import generate_response
import json


def generate_website_json(

    business_name,
    business_type,
    audience,
    style,
    colors,
    pages,
    cta

):

    prompt = f"""
Create ONLY valid JSON.

Business Name:
{business_name}

Business Type:
{business_type}

Audience:
{audience}

Style:
{style}

Colors:
{colors}

Pages:
{pages}

CTA:
{cta}

Return ONLY JSON.

Structure:

{{
"name":"",
"industry":"",
"hero":{{

"title":"",
"description":"",
"button":""

}},

"about":"",

"services":[

"", "", ""

],

"testimonials":[

{{

"name":"",
"review":""

}}

],

"faq":[

{{

"question":"",
"answer":""

}}

],

"colors":{{

"primary":"",
"secondary":""

}}

}}
"""

    response = generate_response(

        prompt=prompt,

        system_prompt="""
Return ONLY valid JSON.

No markdown.

No explanation.

No code block.

Only JSON.
"""

    )

    try:

        return json.loads(response)

    except Exception:

        return None