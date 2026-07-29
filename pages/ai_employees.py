import streamlit as st

from ai_employees.sales_manager import show as sales_manager
from ai_employees.creative_director import show as creative_director
from ai_employees.proposal_writer import show as proposal_writer
from ai_employees.seo_expert import show as seo_expert
from ai_employees.business_consultant import show as business_consultant
def show():

    st.title("🤖 AI Employees")

    st.markdown("### Your Complete AI Team")

    employee = st.selectbox(

        "Choose AI Employee",

        [

            "💼 AI Sales Manager",

            "🎨 AI Creative Director",

            "🧠 AI Business Consultant",

            "📄 AI Proposal Writer",

            "🌐 AI Website Builder",

            "📈 AI SEO Expert",

            "📱 AI Social Media Manager",

            "📧 AI Cold Outreach",

            "✍ AI Copywriter",

            "📊 AI Project Manager",

        ]

    )

    st.divider()

    if employee == "💼 AI Sales Manager":

        sales_manager()

    elif employee == "🎨 AI Creative Director":

        creative_director()

    elif employee == "🧠 AI Business Consultant":

        business_consultant()

    elif employee == "📄 AI Proposal Writer":
        proposal_writer()

        st.info("🚧 Coming Soon")

    elif employee == "🌐 AI Website Builder":

        from ai_employees.website_builder import show
        show()

    elif employee == "📈 AI SEO Expert":
        seo_expert()

        st.info("🚧 Coming Soon")

    elif employee == "📱 AI Social Media Manager":

        from ai_employees.social_media_manager import show
        show()

    elif employee == "📧 AI Cold Outreach":

        from ai_employees.cold_outreach import show
        show()

    elif employee == "✍ AI Copywriter":

        from ai_employees.copywriter import show
        show()

    elif employee == "📊 AI Project Manager":

        from ai_employees.project_manager import show
        show()