
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
                        Growth Test Clinic
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
                        Book Now
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
                                dental clinic
                            </span>

                            <h1>
                                Quality Dental Care For Your Family
                            </h1>

                            <p>
                                Providing professional dental services in a comfortable environment.
                            </p>

                            <a
                                href="#contact"
                                className="primary-button"
                            >
                                Book Now
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
                                About Growth Test Clinic
                            </h2>

                        </div>

                        <div className="about-card">

                            <p>
                                Growth Test Clinic is dedicated to offering comprehensive dental care tailored to meet the needs of local patients.
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
            <h3>Preventive Care</h3>
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
            <h3>What are your business hours?</h3>
            <p>Our clinic hours are Monday to Friday from 9 AM to 5 PM.</p>
        </div>
        
        <div className="faq-item">
            <h3>Do you accept insurance?</h3>
            <p>We accept most major dental insurance plans.</p>
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
                                    Contact Growth Test Clinic to learn more
                                    about the available services.
                                </p>

                            </div>

                            <a
                                href="mailto:"
                                className="primary-button"
                            >
                                Book Now
                            </a>

                        </div>

                    </div>

                </section>

            </main>


            <footer>

                <div className="container footer-inner">

                    <div>
                        <strong>
                            Growth Test Clinic
                        </strong>

                        <p>
                            dental clinic
                        </p>
                    </div>

                    <p>
                        © 2026 Growth Test Clinic. All rights reserved.
                    </p>

                </div>

            </footer>

        </div>

    )

}

export default App
