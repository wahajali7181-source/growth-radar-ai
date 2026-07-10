from website_scanner.scanner import scan_website
from website_scanner.seo import scan_seo
from website_scanner.security import scan_security


def generate_report(website):

    report = {
        "scanner": scan_website(website),
        "seo": scan_seo(website),
        "security": scan_security(website)
    }

    return report