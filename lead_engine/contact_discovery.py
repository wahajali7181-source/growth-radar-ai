from services.email_finder import find_emails
from services.phone_finder import find_phones
from services.social_finder import find_social_links


def discover_contacts(website):

    result = {

        "emails": [],

        "phones": [],

        "socials": {}

    }

    if not website:

        return result

    result["emails"] = find_emails(website)

    result["phones"] = find_phones(website)

    result["socials"] = find_social_links(website)

    return result