import discord
from discord import app_commands

from core.client import BotClient
from commands.youtube import run_youtube_command, stop_music
from commands.memory import 기억해, 알려줘

from config import BOT_TOKEN, DEFAULT_VOLUME

client = BotClient()

@client.tree.command(name="youtube", description="YouTube 영상 검색")
@app_commands.describe(query="검색어", volume="음량 (0~100) / 기본값 2")
async def youtube(interaction: discord.Interaction, query: str, volume: int = DEFAULT_VOLUME):
    await run_youtube_command(interaction, query, volume)

@client.tree.command(name="재생", description="YouTube 영상 검색")
@app_commands.describe(query="검색어", volume="음량 (0~100) / 기본값 2")
async def youtube(interaction: discord.Interaction, query: str, volume: int = DEFAULT_VOLUME):
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
