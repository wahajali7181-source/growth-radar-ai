import re


def _safe_text(value):
    """
    Convert any value into safe HTML text.
    """

    if value is None:
        return ""

    text = str(value)

    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _safe_color(value, fallback):
    """
    Return a safe CSS color value.
    """

    if not value:
        return fallback

    value = str(value).strip()

    if re.fullmatch(
        r"#[0-9a-fA-F]{3,8}",
        value
    ):
        return value

    allowed = {
        "white",
        "black",
        "red",
        "blue",
        "green",
        "gray",
        "grey",
        "orange",
        "purple",
        "yellow",
        "pink",
        "transparent",
    }

    if value.lower() in allowed:
        return value

    return fallback


def _normalize_pages(pages):
    """
    Convert the pages input into a normalized set.
    """

    if isinstance(
        pages,
        str
    ):
        page_list = pages.split(",")

    elif isinstance(
        pages,
        list
    ):
        page_list = pages

    else:
        page_list = []

    normalized = set()

    for page in page_list:

        page_name = str(
            page
        ).strip().lower()

        if page_name:
            normalized.add(
                page_name
            )

    return normalized


def build_react_template(
    data,
    pages=None
):

    if not isinstance(
        data,
        dict
    ):
        return None

    selected_pages = _normalize_pages(
        pages
    )

    # Backward compatibility:
    # If pages are not supplied, generate the
    # complete standard website.
    if not selected_pages:

        selected_pages = {
            "home",
            "about",
            "services",
            "testimonials",
            "faq",
            "contact",
        }

    name = _safe_text(
        data.get(
            "name",
            "Business Website"
        )
    )

    industry = _safe_text(
        data.get(
            "industry",
            ""
        )
    )

    hero = data.get(
        "hero",
        {}
    )

    if not isinstance(
        hero,
        dict
    ):
        hero = {}

    hero_title = _safe_text(
        hero.get(
            "title",
            "Welcome to Our Business"
        )
    )

    hero_description = _safe_text(
        hero.get(
            "description",
            (
                "Professional services designed "
                "around your needs."
            )
        )
    )

    hero_button = _safe_text(
        hero.get(
            "button",
            "Get Started"
        )
    )

    about = _safe_text(
        data.get(
            "about",
            (
                "Learn more about our business "
                "and services."
            )
        )
    )

    services = data.get(
        "services",
        []
    )

    if not isinstance(
        services,
        list
    ):
        services = []

    testimonials = data.get(
        "testimonials",
        []
    )

    if not isinstance(
        testimonials,
        list
    ):
        testimonials = []

    faq = data.get(
        "faq",
        []
    )

    if not isinstance(
        faq,
        list
    ):
        faq = []

    colors = data.get(
        "colors",
        {}
    )

    if not isinstance(
        colors,
        dict
    ):
        colors = {}

    primary = _safe_color(
        colors.get(
            "primary"
        ),
        "#2563EB"
    )

    secondary = _safe_color(
        colors.get(
            "secondary"
        ),
        "#FFFFFF"
    )

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    nav_links = ""

    page_labels = [
        (
            "home",
            "Home",
        ),
        (
            "about",
            "About",
        ),
        (
            "services",
            "Services",
        ),
        (
            "testimonials",
            "Testimonials",
        ),
        (
            "faq",
            "FAQ",
        ),
        (
            "contact",
            "Contact",
        ),
    ]

    for page_id, label in page_labels:

        if page_id not in selected_pages:
            continue

        if (
            page_id == "testimonials"
            and not testimonials
        ):
            continue

        nav_links += f"""
                        <a href="#{page_id}">
                            {label}
                        </a>
        """

    # ==========================================================
    # SERVICES
    # ==========================================================

    service_cards = ""

    for service in services:

        service_name = _safe_text(
            service
        )

        if not service_name:
            continue

        service_cards += f"""
                        <div className="service-card">

                            <div className="service-icon">
                                ✓
                            </div>

                            <h3>
                                {service_name}
                            </h3>

                            <p>
                                Professional service designed
                                to meet your needs.
                            </p>

                        </div>
        """

    # ==========================================================
    # TESTIMONIALS
    # ==========================================================

    testimonial_cards = ""

    for item in testimonials:

        if not isinstance(
            item,
            dict
        ):
            continue

        person = _safe_text(
            item.get(
                "name",
                "Customer"
            )
        )

        review = _safe_text(
            item.get(
                "review",
                ""
            )
        )

        if not review:
            continue

        testimonial_cards += f"""
                        <div className="testimonial-card">

                            <p>
                                "{review}"
                            </p>

                            <strong>
                                {person}
                            </strong>

                        </div>
        """

    # ==========================================================
    # FAQ
    # ==========================================================

    faq_items = ""

    for item in faq:

        if not isinstance(
            item,
            dict
        ):
            continue

        question = _safe_text(
            item.get(
                "question",
                ""
            )
        )

        answer = _safe_text(
            item.get(
                "answer",
                ""
            )
        )

        if not question:
            continue

        faq_items += f"""
                        <div className="faq-item">

                            <h3>
                                {question}
                            </h3>

                            <p>
                                {answer}
                            </p>

                        </div>
        """

    # ==========================================================
    # PAGE SECTIONS
    # ==========================================================

    sections = ""

    # ----------------------------------------------------------
    # HOME
    # ----------------------------------------------------------

    if "home" in selected_pages:

        sections += f"""
                <section
                    id="home"
                    className="hero"
                >

                    <div
                        className="
                            container
                            hero-content
                        "
                    >

                        <div className="hero-text">

                            <span className="eyebrow">
                                {industry}
                            </span>

                            <h1>
                                {hero_title}
                            </h1>

                            <p>
                                {hero_description}
                            </p>

                            <a
                                href="#contact"
                                className="primary-button"
                            >
                                {hero_button}
                            </a>

                        </div>

                    </div>

                </section>
        """

    # ----------------------------------------------------------
    # ABOUT
    # ----------------------------------------------------------

    if "about" in selected_pages:

        sections += f"""
                <section
                    id="about"
                    className="section"
                >

                    <div className="container">

                        <div className="section-heading">

                            <span>
                                ABOUT
                            </span>

                            <h2>
                                About {name}
                            </h2>

                        </div>

                        <div className="about-card">

                            <p>
                                {about}
                            </p>

                        </div>

                    </div>

                </section>
        """

    # ----------------------------------------------------------
    # SERVICES
    # ----------------------------------------------------------

    if (
        "services" in selected_pages
        and service_cards
    ):

        sections += f"""
                <section
                    id="services"
                    className="
                        section
                        services-section
                    "
                >

                    <div className="container">

                        <div className="section-heading">

                            <span>
                                SERVICES
                            </span>

                            <h2>
                                What We Offer
                            </h2>

                        </div>

                        <div className="services-grid">

                            {service_cards}

                        </div>

                    </div>

                </section>
        """

    # ----------------------------------------------------------
    # TESTIMONIALS
    # ----------------------------------------------------------

    if (
        "testimonials" in selected_pages
        and testimonial_cards
    ):

        sections += f"""
                <section
                    id="testimonials"
                    className="section"
                >

                    <div className="container">

                        <div className="section-heading">

                            <span>
                                TESTIMONIALS
                            </span>

                            <h2>
                                What Our Customers Say
                            </h2>

                        </div>

                        <div
                            className="
                                testimonials-grid
                            "
                        >

                            {testimonial_cards}

                        </div>

                    </div>

                </section>
        """

    # ----------------------------------------------------------
    # FAQ
    # ----------------------------------------------------------

    if (
        "faq" in selected_pages
        and faq_items
    ):

        sections += f"""
                <section
                    id="faq"
                    className="
                        section
                        faq-section
                    "
                >

                    <div className="container">

                        <div className="section-heading">

                            <span>
                                FAQ
                            </span>

                            <h2>
                                Frequently Asked Questions
                            </h2>

                        </div>

                        <div className="faq-list">

                            {faq_items}

                        </div>

                    </div>

                </section>
        """

    # ----------------------------------------------------------
    # CONTACT
    # ----------------------------------------------------------

    if "contact" in selected_pages:

        sections += f"""
                <section
                    id="contact"
                    className="contact-section"
                >

                    <div className="container">

                        <div className="contact-card">

                            <div>

                                <span className="eyebrow">
                                    GET STARTED
                                </span>

                                <h2>
                                    Ready to get started?
                                </h2>

                                <p>
                                    Contact {name} to learn more
                                    about the available services.
                                </p>

                            </div>

                            <a
                                href="mailto:"
                                className="primary-button"
                            >
                                {hero_button}
                            </a>

                        </div>

                    </div>

                </section>
        """

    # ==========================================================
    # CONTACT BUTTON TARGET
    # ==========================================================

    contact_target = (
        "#contact"
        if "contact" in selected_pages
        else "#home"
    )

    # ==========================================================
    # FINAL REACT PROJECT
    # ==========================================================

    project = f"""
import "./App.css";

function App() {{

    return (

        <div
            className="website"
            style={{{{
                "--primary": "{primary}",
                "--secondary": "{secondary}"
            }}}}
        >

            <nav className="navbar">

                <div className="container nav-inner">

                    <div className="logo">
                        {name}
                    </div>

                    <div className="nav-links">

                        {nav_links}

                    </div>

                    <a
                        href="{contact_target}"
                        className="nav-button"
                    >
                        {hero_button}
                    </a>

                </div>

            </nav>

            <main>

                {sections}

            </main>

            <footer>

                <div
                    className="
                        container
                        footer-inner
                    "
                >

                    <div>

                        <strong>
                            {name}
                        </strong>

                        <p>
                            {industry}
                        </p>

                    </div>

                    <p>
                        © 2026 {name}.
                        All rights reserved.
                    </p>

                </div>

            </footer>

        </div>

    );

}}

export default App;
"""

    return project