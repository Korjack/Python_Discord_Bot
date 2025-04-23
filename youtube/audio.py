import asyncio
from yt_dlp import YoutubeDL
import os

from config import AUDIO_PATH

async def download_audio(url: str, filename: str):
    os.makedirs(AUDIO_PATH, exist_ok=True)
    filename = os.path.join(AUDIO_PATH, filename)

    loop = asyncio.get_event_loop()

    def run():
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "outtmpl": filename.replace(".mp3", ".%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    await loop.run_in_executor(None, run)
