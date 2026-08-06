import streamlit as st

from business.intelligence import load_business_intelligence


def show():

    businesses = load_business_intelligence()

    st.subheader("🏢 Select Business")

    if not businesses:

        st.warning(
            "No businesses found.\n\nSearch businesses first from Lead Finder."
        )
        return None

    search = st.text_input(

        "🔍 Search Business",

        placeholder="Business name..."

    )

    filtered = []

    if search:

        for business in businesses:

            if search.lower() in business.name.lower():

                filtered.append(business)

    else:

        filtered = businesses

    names = [

        business.name

        for business in filtered

    ]

    selected = st.selectbox(

        "Business",

        names,

        index=None,

        placeholder="Choose Business"

    )

    if not selected:

        return None

    business = next(

        x

        for x in filtered

        if x.name == selected

    )

    st.divider()

    c1, c2 = st.columns(2)

    c1.metric(

        "Lead Score",

        business.lead_score

    )

    c2.metric(

        "Priority",

        business.priority

    )

    c3, c4 = st.columns(2)

    c3.metric(

        "CRM",

        business.status

    )

    c4.metric(

        "Stage",

        business.deal_stage

    )

    st.text_input(

        "Website",

        business.website,

        disabled=True

    )

    st.text_input(

        "City",

        business.city,

        disabled=True

    )

    st.text_area(

        "Notes",

        business.notes,

        height=120,

        disabled=True

    )

    st.session_state["selected_business"] = business

    return business