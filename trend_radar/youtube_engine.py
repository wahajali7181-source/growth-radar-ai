from youtubesearchpython import VideosSearch


def get_top_videos(keyword, limit=10):

    search = VideosSearch(keyword, limit=limit)

    results = search.result()["result"]

    videos = []

    for video in results:

        videos.append({

            "title": video.get("title"),

            "channel": video.get("channel", {}).get("name"),

            "views": video.get("viewCount", {}).get("text"),

            "published": video.get("publishedTime"),

            "duration": video.get("duration"),

            "link": video.get("link")

        })

    return videos