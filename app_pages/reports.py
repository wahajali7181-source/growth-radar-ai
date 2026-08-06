import streamlit as st
from auth.session import require_auth
def show():
    

    require_auth()

    

    st.title("📄 Reports")

    st.info("Reports module ready.")