import discord
import uuid
import os
import asyncio
from youtube.audio import try_stream_or_download

from config import AUDIO_PATH

class CancelButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(
            label="❌ 취소",
            style=discord.ButtonStyle.danger,
            custom_id="cancel"
        )
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message(
                f"❌ 이 버튼은 **{self.user.display_name}** 님만 사용할 수 있어요!",
                ephemeral=True
            )
            return

        for item in self.view.children:
            item.disabled = True
        await interaction.message.edit(view=self.view)
        await interaction.response.send_message("🛑 선택이 취소되었습니다.", ephemeral=False)

class YouTubeView(discord.ui.View):
    def __init__(self, videos: list, interaction_user: discord.User, volume: float):
        super().__init__(timeout=60)
        self.videos = videos
        self.interaction_user = interaction_user
        self.volume = volume

        for i, video in enumerate(videos):
            self.add_item(YouTubePlayButton(i, video, interaction_user, volume))

        # ✅ 취소 버튼 추가
        self.add_item(CancelButton(interaction_user))

class YouTubePlayButton(discord.ui.Button):
    def __init__(self, index, video, user, volume: float):
        super().__init__(
            label=f"{index+1}. {video['title'][:30]}",
            style=discord.ButtonStyle.primary,
            custom_id=str(index)
        )
        self.video = video
        self.user = user
        self.volume = volume

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message(
                f"❌ 이 버튼은 **{self.user.display_name}** 님만 사용할 수 있어요!",
                ephemeral=True
            )
            return

        voice_state = interaction.user.voice
        if not voice_state or not voice_state.channel:
            await interaction.response.send_message("❌ 음성 채널에 먼저 들어가 주세요!", ephemeral=True)
            return

        for item in self.view.children:
            item.disabled = True
        await interaction.message.edit(view=self.view)

        channel = voice_state.channel
        await interaction.response.send_message(f"⏬ **{self.video['title']}** 다운로드 또는 스트리밍 중입니다...", ephemeral=False)

        guild_id = interaction.guild.id if interaction.guild else uuid.uuid4().hex
        filename = f"temp_audio_{guild_id}.mp3"
        audio_path = os.path.join(AUDIO_PATH, filename)

        # 음성 채널 접속
        vc = await channel.connect(self_deaf=True, self_mute=True)

        # 볼륨 계산 (0.0 ~ 1.0)
        volume_level = max(0.0, min(self.volume, 100.0)) / 100

        # 스트리밍 시도, 실패하면 다운로드 후 재생
        await try_stream_or_download(vc, self.video["url"], audio_path, volume_level)

        while vc.is_playing():
            await asyncio.sleep(1)

        await vc.disconnect()

        # 다운로드된 파일이면 삭제
        if os.path.exists(audio_path):
            os.remove(audio_path)