import streamlit as st

from auth.session import is_logged_in
from auth.session import logout_session

from app_pages.login import show as login_page
from app_pages.register import show as register_page

from ui.sidebar import show_sidebar

from app_pages.dashboard import show as dashboard_page
from app_pages.lead_finder_old import show as lead_finder_page
from app_pages.crm import show as crm_page
from app_pages.website_intelligence import show as website_page
from app_pages.social_intelligence import show as social_page
from app_pages.trend_intelligence import show as trend_page
from app_pages.ai_employees import show as ai_page
from app_pages.reports_dashboard import show as reports_page
from app_pages.settings import show as settings_page
from app_pages.account import show as account_page
from app_pages.upgrade import show as upgrade_page
from app_pages.admin import show as admin_page

def run():

    # ==========================
    # LOGIN FIRST
    # ==========================

    if not is_logged_in():

        tab1, tab2 = st.tabs([

            "🔐 Login",

            "📝 Register"

        ])

        with tab1:
            login_page()

        with tab2:
            register_page()

        return

    # ==========================
    # SIDEBAR
    # ==========================

    page = show_sidebar()

    with st.sidebar:

        st.divider()

        if st.button(

            "🚪 Logout",

            use_container_width=True

        ):

            logout_session()

            st.rerun()

    # ==========================
    # ROUTER
    # ==========================
    
    

    if page == "🏠 Dashboard":

        dashboard_page()
        
    elif page == "👑 Admin":

        admin_page()    

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
        
    elif page == "👤 My Account":

        account_page()    
        
    elif page == "💳 Upgrade Plan":

        upgrade_page()    
        

    elif page == "⚙ Settings":

        settings_page()