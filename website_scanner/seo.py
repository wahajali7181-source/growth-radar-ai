import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


def scan_seo(website):

    result = {
        "canonical": "❌ Not Found",
        "meta_keywords": "❌ Not Found",
        "open_graph": "❌ Not Found",
        "twitter_cards": "❌ Not Found",
        "robots_txt": "❌ Not Found",
        "sitemap_xml": "❌ Not Found",
        "language": "❌ Not Found",
        "charset": "❌ Not Found",
        "h1_count": 0,
    }

    if not website:
        return result

    website = website.strip()

    if not website.startswith(("http://", "https://")):
        website = "https://" + website

    try:

        response = requests.get(
            website,
            headers=HEADERS,
            timeout=10
        )

        soup = BeautifulSoup(response.text, "lxml")

        # Canonical
        canonical = soup.find("link", rel="canonical")

        if canonical and canonical.get("href"):
            result["canonical"] = canonical["href"]

        # Meta Keywords
        keywords = soup.find(
            "meta",
            attrs={"name": "keywords"}
        )

        if keywords and keywords.get("content"):
            result["meta_keywords"] = keywords["content"]

        # Open Graph
        og = soup.find(
            "meta",
            attrs={"property": "og:title"}
        )

        if og:
            result["open_graph"] = "✅ Present"

        # Twitter Cards
        twitter = soup.find(
            "meta",
            attrs={"name": "twitter:card"}
        )

        if twitter:
            result["twitter_cards"] = "✅ Present"

        # Language
        html = soup.find("html")

        if html and html.get("lang"):
            result["language"] = html["lang"]

        # Charset
        charset = soup.find("meta", charset=True)

        if charset:
            result["charset"] = charset["charset"]

        # H1 Count
        result["h1_count"] = len(
            soup.find_all("h1")
        )

        # robots.txt
        robots = urljoin(
            website,
            "/robots.txt"
        )

        r = requests.get(
            robots,
            headers=HEADERS,
            timeout=5
        )

        if r.status_code == 200:
            result["robots_txt"] = robots

        # sitemap.xml
        sitemap = urljoin(
            website,
            "/sitemap.xml"
        )

        s = requests.get(
            sitemap,
            headers=HEADERS,
            timeout=5
        )

        if s.status_code == 200:
            result["sitemap_xml"] = sitemap

    except Exception:
        pass

    return result