
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
                        MISHAL DENTAL CLINIC
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
                        SCHEDULE YOUR APPOINTMENT
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
                                Providing quality dental services for local patients.
                            </p>

                            <a
                                href="#contact"
                                className="primary-button"
                            >
                                SCHEDULE YOUR APPOINTMENT
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
                                About MISHAL DENTAL CLINIC
                            </h2>

                        </div>

                        <div className="about-card">

                            <p>
                                Mishal Dental Clinic offers professional dental services tailored to meet the needs of local patients. Our team is dedicated to providing personalized care in a comfortable environment.
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
            <h3>Teeth Cleaning</h3>
            <p>
                Professional service designed to meet your needs.
            </p>
        </div>
        
        <div className="service-card">
            <div className="service-icon">✓</div>
            <h3>Dental Checkups</h3>
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
            <h3>What are your operating hours?</h3>
            <p>Our clinic is open from Monday to Friday, 9 AM to 5 PM.</p>
        </div>
        
        <div className="faq-item">
            <h3>Do you accept insurance?</h3>
            <p>We accept most major dental insurance plans. Please contact us for details.</p>
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
                                    Contact MISHAL DENTAL CLINIC to learn more
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
                            MISHAL DENTAL CLINIC
                        </strong>

                        <p>
                            DENTIST
                        </p>
                    </div>

                    <p>
                        © 2026 MISHAL DENTAL CLINIC. All rights reserved.
                    </p>

                </div>

            </footer>

        </div>

    )

}

export default App
