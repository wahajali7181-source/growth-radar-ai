import streamlit as st

from core.navigation import (
    open_ai_consultant,
    open_proposal,
    open_website_scan,
    open_crm,
)


def show_business_card(business):

    score = int(business.get("lead_score", 0))

    if score >= 80:
        badge = "🟢 Excellent"

    elif score >= 60:
        badge = "🟡 High"

    elif score >= 40:
        badge = "🟠 Medium"

    else:
        badge = "🔴 Low"

    with st.container(border=True):

        c1, c2 = st.columns([4, 1])

        with c1:

            st.subheader(

                business.get("name", "Unknown Business")

            )

            st.caption(

                business.get("business_type", "")

            )

        with c2:

            st.metric(

                "Lead Score",

                score

            )

        st.write(f"**Opportunity:** {badge}")

        st.write(f"⭐ Rating: {business.get('rating', 0)}")

        st.write(f"📝 Reviews: {business.get('reviews', 0)}")

        if business.get("website"):

            st.write(f"🌐 {business['website']}")

        if business.get("email"):

            st.write(f"📧 {business['email']}")

        if business.get("phone"):

            st.write(f"📞 {business['phone']}")

        if business.get("technology"):

            st.write(f"💻 {business['technology']}")

        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        if c1.button(
            "🌐 Website",
            key=f"website_{business['name']}",
            use_container_width=True,
        ):
            open_website_scan(
                business.to_dict() if hasattr(business, "to_dict") else dict(business)
            )
            st.rerun()

        if c2.button(
            "🤖 AI",
            key=f"ai_{business['name']}",
            use_container_width=True,
        ):
            open_ai_consultant(
                business.to_dict() if hasattr(business, "to_dict") else dict(business)
            )
            st.rerun()

        if c3.button(
            "📄 Proposal",
            key=f"proposal_{business['name']}",
            use_container_width=True,
        ):
            open_proposal(
                business.to_dict() if hasattr(business, "to_dict") else dict(business)
            )
            st.rerun()

        if c4.button(
            "📋 CRM",
            key=f"crm_{business['name']}",
            use_container_width=True,
        ):
            open_crm(
                business.to_dict() if hasattr(business, "to_dict") else dict(business)
            )
            st.rerun()