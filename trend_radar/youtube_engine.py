import os
import requests

from dotenv import load_dotenv


# ==========================================================
# CONFIG
# ==========================================================

load_dotenv(override=True)

YOUTUBE_API_URL = (
    "https://www.googleapis.com/youtube/v3"
)

REQUEST_TIMEOUT = 20


# ==========================================================
# API KEY
# ==========================================================

def get_api_key():

    key = os.getenv(
        "YOUTUBE_API_KEY"
    )

    if not key:

        raise RuntimeError(
            "YOUTUBE_API_KEY is not configured."
        )

    return key


# ==========================================================
# SEARCH VIDEOS
# ==========================================================

def get_top_videos(
    keyword,
    limit=10
):

    if not keyword or not keyword.strip():

        return []

    limit = max(
        1,
        min(
            int(limit),
            50
        )
    )

    params = {

        "part": "snippet",

        "q": keyword.strip(),

        "type": "video",

        "maxResults": limit,

        "order": "relevance",

        "key": get_api_key()

    }

    response = requests.get(

        f"{YOUTUBE_API_URL}/search",

        params=params,

        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()

    data = response.json()

    items = data.get(
        "items",
        []
    )

    video_ids = [

        item.get(
            "id",
            {}
        ).get(
            "videoId"
        )

        for item in items

        if item.get(
            "id",
            {}
        ).get(
            "videoId"
        )
    ]

    if not video_ids:

        return []

    # ======================================================
    # VIDEO STATISTICS
    # ======================================================

    stats_params = {

        "part": "snippet,statistics,contentDetails",

        "id": ",".join(
            video_ids
        ),

        "key": get_api_key()

    }

    stats_response = requests.get(

        f"{YOUTUBE_API_URL}/videos",

        params=stats_params,

        timeout=REQUEST_TIMEOUT
    )

    stats_response.raise_for_status()

    stats_data = stats_response.json()

    stats_map = {

        item.get("id"): item

        for item in stats_data.get(
            "items",
            []
        )
    }

    # ======================================================
    # BUILD RESULT
    # ======================================================

    videos = []

    for item in items:

        video_id = item.get(
            "id",
            {}
        ).get(
            "videoId"
        )

        if not video_id:
            continue

        snippet = item.get(
            "snippet",
            {}
        )

        details = stats_map.get(
            video_id,
            {}
        )

        statistics = details.get(
            "statistics",
            {}
        )

        content_details = details.get(
            "contentDetails",
            {}
        )

        videos.append({

            "title": snippet.get(
                "title"
            ),

            "channel": snippet.get(
                "channelTitle"
            ),

            "channel_id": snippet.get(
                "channelId"
            ),

            "video_id": video_id,

            "views": int(
                statistics.get(
                    "viewCount",
                    0
                )
            ),

            "likes": int(
                statistics.get(
                    "likeCount",
                    0
                )
            ),

            "comments": int(
                statistics.get(
                    "commentCount",
                    0
                )
            ),

            "published": snippet.get(
                "publishedAt"
            ),

            "duration": content_details.get(
                "duration"
            ),

            "thumbnail": (
                snippet.get(
                    "thumbnails",
                    {}
                )
                .get(
                    "high",
                    {}
                )
                .get(
                    "url"
                )
            ),

            "link": (
                f"https://www.youtube.com/watch?v={video_id}"
            )

        })

    return videos