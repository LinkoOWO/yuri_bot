import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

conn = sqlite3.connect("vocabulary.db")
cursor = conn.cursor()

class WordShow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="showall", description="顯示所有單字或特定詞性單字")
    @app_commands.describe(pos="要查詢的詞性（可選）")
    async def show_all(self, interaction: discord.Interaction, pos: str = None):
        await interaction.response.defer()  # 延遲回應以避免超時

        if pos:
            cursor.execute("SELECT * FROM words WHERE pos = ?", (pos,))
        else:
            cursor.execute("SELECT * FROM words")
        words = cursor.fetchall()

        if not words:
            await interaction.followup.send(f"❌ 沒有找到詞性為 `{pos}` 的單字", ephemeral=True)
            return

        header = f"{'ID':<8} | {'單字':<20} | {'詞性':<4} | 中文意思"
        lines = [header, "-" * 50]

        for word in words:
            line = f"{word[0]:<4} | {word[1]:<15} | {word[2]:<4} | {word[3]}"
            lines.append(line)

        result = "\n".join(lines)

        chunks = [result[i:i+4000] for i in range(0, len(result), 4000)]
        for chunk in chunks:
            embed = discord.Embed(
                title=f"📚 詞性為 {pos if pos else '全部'} 的單字列表",
                description=f"```\n{chunk}\n```",
                color=0x55acee
            )
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="number", description="顯示資料庫中的單字數量")
    async def number(self, interaction: discord.Interaction):
        cursor.execute("SELECT COUNT(*) FROM words")
        count = cursor.fetchone()[0]
        await interaction.response.send_message(f"📊 目前資料庫中有{count}個單字", ephemeral=True)

async def setup(bot):
    await bot.add_cog(WordShow(bot))