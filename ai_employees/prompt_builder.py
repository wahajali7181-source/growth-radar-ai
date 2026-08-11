def build_sales_prompt(
    business_name,
    business_type,
    website,
    country,
    target_audience,
    goal,
    budget,
):

    return f"""
You are one of the world's best B2B Sales Consultants.

Business Information

Business Name:
{business_name}

Business Type:
{business_type}

Website:
{website}

Country:
{country}

Target Audience:
{target_audience}

Business Goal:
{goal}

Monthly Marketing Budget:
{budget}

Create a professional report using markdown.

Include these sections:

# Business Overview

# Current Business Situation

# Biggest Challenges

# Strengths

# Weaknesses

# Growth Opportunities

# Target Customer Profile

# Sales Strategy

# Lead Generation Strategy

# Outreach Strategy

# Cold Email

# LinkedIn Outreach

# WhatsApp Pitch

# Discovery Call Questions

# Objection Handling

# Closing Strategy

# Recommended Digital Marketing Services

# 30-Day Action Plan

Be practical.

Avoid generic advice.

Write like a senior business consultant.
"""