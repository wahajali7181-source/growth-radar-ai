def build_sales_prompt(
    business_name,
    business_type,
    website
):

    return f"""
You are an expert Sales Manager.

Business Name:
{business_name}

Business Type:
{business_type}

Website:
{website}

Generate:

1. Business Analysis

2. Biggest Problems

3. Growth Opportunities

4. Services To Sell

5. Cold Email

6. LinkedIn Message

7. WhatsApp Pitch

8. Discovery Call Questions

9. Objection Handling

10. Closing Strategy

Write professionally.
"""