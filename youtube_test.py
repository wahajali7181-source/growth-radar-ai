from trend_radar.youtube_engine import get_top_videos

videos = get_top_videos("AI Marketing")

for video in videos:

    print(video)