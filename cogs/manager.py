import os
import discord
from discord.ext import commands
from discord import app_commands

# 權限檢查：管理員限定使用
def is_admin():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.guild_permissions.administrator
    return app_commands.check(predicate)

class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="loadcog", description="載入一個 Cog（限管理員）")
    @is_admin()
    async def load_cog(self, interaction: discord.Interaction, cog: str):
        try:
            await self.bot.load_extension(f"cogs.{cog}")
            await interaction.response.send_message(f"✅ 成功載入 cog: `{cog}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 載入失敗: {e}", ephemeral=True)

    @app_commands.command(name="unloadcog", description="卸載一個 Cog（限管理員）")
    @is_admin()
    async def unload_cog(self, interaction: discord.Interaction, cog: str):
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            await interaction.response.send_message(f"✅ 成功卸載 cog: `{cog}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 卸載失敗: {e}", ephemeral=True)

    @app_commands.command(name="reloadcog", description="重新載入一個 Cog（限管理員）")
    @is_admin()
    async def reload_cog(self, interaction: discord.Interaction, cog: str):
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await interaction.response.send_message(f"✅ 成功重新載入 cog: `{cog}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 重新載入失敗: {e}", ephemeral=True)

    @app_commands.command(name="listcog", description="列出 cogs 資料夾中的所有 .py 檔案（限管理員）")
    @is_admin()
    async def list_cogs(self, interaction: discord.Interaction):
        cog_folder = "cogs"
        cogs = [f[:-3] for f in os.listdir(cog_folder) if f.endswith(".py") and f != "__init__.py"]
        if not cogs:
            await interaction.response.send_message("⚠️ 找不到任何 Cog 檔案", ephemeral=True)
        else:
            formatted = "\n".join([f"`{c}`" for c in cogs])
            await interaction.response.send_message(f"📦 可用的 Cogs:\n{formatted}", ephemeral=True)

    @app_commands.command(name="loadedcogs", description="列出目前已載入的 Cogs（限管理員）")
    @is_admin()
    async def loaded_cogs(self, interaction: discord.Interaction):
        if self.bot.cogs:
            formatted = "\n".join([f"`{name}`" for name in self.bot.cogs])
            await interaction.response.send_message(f"✅ 目前已載入的 Cogs:\n{formatted}", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ 尚未載入任何 Cogs", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Manager(bot))