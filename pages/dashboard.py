import streamlit as st

from lead_engine.database import load_businesses


def show():

    st.title("📊 Dashboard")

    df = load_businesses()

    if df.empty:

        st.info("No businesses available.")

        return

    total = len(df)

    high = len(df[df["opportunity"] == "High"])
    medium = len(df[df["opportunity"] == "Medium"])
    low = len(df[df["opportunity"] == "Low"])

    avg_score = round(df["lead_score"].mean(), 1)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Businesses", total)
    c2.metric("High", high)
    c3.metric("Medium", medium)
    c4.metric("Average Score", avg_score)

    st.divider()

    st.subheader("Latest Businesses")

    st.dataframe(
        df.sort_values(
            "id",
            ascending=False
        ),
        use_container_width=True
    )