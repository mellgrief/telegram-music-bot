import os
from dataclasses import dataclass
from typing import List, Tuple

import diskcache
from googleapiclient.discovery import build
from pytube import YouTube, Stream


@dataclass
class YoutubeVideo:
    video_title: str
    video_id: str


class YouTubeApi:

    def __init__(self, token: str):
        self._youtube = build("youtube", "v3", developerKey=token)
        self._cache = diskcache.Cache(
            "cache",
            size_limit=10 * 1024 * 1024,
        )

    def search_music(self, query: str) -> List[YoutubeVideo]:

        request = self._youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=6,
            videoCategoryId="10"
        )
        response = request.execute()

        return [YoutubeVideo(item["snippet"]["title"], item["id"]["videoId"]) for item in response["items"]]

    def cache_audio(self, video_id: str, audio_stream: 'Stream') -> bytes:
        if video_id not in self._cache:
            print("Downloading ", video_id)
            audio_stream.download(filename=f"tempAudios/{video_id}.mp3")
            with open(f"tempAudios/{video_id}.mp3", "rb") as audio:
                self._cache.set(video_id, audio.read(), expire=24 * 60 * 60)
            os.remove(f"tempAudios/{video_id}.mp3")
        return self._cache[video_id]

    def download_audio(self, video_id: str) -> Tuple[str, bytes]:
        video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        audio_stream = video.streams.filter(only_audio=True).first()
        audio_data = self.cache_audio(video_id, audio_stream)
        return video.title, audio_data
