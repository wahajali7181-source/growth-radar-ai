import streamlit as st

from ai_employees.ai_client import generate_response


def show():

    st.subheader("📈 AI SEO Expert")

    website = st.text_input(
        "Website"
    )

    business_type = st.text_input(
        "Business Type"
    )

    city = st.text_input(
        "Target City"
    )

    if st.button("Generate SEO Strategy"):

        if website.strip() == "":

            st.warning("Please enter website.")

            return

        prompt = f"""
Website:
{website}

Business Type:
{business_type}

Target City:
{city}

Generate a complete SEO strategy.

Include:

1. Website SEO Audit

2. Technical SEO

3. On Page SEO

4. Off Page SEO

5. Local SEO

6. Google Business Profile Tips

7. Top 20 Keywords

8. Blog Ideas

9. Competitor Strategy

10. Backlink Strategy

11. Internal Linking

12. Content Calendar

13. 30 Day SEO Plan

14. Priority Fixes

Write professionally.
"""

        with st.spinner("SEO Expert is working..."):

            result = generate_response(

                prompt=prompt,

                system_prompt="""
You are an international SEO Expert.

Generate premium SEO reports.

Always write detailed responses.

Use markdown headings.

Think like an SEO consultant charging $5,000/month.
"""

            )

        st.markdown(result)