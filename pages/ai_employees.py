import streamlit as st

from ai_employees.sales_manager import show as sales_manager
from ai_employees.creative_director import show as creative_director
from ai_employees.proposal_writer import show as proposal_writer
from ai_employees.seo_expert import show as seo_expert
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

        st.info("🚧 Coming Soon")

    elif employee == "📄 AI Proposal Writer":
        proposal_writer()

        st.info("🚧 Coming Soon")

    elif employee == "🌐 AI Website Builder":

        st.info("🚧 Coming Soon")

    elif employee == "📈 AI SEO Expert":
        seo_expert()

        st.info("🚧 Coming Soon")

    elif employee == "📱 AI Social Media Manager":

        st.info("🚧 Coming Soon")

    elif employee == "📧 AI Cold Outreach":

        st.info("🚧 Coming Soon")

    elif employee == "✍ AI Copywriter":

        st.info("🚧 Coming Soon")

    elif employee == "📊 AI Project Manager":

        st.info("🚧 Coming Soon")