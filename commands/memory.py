import discord
from discord import app_commands
from core.database import get_connection, ensure_table

@app_commands.command(name="기억해", description="대상을 기억시킵니다")
@app_commands.describe(target="기억할 대상", content="기억할 내용")
async def 기억해(interaction: discord.Interaction, target: str, content: str):
    guild_id = interaction.guild.id
    ensure_table(guild_id)

    with get_connection() as conn:
        try:
            conn.execute(f"""
                INSERT OR REPLACE INTO memory_{guild_id} (target, content)
                VALUES (?, ?)
            """, (target, content))
            conn.commit()
            await interaction.response.send_message(f"✅ '{target}'을(를) 기억했어요.")
        except Exception as e:
            await interaction.response.send_message(f"❌ 저장 실패: {e}")

@app_commands.command(name="알려줘", description="기억해둔 내용을 알려줍니다")
@app_commands.describe(target="알고 싶은 대상")
async def 알려줘(interaction: discord.Interaction, target: str):
    guild_id = interaction.guild.id
    ensure_table(guild_id)

    with get_connection() as conn:
        cursor = conn.execute(f"""
            SELECT content FROM memory_{guild_id}
            WHERE target = ?
        """, (target,))
        row = cursor.fetchone()

    if row:
        await interaction.response.send_message(f"📌 '{target}': {row[0]}")
    else:
        await interaction.response.send_message("🤔 그런 건 기억하고 있지 않아요.")
