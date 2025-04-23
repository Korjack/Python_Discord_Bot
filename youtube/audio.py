import os
import asyncio
from subprocess import run, PIPE
from yt_dlp import YoutubeDL
import discord

from config import AUDIO_PATH

async def download_audio(url: str, filename: str):
    os.makedirs(AUDIO_PATH, exist_ok=True)
    filename = os.path.join(AUDIO_PATH, filename)

    loop = asyncio.get_event_loop()

    def run_dl():
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

    await loop.run_in_executor(None, run_dl)

async def try_stream_or_download(vc, video_url: str, fallback_audio_path: str, volume: float):
    try:
        result = result = run(["yt-dlp", "-f", "bestaudio", "-g", video_url], stdout=PIPE, stderr=PIPE, text=True)

        stream_url = result.stdout.strip().splitlines()[0]

        if stream_url.startswith("http"):
            print("🎥 스트림 URL로 재생 중")
            ffmpeg_options = {
                "before_options": (
                    "-reconnect 1 "
                    "-reconnect_streamed 1 "
                    "-reconnect_delay_max 5 "
                    "-probesize 32 "
                    "-analyzeduration 0 "
                ),
                "options": (
                    '-vn '
                    f'-filter:a "volume={volume}"'
                )
            }
            vc.play(discord.FFmpegPCMAudio(stream_url, **ffmpeg_options))
            return
    except Exception as e:
        print("❌ 스트리밍 실패, 다운로드로 대체:", e)

    await download_audio(video_url, fallback_audio_path)

    ffmpeg_options = {
        "before_options": "-nostdin",
        "options": f'-vn -filter:a "volume={volume}"'
    }
    vc.play(discord.FFmpegPCMAudio(fallback_audio_path, **ffmpeg_options))