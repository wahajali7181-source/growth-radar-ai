import streamlit as st

from lead_engine.database import load_businesses


def show():

    st.title("📊 Dashboard")

    df = load_businesses()

    if df.empty:

        st.info("No businesses available.")
        st.write(df.columns.tolist())
        st.dataframe(df.head())
        return
     
    total = len(df)

    excellent = len(df[df["opportunity"] == "🟢 Excellent"])
    good = len(df[df["opportunity"] == "🟡 Good"])
    average = len(df[df["opportunity"] == "🟠 Average"])
    high_opportunity = len(df[df["opportunity"] == "🔴 High Opportunity"])

    avg_score = round(df["lead_score"].mean(), 1)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Businesses", total)
    c2.metric("Excellent", excellent)
    c3.metric("Good", good)
    c4.metric("Avg Score", avg_score)

    st.divider()

    st.subheader("Latest Businesses")

    st.dataframe(
        df.sort_values(
            "id",
            ascending=False
        ),
        use_container_width=True
    )