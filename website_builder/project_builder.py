import os
import re


def _safe_project_name(business_name):
    """
    Create a filesystem-safe project folder name.
    """

    name = str(business_name).strip()

    name = re.sub(
        r'[<>:"/\\|?*]',
        "",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    )

    return name or "Generated Website"


def create_project(
    business_name,
    app_code
):

    project_name = _safe_project_name(
        business_name
    )

    folder = os.path.join(
        "generated_sites",
        project_name
    )

    src = os.path.join(
        folder,
        "src"
    )

    os.makedirs(
        src,
        exist_ok=True
    )

    # ==========================================================
    # APP.JSX
    # ==========================================================

    app_path = os.path.join(
        src,
        "App.jsx"
    )

    with open(
        app_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            app_code or ""
        )

    # ==========================================================
    # MAIN.JSX
    # ==========================================================

    main_code = """import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./App.css";

ReactDOM.createRoot(
    document.getElementById("root")
).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
"""

    main_path = os.path.join(
        src,
        "main.jsx"
    )

    with open(
        main_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            main_code
        )

    # ==========================================================
    # APP.CSS
    # ==========================================================

    css_code = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
    font-family:
        Inter,
        ui-sans-serif,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    color: #172033;
    background: #ffffff;
    font-synthesis: none;
    text-rendering: optimizeLegibility;
}

* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    margin: 0;
    min-width: 320px;
    background: #ffffff;
}

body,
button,
a {
    font-family: inherit;
}

a {
    color: inherit;
    text-decoration: none;
}

button {
    border: 0;
    cursor: pointer;
}

.website {
    min-height: 100vh;
    background: var(--secondary);
    color: #172033;
}

/* ==========================================================
   CONTAINER
   ========================================================== */

.container {
    width: min(1120px, calc(100% - 40px));
    margin: 0 auto;
}

/* ==========================================================
   NAVIGATION
   ========================================================== */

.navbar {
    position: sticky;
    top: 0;
    z-index: 100;

    background: rgba(255, 255, 255, 0.92);
    border-bottom: 1px solid #e9edf3;

    backdrop-filter: blur(14px);
}

.nav-inner {
    min-height: 76px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    gap: 24px;
}

.logo {
    color: var(--primary);

    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.03em;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 28px;
}

.nav-links a {
    color: #5c6678;

    font-size: 14px;
    font-weight: 600;

    transition:
        color 0.2s ease;
}

.nav-links a:hover {
    color: var(--primary);
}

.nav-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    min-height: 42px;
    padding: 0 18px;

    color: #ffffff;
    background: var(--primary);

    border-radius: 10px;

    font-size: 14px;
    font-weight: 700;

    box-shadow:
        0 8px 20px rgba(0, 0, 0, 0.08);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.nav-button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 12px 26px rgba(0, 0, 0, 0.12);
}

/* ==========================================================
   HERO
   ========================================================== */

.hero {
    position: relative;
    overflow: hidden;

    min-height: 620px;

    display: flex;
    align-items: center;

    background:
        radial-gradient(
            circle at 80% 20%,
            color-mix(
                in srgb,
                var(--primary) 12%,
                transparent
            ),
            transparent 38%
        ),
        linear-gradient(
            135deg,
            #ffffff 0%,
            #f7faff 100%
        );
}

.hero::before {
    content: "";

    position: absolute;
    width: 420px;
    height: 420px;

    right: -180px;
    bottom: -220px;

    background: var(--primary);

    opacity: 0.06;

    border-radius: 50%;
}

.hero-content {
    position: relative;
    z-index: 1;

    padding: 100px 0;
}

.hero-text {
    max-width: 760px;
}

