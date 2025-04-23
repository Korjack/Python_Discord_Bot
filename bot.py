import discord
from discord import app_commands

from core.client import BotClient
from commands.youtube import run_youtube_command, stop_music
from commands.memory import 기억해, 알려줘

from config import BOT_TOKEN, DEFAULT_VOLUME

client = BotClient()

@client.event
async def on_voice_state_update(member, before, after):
    voice_client = discord.utils.get(client.voice_clients, guild=member.guild)

    if voice_client and voice_client.channel:
        if len(voice_client.channel.members) == 1:  # 봇만 남았다면
            guild_name = voice_client.guild.name
            channel_name = voice_client.channel.name
            await voice_client.disconnect()
            print(f"[{guild_name}] 서버의 음성채널 '{channel_name}'에서 유저가 없어 연결을 종료했습니다.")


@client.tree.command(name="youtube", description="YouTube 영상 검색")
@app_commands.describe(query="검색어", volume=f"음량 (0.0 ~ 100.0) / 기본값 {DEFAULT_VOLUME}")
async def youtube(interaction: discord.Interaction, query: str, volume: float = DEFAULT_VOLUME):
    await run_youtube_command(interaction, query, volume)

@client.tree.command(name="재생", description="YouTube 영상 검색")
@app_commands.describe(query="검색어", volume=f"음량 (0.0 ~ 100.0) / 기본값 {DEFAULT_VOLUME}")
async def youtube(interaction: discord.Interaction, query: str, volume: float = DEFAULT_VOLUME):
    await run_youtube_command(interaction, query, volume)

@client.tree.command(name="stop", description="현재 재생 중인 음악을 중단합니다.")
async def stop(interaction: discord.Interaction):
    await stop_music(interaction)

@client.tree.command(name="그만", description="현재 재생 중인 음악을 중단합니다.")
async def 그만(interaction: discord.Interaction):
    await stop_music(interaction)

client.tree.add_command(기억해)
client.tree.add_command(알려줘)

client.run(BOT_TOKEN)
