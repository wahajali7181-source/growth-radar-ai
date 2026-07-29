import streamlit as st

from website_scanner.engine import analyze_website


def show():

    st.title("🌐 Website Intelligence")

    st.caption(
        "Complete Website Audit & AI Analysis"
    )

    st.divider()

    website = st.text_input(

        "Website URL",

        placeholder="https://example.com"

    )

    st.divider()

    if st.button(

        "🚀 Analyze Website",

        width="stretch"

    ):

        if not website:

            st.warning(

                "Please enter a website."

            )

            return

        with st.spinner(

            "Scanning website..."

        ):

            report = analyze_website(website)

        st.success(

            "Website analyzed successfully."

        )

        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(

            "Overall",

            f"{report['overall_score']}%"

        )

        c2.metric(

            "Health",

            f"{report['health']['score']}%"

        )

        c3.metric(

            "SEO",

            f"{report['seo']['score']}%"

        )

        c4.metric(

            "Security",

            f"{report['security']['score']}%"

        )

        st.metric(

            "Performance",

            f"{report['performance']['score']}%"

        )

        st.divider()

        st.subheader("❤️ Health")

        if report["health"]["recommendations"]:

            for item in report["health"]["recommendations"]:

                st.write(f"• {item}")

        else:

            st.success("No issues detected.")

        st.divider()

        st.subheader("🔍 SEO")

        if report["seo"]["recommendations"]:

            for item in report["seo"]["recommendations"]:

                st.write(f"• {item}")

        else:

            st.success("SEO looks good.")

        st.divider()

        st.subheader("🛡 Security")

        if report["security"]["recommendations"]:

            for item in report["security"]["recommendations"]:

                st.write(f"• {item}")

        else:

            st.success("Security looks good.")

        st.divider()

        st.subheader("⚡ Performance")

        if report["performance"]["recommendations"]:

            for item in report["performance"]["recommendations"]:

                st.write(f"• {item}")

        else:

            st.success("Performance looks good.")