.eyebrow {
    display: inline-block;

    margin-bottom: 18px;

    color: var(--primary);

    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.hero h1 {
    max-width: 780px;

    margin: 0 0 24px;

    color: #101828;

    font-size: clamp(
        44px,
        7vw,
        76px
    );

    line-height: 0.98;
    letter-spacing: -0.055em;
}

.hero p {
    max-width: 680px;

    margin: 0 0 34px;

    color: #667085;

    font-size: 19px;
    line-height: 1.75;
}

.primary-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    min-height: 52px;
    padding: 0 24px;

    color: #ffffff;
    background: var(--primary);

    border-radius: 12px;

    font-size: 15px;
    font-weight: 800;

    box-shadow:
        0 12px 30px rgba(0, 0, 0, 0.12);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.primary-button:hover {
    transform: translateY(-3px);

    box-shadow:
        0 18px 34px rgba(0, 0, 0, 0.16);
}

/* ==========================================================
   SECTIONS
   ========================================================== */

.section {
    padding: 110px 0;
}

.section-heading {
    max-width: 700px;

    margin-bottom: 54px;
}

.section-heading span {
    color: var(--primary);

    font-size: 12px;
    font-weight: 800;

    letter-spacing: 0.14em;
}

.section-heading h2 {
    margin: 12px 0 0;

    color: #101828;

    font-size: clamp(
        34px,
        5vw,
        52px
    );

    line-height: 1.05;
    letter-spacing: -0.045em;
}

/* ==========================================================
   ABOUT
   ========================================================== */

.about-card {
    max-width: 900px;

    padding: 38px;

    background: #f8fafc;

    border: 1px solid #e7ebf0;
    border-radius: 20px;
}

.about-card p {
    margin: 0;

    color: #667085;

    font-size: 18px;
    line-height: 1.85;
}

/* ==========================================================
   SERVICES
   ========================================================== */

.services-section {
    background: #f8fafc;
}

.services-grid {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 22px;
}

.service-card {
    min-height: 220px;

    padding: 30px;

    background: #ffffff;

    border: 1px solid #e7ebf0;
    border-radius: 18px;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border-color 0.25s ease;
}

.service-card:hover {
    transform: translateY(-6px);

    border-color: var(--primary);

    box-shadow:
        0 20px 50px rgba(16, 24, 40, 0.09);
}

.service-icon {
    width: 42px;
    height: 42px;

    display: flex;
    align-items: center;
    justify-content: center;

    margin-bottom: 24px;

    color: #ffffff;
    background: var(--primary);

    border-radius: 12px;

    font-weight: 900;
}

.service-card h3 {
    margin: 0 0 12px;

    color: #101828;

    font-size: 20px;
}

.service-card p {
    margin: 0;

    color: #667085;

    line-height: 1.7;
}

/* ==========================================================
   TESTIMONIALS
   ========================================================== */

.testimonials-grid {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 22px;
}

.testimonial-card {
    padding: 30px;

    background: #ffffff;

    border: 1px solid #e7ebf0;
    border-radius: 18px;
}

.testimonial-card p {
    margin: 0 0 22px;

    color: #475467;

    line-height: 1.75;
}

.testimonial-card strong {
    color: #101828;
}

/* ==========================================================
   FAQ
   ========================================================== */

.faq-section {
    background: #f8fafc;
}

.faq-list {
    max-width: 850px;
}

.faq-item {
    padding: 28px 0;

    border-bottom: 1px solid #dfe4ea;
}

.faq-item:first-child {
    border-top: 1px solid #dfe4ea;
}

.faq-item h3 {
    margin: 0 0 10px;

    color: #101828;

    font-size: 18px;
}

.faq-item p {
    margin: 0;

    color: #667085;

    line-height: 1.75;
}

/* ==========================================================
   CONTACT
   ========================================================== */

.contact-section {
    padding: 90px 0;
}

.contact-card {
    display: flex;
    align-items: center;
    justify-content: space-between;

    gap: 40px;

    padding: 54px;

    color: #ffffff;
    background: var(--primary);

    border-radius: 24px;

    box-shadow:
        0 24px 60px rgba(0, 0, 0, 0.14);
}

.contact-card .eyebrow {
    color: rgba(255, 255, 255, 0.75);
}

.contact-card h2 {
    margin: 0 0 14px;

    font-size: clamp(
        32px,
        5vw,
        48px
    );

    line-height: 1;
    letter-spacing: -0.04em;
}

.contact-card p {
    max-width: 600px;

    margin: 0;

    color: rgba(255, 255, 255, 0.82);

    line-height: 1.7;
}

.contact-card .primary-button {
    flex-shrink: 0;

    color: var(--primary);
    background: #ffffff;
}

/* ==========================================================
   FOOTER
   ========================================================== */

footer {
    padding: 40px 0;

    background: #0f172a;

    color: #ffffff;
}

.footer-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;

    gap: 30px;
}

.footer-inner strong {
    font-size: 18px;
}

.footer-inner p {
    margin: 5px 0 0;

    color: #94a3b8;

    font-size: 14px;
}

/* ==========================================================
   RESPONSIVE
   ========================================================== */

@media (max-width: 900px) {

    .nav-links {
        display: none;
    }

    .hero {
        min-height: 540px;
    }

    .services-grid,
    .testimonials-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }

    .contact-card {
        flex-direction: column;
        align-items: flex-start;
    }

}

@media (max-width: 640px) {

    .container {
        width: min(
            100% - 28px,
            1120px
        );
    }

    .nav-inner {
        min-height: 68px;
    }

    .nav-button {
        display: none;
    }

    .hero-content {
        padding: 80px 0;
    }

    .hero h1 {
        font-size: 46px;
    }

    .hero p {
        font-size: 17px;
    }

    .section {
        padding: 80px 0;
    }

    .services-grid,
    .testimonials-grid {
        grid-template-columns: 1fr;
    }

    .about-card {
        padding: 25px;
    }

    .contact-card {
        padding: 32px 25px;
        border-radius: 18px;
    }

    .footer-inner {
        flex-direction: column;
        align-items: flex-start;
    }

}
"""

    css_path = os.path.join(
        src,
        "App.css"
    )

    with open(
        css_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            css_code
        )

    # ==========================================================
    # INDEX.HTML
    # ==========================================================

    index_code = """<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    />
    <meta
        name="description"
        content="Generated business website"
    />
    <title>Generated Website</title>
</head>

<body>

    <div id="root"></div>

    <script
        type="module"
        src="/src/main.jsx"
    ></script>

</body>
</html>
"""

    index_path = os.path.join(
        folder,
        "index.html"
    )

    with open(
        index_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            index_code
        )

    # ==========================================================
    # PACKAGE.JSON
    # ==========================================================

    package_json = """{
  "name": "generated-business-website",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@vitejs/plugin-react": "latest",
    "vite": "latest",
    "react": "latest",
    "react-dom": "latest",
    "tailwindcss": "latest"
  },
  "devDependencies": {}
}
"""

    package_path = os.path.join(
        folder,
        "package.json"
    )

    with open(
        package_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            package_json
        )

    # ==========================================================
    # VITE CONFIG
    # ==========================================================

    vite_config = """import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()]
});
"""

    vite_path = os.path.join(
        folder,
        "vite.config.js"
    )

    with open(
        vite_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            vite_config
        )

    # ==========================================================
    # TAILWIND CONFIG
    # ==========================================================

    tailwind_config = """export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}"
    ],
    theme: {
        extend: {}
    },
    plugins: []
};
"""

    tailwind_path = os.path.join(
        folder,
        "tailwind.config.js"
    )

    with open(
        tailwind_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            tailwind_config
        )

    return folder