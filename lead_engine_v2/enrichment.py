from services.email_finder import find_emails
from services.phone_finder import find_phones
from services.social_finder import find_social_links

from website_scanner.technology import detect_technology


def enrich_business(lead):

    website = lead.website.strip()

    if website == "":
        return lead

    try:

        emails = find_emails(website)

        if emails:
            lead.email = ", ".join(emails)

    except Exception:
        pass

    try:

        phones = find_phones(website)

        if phones:
            lead.phone = ", ".join(phones)

    except Exception:
        pass

    try:

        socials = find_social_links(website)

        lead.facebook = socials.get("facebook", "")
        lead.instagram = socials.get("instagram", "")
        lead.linkedin = socials.get("linkedin", "")
        lead.youtube = socials.get("youtube", "")
        lead.twitter = socials.get("twitter", "")

    except Exception:
        pass

    try:

        tech = detect_technology(website)

        if isinstance(tech, list):
            lead.technology = ", ".join(tech)
        else:
            lead.technology = str(tech)

    except Exception:
        pass

    return lead