def build_json_prompt(
    business_name,
    business_type,
    website,
    country,
    target_audience,
    goal,
    budget,
):

    return f"""
Return ONLY valid JSON.

No markdown.

No explanation.

No text outside JSON.

Business

Name:
{business_name}

Industry:
{business_type}

Website:
{website}

Country:
{country}

Target Audience:
{target_audience}

Goal:
{goal}

Budget:
{budget}

Return JSON using EXACTLY this schema.

{{
"business_score":0,

"grade":"",

"priority":"",

"summary":"",

"strengths":[
"",
"",
""
],

"weaknesses":[
"",
"",
""
],

"opportunities":[
"",
"",
""
],

"threats":[
"",
"",
""
],

"ideal_customer_profile":{{
"industry":"",
"company_size":"",
"decision_maker":"",
"pain_points":[]
}},

"sales_strategy":[
"",
"",
""
],

"lead_generation":[
"",
"",
""
],

"marketing_strategy":[
"",
"",
""
],

"seo_strategy":[
"",
"",
""
],

"paid_ads_strategy":[
"",
"",
""
],

"social_media_strategy":[
"",
"",
""
],

"recommended_services":[
"",
"",
"",
""
],

"estimated_roi":"",

"pricing_strategy":"",

"competitor_strategy":"",

"kpis":[
"",
"",
"",
""
],

"cold_email":"",

"linkedin":"",

"whatsapp":"",

"follow_up_sequence":[
"",
"",
""
],

"sales_script":"",

"objection_handling":[
"",
"",
""
],

"action_plan":[
"",
"",
"",
"",
"",
"",
"",
""
]
}}

Everything must be practical.

Do NOT leave empty values.

Think like a senior McKinsey business consultant.
"""