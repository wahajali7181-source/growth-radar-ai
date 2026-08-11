import streamlit as st


def open_ai_consultant(business):

    st.session_state["selected_business"] = business
    st.session_state["page"] = "AI Sales Consultant"


def open_proposal(business):

    st.session_state["selected_business"] = business
    st.session_state["page"] = "Proposal Generator"


def open_website_scan(business):

    st.session_state["selected_business"] = business
    st.session_state["page"] = "Website Intelligence"


def open_crm(business):

    st.session_state["selected_business"] = business
    st.session_state["page"] = "CRM"