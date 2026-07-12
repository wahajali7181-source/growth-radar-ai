import streamlit as st


def show_dashboard():

    st.title("🚀 Growth Radar AI")

    st.caption("AI Powered Business Intelligence Platform")

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Businesses", "0")

    with c2:
        st.metric("Websites", "0")

    with c3:
        st.metric("Health", "0")

    with c4:
        st.metric("Reports", "0")

    st.divider()