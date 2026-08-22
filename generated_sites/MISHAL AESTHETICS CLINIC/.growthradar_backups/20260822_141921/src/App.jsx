
import './App.css'

function App() {

    return (

        <div
            className="website"
            style={{
                '--primary': '#2563EB',
                '--secondary': '#FFFFFF'
            }}
        >

            <nav className="navbar">

                <div className="container nav-inner">

                    <div className="logo">
                        MISHAL AESTHETICS CLINIC
                    </div>

                    <div className="nav-links">

                        <a href="#home">
                            Home
                        </a>

                        <a href="#about">
                            About
                        </a>

                        <a href="#services">
                            Services
                        </a>

                        <a href="#faq">
                            FAQ
                        </a>

                        <a href="#contact">
                            Contact
                        </a>

                    </div>

                    <a
                        href="#contact"
                        className="nav-button"
                    >
                        BOOK NOW
                    </a>

                </div>

            </nav>


            <main>

                <section
                    id="home"
                    className="hero"
                >

                    <div className="container hero-content">

                        <div className="hero-text">

                            <span className="eyebrow">
                                AESTHETICS CLINIC
                            </span>

                            <h1>
                                Welcome to Mishal Aesthetics Clinic
                            </h1>

                            <p>
                                Professional aesthetic treatments tailored for local patients.
                            </p>

                            <a
                                href="#contact"
                                className="primary-button"
                            >
                                BOOK NOW
                            </a>

                        </div>

                    </div>

                </section>


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
                                About MISHAL AESTHETICS CLINIC
                            </h2>

                        </div>

                        <div className="about-card">

                            <p>
                                Mishal Aesthetics Clinic provides expert aesthetic treatments in a professional and welcoming environment.
                            </p>

                        </div>

                    </div>

                </section>


                <section
                    id="services"
                    className="section services-section"
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

                            
        <div className="service-card">
            <div className="service-icon">✓</div>
            <h3>Skin Treatments</h3>
            <p>
                Professional service designed to meet your needs.
            </p>
        </div>
        
        <div className="service-card">
            <div className="service-icon">✓</div>
            <h3>Laser Therapy</h3>
            <p>
                Professional service designed to meet your needs.
            </p>
        </div>
        
        <div className="service-card">
            <div className="service-icon">✓</div>
            <h3>Injectables</h3>
            <p>
                Professional service designed to meet your needs.
            </p>
        </div>
        

                        </div>

                    </div>

                </section>


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

                        <div className="testimonials-grid">

                            

                        </div>

                    </div>

                </section>


                <section
                    id="faq"
                    className="section faq-section"
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

                            
        <div className="faq-item">
            <h3>What services do you offer?</h3>
            <p>We offer a range of aesthetic treatments including skin treatments, laser therapy, and injectables.</p>
        </div>
        

                        </div>

                    </div>

                </section>


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
                                    Contact MISHAL AESTHETICS CLINIC to learn more
                                    about the available services.
                                </p>

                            </div>

                            <a
                                href="mailto:"
                                className="primary-button"
                            >
                                BOOK NOW
                            </a>

                        </div>

                    </div>

                </section>

            </main>


            <footer>

                <div className="container footer-inner">

                    <div>
                        <strong>
                            MISHAL AESTHETICS CLINIC
                        </strong>

                        <p>
                            AESTHETICS CLINIC
                        </p>
                    </div>

                    <p>
                        © 2026 MISHAL AESTHETICS CLINIC. All rights reserved.
                    </p>

                </div>

            </footer>

        </div>

    )

}

export default App
