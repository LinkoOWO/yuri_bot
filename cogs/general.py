import discord
from discord.ext import commands
from discord import app_commands
import json, asyncio

with open("error.json", "r", encoding="utf-8") as jfile:
    j = json.load(jfile)

with open("info.json", "r", encoding="utf-8") as f:
    info = json.load(f)

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel_id = info["welcome"]
        channel = member.guild.get_channel(channel_id)
        if channel:
            await channel.send(f"歡迎 {member.mention} 加入伺服器！")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel_id = info["leave"]
        channel = member.guild.get_channel(channel_id)
        if channel:
            await channel.send(f"{member.mention} 離開了伺服器。")

    @app_commands.command(name="ping", description="Ping the bot")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"The ping now is {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="hello", description="Say hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello, world!")

    @app_commands.command(name="commandhelp", description="Get help for all commands")
    async def command_help(self, interaction: discord.Interaction):
        commands_list = []
        for command in self.bot.tree.walk_commands():
            if isinstance(command, app_commands.Command):
                cmd_name = command.name
                cmd_description = command.description or "沒有描述"
                cmd_params = ", ".join([f"<{param.name}>" for param in command.parameters]) if command.parameters else ""
                commands_list.append({
                    "name": cmd_name,
                    "params": cmd_params,
                    "description": cmd_description
                })

        page_size = 10
        pages = [commands_list[i:i + page_size] for i in range(0, len(commands_list), page_size)]
        total_pages = len(pages)
        current_page = 1

        await self.send_help_page(interaction, pages, current_page, total_pages)

    async def send_help_page(self, interaction, pages, current_page, total_pages):
        embed = discord.Embed(title=f"📖 指令幫助 {current_page}/{total_pages}", color=0x3498db)
        for cmd in pages[current_page - 1]:
            embed.add_field(
                name=f"/{cmd['name']} {cmd['params']}",
                value=cmd['description'],
                inline=False
            )

        view = HelpPageView(self, pages, current_page, total_pages)
        await interaction.response.send_message(embed=embed, view=view)

    async def update_help_page(self, interaction_message, pages, current_page, total_pages):
        embed = discord.Embed(title=f"📖 指令幫助 {current_page}/{total_pages}", color=0x3498db)
        for cmd in pages[current_page - 1]:
            embed.add_field(
                name=f"/{cmd['name']} {cmd['params']}",
                value=cmd['description'],
                inline=False
            )

        view = HelpPageView(self, pages, current_page, total_pages)
        await interaction_message.edit(embed=embed, view=view)

class HelpPageView(discord.ui.View):
    def __init__(self, cog, pages, current_page, total_pages):
        super().__init__(timeout=60)
        self.cog = cog
        self.pages = pages
        self.current_page = current_page
        self.total_pages = total_pages

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 1:
            self.current_page -= 1
            await self.cog.update_help_page(interaction.message, self.pages, self.current_page, self.total_pages)
            await interaction.response.defer()

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages:
            self.current_page += 1
            await self.cog.update_help_page(interaction.message, self.pages, self.current_page, self.total_pages)
            await interaction.response.defer()

async def setup(bot):
    await bot.add_cog(General(bot))
