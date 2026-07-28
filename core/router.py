import streamlit as st

from pages.dashboard import show as dashboard_page
from pages.lead_finder import show as lead_finder_page
from pages.crm import show as crm_page
from pages.website_intelligence import show as website_page
from pages.social_intelligence import show as social_page
from pages.trend_intelligence import show as trend_page
from pages.ai_employees import show as ai_employees_page
from pages.reports import show as reports_page


def route(page):

    if page == "🏠 Dashboard":
        dashboard_page()
        return

    if page == "🔍 Business Finder":
        lead_finder_page()
        return

    if page == "📋 CRM":
        crm_page()
        return

    if page == "🌐 Website Intelligence":
        website_page()
        return

    if page == "📱 Social Intelligence":
        social_page()
        return

    if page == "📈 Trend Intelligence":
        trend_page()
        return

    if page == "🤖 AI Employees":
        ai_employees_page()
        return

    if page == "📄 Reports":
        reports_page()
        return

    if page == "⚙ Settings":
        from pages.settings import show
        show()
        return