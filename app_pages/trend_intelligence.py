import streamlit as st
from auth.session import require_auth
def show():
    require_auth()

    
    st.title("📈 Trend Intelligence")

    st.info("Trend Intelligence module ready.")