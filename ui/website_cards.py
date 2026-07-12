import streamlit as st


def show_overview_card(scanner):

    st.markdown("## 🌐 Website Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Website Status",
            scanner["status"]
        )

    with c2:
        st.metric(
            "SSL",
            scanner["ssl"]
        )

    with c3:
        st.metric(
            "Load Time",
            scanner["load_time"]
        )

    st.info(
        f"📄 {scanner['title']}"
    )


def show_seo_card(seo):

    st.markdown("## 🔍 SEO Intelligence")

    c1, c2 = st.columns(2)

    with c1:

        st.success(
            f"Canonical\n\n{seo['canonical']}"
        )

        st.success(
            f"Robots\n\n{seo['robots_txt']}"
        )

        st.success(
            f"Sitemap\n\n{seo['sitemap_xml']}"
        )

    with c2:

        st.info(
            f"Language : {seo['language']}"
        )

        st.info(
            f"H1 Count : {seo['h1_count']}"
        )

        st.info(
            f"Open Graph : {seo['open_graph']}"
        )

        st.info(
            f"Twitter Cards : {seo['twitter_cards']}"
        )


def show_security_card(security):

    st.markdown("## 🛡 Security Intelligence")

    c1, c2 = st.columns(2)

    with c1:

        st.success(
            f"SSL : {security['ssl']}"
        )

        st.success(
            f"HSTS : {security['hsts']}"
        )

        st.success(
            f"CSP : {security['content_security_policy']}"
        )

    with c2:

        st.info(
            f"Server : {security['server']}"
        )

        st.info(
            f"X-Frame : {security['x_frame_options']}"
        )

        st.info(
            f"Referrer : {security['referrer_policy']}"
        )