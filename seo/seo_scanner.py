import requests
from bs4 import BeautifulSoup


class SEOScanner:

    def scan(self, website):

        result = {
            "canonical": "❌ Not Found",
            "meta_keywords": "❌ Not Found",
            "open_graph": "❌ Not Found",
            "twitter_cards": "❌ Not Found",
            "robots_txt": "❌ Not Found",
            "sitemap_xml": "❌ Not Found",
            "language": "❌ Not Found",
            "charset": "❌ Not Found",
            "h1_count": 0
        }

        if not website:
            return result

        try:

            response = requests.get(
                website,
                timeout=15,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Canonical
            canonical = soup.find(
                "link",
                rel="canonical"
            )

            if canonical:
                result["canonical"] = "✅ Found"

            # Meta Keywords
            keywords = soup.find(
                "meta",
                attrs={"name": "keywords"}
            )

            if keywords:
                result["meta_keywords"] = "✅ Found"

            # Open Graph
            if soup.find(
                "meta",
                property="og:title"
            ):
                result["open_graph"] = "✅ Found"

            # Twitter Cards
            if soup.find(
                "meta",
                attrs={"name": "twitter:card"}
            ):
                result["twitter_cards"] = "✅ Found"

            # Language
            html = soup.find("html")

            if html and html.get("lang"):
                result["language"] = html.get("lang")

            # Charset
            charset = soup.find("meta", charset=True)

            if charset:
                result["charset"] = charset.get("charset")

            # H1 Count
            result["h1_count"] = len(
                soup.find_all("h1")
            )

            # robots.txt
            try:
                r = requests.get(
                    website.rstrip("/") + "/robots.txt",
                    timeout=5
                )

                if r.status_code == 200:
                    result["robots_txt"] = "✅ Found"

            except:
                pass

            # sitemap.xml
            try:
                s = requests.get(
                    website.rstrip("/") + "/sitemap.xml",
                    timeout=5
                )

                if s.status_code == 200:
                    result["sitemap_xml"] = "✅ Found"

            except:
                pass

            return result

        except Exception:

            return result


seo_scanner = SEOScanner()