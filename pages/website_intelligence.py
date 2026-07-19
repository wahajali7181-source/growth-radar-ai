import streamlit as st
from website_scanner.report import generate_report
from website_scanner.health import calculate_health_score

from ui.website_cards import (
    show_overview_card,
    show_seo_card,
    show_security_card,
)

from ai_engine.recommendation_engine import generate_ai_actions

def show():

    st.title("🌐 Website Intelligence")

    st.info("Website Intelligence migration in progress.")

    st.write("Website Scanner, SEO, Security and AI Analysis will appear here.")