import streamlit as st


def show_filters(df):

    if df.empty:

        return df

    st.subheader("🔎 Filters")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        min_score = st.slider(

            "Lead Score",

            0,

            100,

            0

        )

    with c2:

        min_rating = st.slider(

            "Rating",

            0.0,

            5.0,

            0.0,

            0.1

        )

    with c3:

        website_only = st.checkbox(

            "Website Only"

        )

    with c4:

        email_only = st.checkbox(

            "Email Only"

        )

    filtered = df.copy()

    filtered = filtered[

        filtered["lead_score"] >= min_score

    ]

    filtered = filtered[

        filtered["rating"] >= min_rating

    ]

    if website_only:

        filtered = filtered[

            filtered["website"].fillna("") != ""

        ]

    if email_only:

        filtered = filtered[

            filtered["email"].fillna("") != ""

        ]

    return filtered