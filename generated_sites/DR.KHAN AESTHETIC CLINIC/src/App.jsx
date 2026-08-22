
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
                        DR.KHAN AESTHETIC CLINIC
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
                        BOOK APPOINTMENT
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
                                AESTHETIC CLINIC
                            </span>

                            <h1>
                                Welcome to DR.KHAN AESTHETIC CLINIC
                            </h1>

                            <p>
                                Professional aesthetic treatments tailored to your needs.
                            </p>

                            <a
                                href="#contact"
                                className="primary-button"
                            >
                                BOOK APPOINTMENT
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
                                About DR.KHAN AESTHETIC CLINIC
                            </h2>

                        </div>

                        <div className="about-card">

                            <p>
                                DR.KHAN AESTHETIC CLINIC provides a range of professional aesthetic treatments designed to meet the needs of local patients.
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
            <h3>Anti-Aging Solutions</h3>
            <p>
                Professional service designed to meet your needs.
            </p>
        </div>
        
        <div className="service-card">
            <div className="service-icon">✓</div>
            <h3>Body Contouring</h3>
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
            <p>We offer various aesthetic treatments including skin treatments, anti-aging solutions, and body contouring.</p>
        </div>
        
        <div className="faq-item">
            <h3>How can I book an appointment?</h3>
            <p>You can book an appointment by clicking the &#39;BOOK APPOINTMENT&#39; button on our website.</p>
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
                                    Contact DR.KHAN AESTHETIC CLINIC to learn more
                                    about the available services.
                                </p>

                            </div>

                            <a
                                href="mailto:"
                                className="primary-button"
                            >
                                BOOK APPOINTMENT
                            </a>

                        </div>

                    </div>

                </section>

            </main>


            <footer>

                <div className="container footer-inner">

                    <div>
                        <strong>
                            DR.KHAN AESTHETIC CLINIC
                        </strong>

                        <p>
                            AESTHETIC CLINIC
                        </p>
                    </div>

                    <p>
                        © 2026 DR.KHAN AESTHETIC CLINIC. All rights reserved.
                    </p>

                </div>

            </footer>

        </div>

    )

}

export default App
