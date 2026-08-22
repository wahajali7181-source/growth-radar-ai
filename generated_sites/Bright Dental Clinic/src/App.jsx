
import './App.css'

function App() {

    return (

        <div
            className="website"
            style={{
                '--primary': '#4C0519',
                '--secondary': '#FFFFFF'
            }}
        >

            <nav className="navbar">

                <div className="container nav-inner">

                    <div className="logo">
                        Bright DENTAL CLINIC
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
                                DENTIST
                            </span>

                            <h1>
                                Professional Dental Care
                            </h1>

                            <p>
                                Comprehensive dental services tailored to meet your needs.
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
                                About Bright DENTAL CLINIC
                            </h2>

                        </div>

                        <div className="about-card">

                            <p>
                                Bright DENTAL CLINIC provides personalized dental care for local patients. Our focus is on delivering quality treatments in a comfortable environment.
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
            <h3>General Dentistry</h3>
            <p>
                Professional service designed to meet your needs.
            </p>
        </div>
        
        <div className="service-card">
            <div className="service-icon">✓</div>
            <h3>Cosmetic Dentistry</h3>
            <p>
                Professional service designed to meet your needs.
            </p>
        </div>
        
        <div className="service-card">
            <div className="service-icon">✓</div>
            <h3>Preventive Care</h3>
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
            <p>We provide a range of dental services including general, cosmetic, and preventive care.</p>
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
                                    Contact Bright DENTAL CLINIC to learn more
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
                            Bright DENTAL CLINIC
                        </strong>

                        <p>
                            DENTIST
                        </p>
                    </div>

                    <p>
                        © 2026 Bright DENTAL CLINIC. All rights reserved.
                    </p>

                </div>

            </footer>

        </div>

    )

}

export default App
