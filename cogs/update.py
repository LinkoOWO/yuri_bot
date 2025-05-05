import discord
from discord.ext import commands
from discord import app_commands

channel = 1367155531449372673

class UpdateDB(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="updatedb", description="手動上傳 vocabulary.db 到指定頻道")
    async def updatedb(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        target_channel = self.bot.get_channel(channel)
        if target_channel:
            try:
                await target_channel.send("手動上傳 vocabulary.db:", file=discord.File("vocabulary.db"))
                await interaction.followup.send("已成功上傳至指定頻道", ephemeral=True)
            except Exception as e:
                await interaction.followup.send(f"上傳失敗: {e}", ephemeral=True)
        else:
            await interaction.followup.send("找不到指定頻道", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(UpdateDB(bot))