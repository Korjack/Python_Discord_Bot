import discord
from datetime import timedelta
from youtube.search import get_video_dict
from ui.views import YouTubeView

def seconds_to_hms(seconds):
    return str(timedelta(seconds=seconds))

async def run_youtube_command(interaction: discord.Interaction, query: str, volume: int = 2):
    await interaction.response.defer()

    video_dict = get_video_dict(query)
    if not video_dict:
        await interaction.followup.send("❌ 검색 결과가 없습니다.")
        return

    videos = [{"title": title, "url": url, "duration": duration}
              for title, (url, duration) in video_dict.items()]

    embed = discord.Embed(title=f"🔎 '{query}' 검색 결과", color=discord.Color.red())
    for i, video in enumerate(videos):
        embed.add_field(
            name=f"{i+1}. {video['title']}",
            value=f"[{seconds_to_hms(video['duration'])}]({video['url']})",
            inline=False
        )

    view = YouTubeView(videos, interaction.user, volume)
    await interaction.followup.send(embed=embed, view=view)

async def stop_music(interaction: discord.Interaction):
    if not interaction.guild.voice_client:
        await interaction.response.send_message("❌ 현재 재생 중인 음악이 없어요.", ephemeral=True)
        return

    vc = interaction.guild.voice_client
    if vc.is_playing():
        vc.stop()
    await vc.disconnect()

    audio_path = f"temp_audio_{interaction.guild.id}.mp3"
    import os
    if os.path.exists(audio_path):
        os.remove(audio_path)

    await interaction.response.send_message("🛑 음악 재생을 중단하고 음성 채널에서 나갔습니다.")
