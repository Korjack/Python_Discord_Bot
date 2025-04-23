import discord
import uuid
import os
import asyncio
from youtube.audio import download_audio

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
    def __init__(self, videos: list, interaction_user: discord.User, volume: int):
        super().__init__(timeout=60)
        self.videos = videos
        self.interaction_user = interaction_user
        self.volume = volume

        for i, video in enumerate(videos):
            self.add_item(YouTubePlayButton(i, video, interaction_user, volume))

        # ✅ 취소 버튼 추가
        self.add_item(CancelButton(interaction_user))

class YouTubePlayButton(discord.ui.Button):
    def __init__(self, index, video, user, volume: int):
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

        # ✅ 버튼들 비활성화
        for item in self.view.children:
            item.disabled = True
        await interaction.message.edit(view=self.view)

        channel = voice_state.channel

        # 🔔 다운로드 중 메시지
        await interaction.response.send_message(f"⏬ **{self.video['title']}** 다운로드 중입니다...", ephemeral=False)

        # 🔐 고유 파일명 생성
        guild_id = interaction.guild.id if interaction.guild else uuid.uuid4().hex
        audio_file = f"temp_audio_{guild_id}.mp3"

        # 🎧 다운로드
        await download_audio(self.video["url"], audio_file)

        # ✅ 다운로드 완료 메시지
        await interaction.followup.send(f"✅ **{self.video['title']}** 다운로드 완료! 음성 채널에 참가합니다.")

        # ✅ 이제 음성 채널 참가
        vc = await channel.connect()

        # 🎶 재생
        volume_level = max(0, min(self.volume, 100)) / 100
        ffmpeg_options = {
            "before_options": "-nostdin",
            "options": f'-vn -filter:a "volume={volume_level}"'
        }
        vc.play(discord.FFmpegPCMAudio(os.path.join(AUDIO_PATH, audio_file), **ffmpeg_options))

        while vc.is_playing():
            await asyncio.sleep(1)

        await vc.disconnect()

        # 🧹 임시 파일 삭제
        if os.path.exists(audio_file):
            os.remove(audio_file)