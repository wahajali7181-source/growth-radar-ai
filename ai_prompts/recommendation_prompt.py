def build_recommendation_prompt(report):

    return f"""
You are a senior Business Growth Consultant.

Analyze this business.

Website Scanner:
{report["scanner"]}

SEO:
{report["seo"]}

Security:
{report["security"]}

Your response MUST include:

1. Business Summary

2. Biggest Problems

3. Revenue Opportunities

4. Priority Actions

5. Estimated Business Impact

Keep the answer professional.
"""