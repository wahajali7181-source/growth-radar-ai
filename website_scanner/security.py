import requests


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


def scan_security(website):

    result = {
        "ssl": "❌ Disabled",
        "server": "Unknown",
        "hsts": "❌ Missing",
        "content_security_policy": "❌ Missing",
        "x_frame_options": "❌ Missing",
        "x_content_type_options": "❌ Missing",
        "referrer_policy": "❌ Missing",
        "permissions_policy": "❌ Missing"
    }

    if not website:
        return result

    website = website.strip()

    if website.lower() == "no":
        return result

    if not website.startswith(("http://", "https://")):
        website = "https://" + website

    try:

        response = requests.get(
            website,
            headers=HEADERS,
            timeout=10
        )

        headers = response.headers

        if website.startswith("https://"):
            result["ssl"] = "✅ Enabled"

        result["server"] = headers.get(
            "Server",
            "Unknown"
        )

        if "Strict-Transport-Security" in headers:
            result["hsts"] = "✅ Enabled"

        if "Content-Security-Policy" in headers:
            result["content_security_policy"] = "✅ Enabled"

        if "X-Frame-Options" in headers:
            result["x_frame_options"] = headers["X-Frame-Options"]

        if "X-Content-Type-Options" in headers:
            result["x_content_type_options"] = headers["X-Content-Type-Options"]

        if "Referrer-Policy" in headers:
            result["referrer_policy"] = headers["Referrer-Policy"]

        if "Permissions-Policy" in headers:
            result["permissions_policy"] = "✅ Enabled"

    except Exception:
        pass

    return result