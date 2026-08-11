import streamlit as st


def show_metrics(df):

    if df.empty:

        return

    total = len(df)

    avg_score = round(

        df["lead_score"].mean(),

        1

    )

    avg_rating = round(

        df["rating"].mean(),

        1

    )

    high = len(

        df[

            df["lead_score"] >= 80

        ]

    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Businesses",

        total

    )

    c2.metric(

        "High Quality",

        high

    )

    c3.metric(

        "Avg Score",

        avg_score

    )

    c4.metric(

        "Avg Rating",

        avg_rating

    )