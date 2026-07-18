import requests
from bs4 import BeautifulSoup
import time


class WebsiteScanner:

    def __init__(self):

        self.timeout = 15

    def scan(self, website):

        result = {

            "status": "Offline",
            "status_code": "N/A",
            "ssl": "❌ No",
            "load_time": "N/A",
            "title": "Not Found",
            "meta_description": "Not Found",
            "favicon": "❌ Not Found"

        }

        if not website:

            return result

        try:

            start = time.time()

            response = requests.get(
                website,
                timeout=self.timeout,
                headers={
                    "User-Agent":
                    "Mozilla/5.0"
                }
            )

            load = round(
                time.time() - start,
                2
            )

            result["status"] = "Online"

            result["status_code"] = response.status_code

            result["load_time"] = str(load) + " sec"

            if website.startswith("https"):

                result["ssl"] = "✅ Yes"

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            title = soup.find("title")

            if title:

                result["title"] = title.text.strip()

            meta = soup.find(
                "meta",
                attrs={
                    "name": "description"
                }
            )

            if meta:

                result["meta_description"] = meta.get(
                    "content",
                    ""
                )

            favicon = soup.find(
                "link",
                rel=lambda x:
                x and "icon" in x.lower()
            )

            if favicon:

                result["favicon"] = "✅ Found"

            return result

        except Exception:

            return result


scanner = WebsiteScanner()