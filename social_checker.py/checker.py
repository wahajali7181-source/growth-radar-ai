import requests


def check_socials(website):

    result = {
        "website": "❌ Not Found",
        "instagram": "❌ Not Found",
        "facebook": "❌ Not Found"
    }

    if not website:
        return result

    website = str(website)

    if website.lower() != "no":

        result["website"] = "✅ Found"

        try:

            response = requests.get(
                "https://" + website,
                timeout=5
            )

            html = response.text.lower()

            if "instagram.com" in html:
                result["instagram"] = "✅ Found"

            if "facebook.com" in html:
                result["facebook"] = "✅ Found"

        except:

            pass

    return result