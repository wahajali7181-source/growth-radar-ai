class ScoreEngine:

    def calculate(

        self,

        scanner,

        seo

    ):

        score = 0

        # Website

        if scanner["status"] == "Online":
            score += 15

        if scanner["ssl"] == "✅ Yes":
            score += 10

        if scanner["title"] != "Not Found":
            score += 5

        if scanner["meta_description"] != "Not Found":
            score += 10

        if scanner["favicon"] == "✅ Found":
            score += 5

        # SEO

        if seo["canonical"] == "✅ Found":
            score += 5

        if seo["open_graph"] == "✅ Found":
            score += 5

        if seo["twitter_cards"] == "✅ Found":
            score += 5

        if seo["robots_txt"] == "✅ Found":
            score += 10

        if seo["sitemap_xml"] == "✅ Found":
            score += 10

        if seo["h1_count"] > 0:
            score += 10

        return min(score, 100)


score_engine = ScoreEngine()