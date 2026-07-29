from ui.sidebar import show_sidebar

from pages.dashboard import show as dashboard_page
from pages.lead_finder import show as lead_finder_page
from pages.crm import show as crm_page
from pages.website_intelligence import show as website_page
from pages.social_intelligence import show as social_page
from pages.trend_intelligence import show as trend_page
from pages.ai_employees import show as ai_page
from pages.reports import show as reports_page
from pages.settings import show as settings_page


def run():

    page = show_sidebar()

    if page == "🏠 Dashboard":
        dashboard_page()

    elif page == "🔍 Business Finder":
        lead_finder_page()

    elif page == "📋 CRM":
        crm_page()

    elif page == "🌐 Website Intelligence":
        website_page()

    elif page == "📱 Social Intelligence":
        social_page()

    elif page == "📈 Trend Intelligence":
        trend_page()

    elif page == "🤖 AI Employees":
        ai_page()

    elif page == "📄 Reports":
        reports_page()

    elif page == "⚙ Settings":
        settings_page()