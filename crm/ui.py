import streamlit as st

from crm.engine import save_crm


PIPELINE = [

    "New Lead",

    "Qualified",

    "Contacted",

    "Meeting Scheduled",

    "Proposal Sent",

    "Negotiation",

    "Won",

    "Lost",

]


PRIORITY = [

    "Low",

    "Medium",

    "High",

    "Urgent",

]


def crm_card(business):

    st.subheader("📋 CRM Management")

    c1, c2 = st.columns(2)

    with c1:

        starred = st.toggle(

            "⭐ Star Lead"

        )

    with c2:

        proposal = st.toggle(

            "📄 Proposal Sent"

        )

    priority = st.selectbox(

        "Priority",

        PRIORITY,

        index=1

    )

    pipeline = st.selectbox(

        "Pipeline Stage",

        PIPELINE

    )

    estimated_value = st.number_input(

        "Estimated Deal Value ($)",

        min_value=0,

        max_value=10000000,

        value=1000,

        step=100,

    )

    probability = st.slider(

        "Closing Probability",

        0,

        100,

        50,

    )

    followup = st.date_input(

        "Next Follow-up"

    )

    notes = st.text_area(

        "Internal Notes",

        height=150,

        placeholder="Write everything about this lead..."

    )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        if st.button(

            "💾 Save CRM",

            use_container_width=True

        ):

            save_crm(

                business["id"],

                int(starred),

                notes,

                str(followup),

                int(proposal),

                pipeline,

                estimated_value

            )

            st.success(

                "CRM Updated Successfully."

            )

    with c2:

        st.button(

            "📄 Generate Proposal",

            use_container_width=True,

            disabled=False

        )

    st.divider()

    st.caption(

        f"""
Lead : {business.get('name','')}

Website : {business.get('website','')}

Email : {business.get('email','Not Available')}

Phone : {business.get('phone','Not Available')}

Closing Probability : {probability}%

Priority : {priority}
"""
    )