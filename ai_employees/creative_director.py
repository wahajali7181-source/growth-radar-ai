import streamlit as st

from ai_employees.ai_client import generate_response


def show():

    st.title("🎨 AI Creative Director")

    business_name = st.text_input(
        "Business Name"
    )

    business_type = st.text_input(
        "Business Type"
    )

    offer = st.text_input(
        "Offer",
        placeholder="20% OFF, Free Consultation"
    )

    target_city = st.text_input(
        "Target City"
    )

    if st.button("Generate Complete Campaign"):

        if business_name.strip() == "":
            st.warning("Enter Business Name")
            return

        prompt = f"""
Business Name:
{business_name}

Business Type:
{business_type}

Offer:
{offer}

Target City:
{target_city}

Create a COMPLETE Meta Ads Campaign.

Include:

1. Campaign Objective

2. Audience

3. Interests

4. Budget Recommendation

5. 5 Headlines

6. Primary Text

7. CTA

8. Facebook Ad Creative Idea

9. Instagram Creative Idea

10. Carousel Content

11. 30 Second Video Ad Script

12. Reel Script

13. Image Generation Prompt

14. Canva Design Prompt

15. Marketing Tips

Use professional formatting.
"""

        with st.spinner("AI Creative Director is working..."):

            result = generate_response(
                prompt=prompt,
                system_prompt="""
You are the world's best Creative Director and Meta Ads Expert.

Create high-converting advertising campaigns.

Always write professionally using markdown headings.

Be detailed.

Focus on generating leads and sales.
"""
            )

        st.markdown(result)