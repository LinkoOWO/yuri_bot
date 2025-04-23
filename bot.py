import discord, os
from discord.ext import commands
from discord import app_commands
import json
import asyncio
import keep_alive

with open("info.json", "r", encoding="utf-8") as f:
    info = json.load(f)

intents = discord.Intents.all()

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents, application_id=info["application_id"])

    async def setup_hook(self):
        await self.load_extension("cogs.general")
        await self.load_extension("cogs.vocab")
        await self.load_extension("cogs.manager")
        await self.load_extension("cogs.showall")

        await self.tree.sync()
        print("Slash 指令已同步")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"登入成功: {bot.user}")
    print("已載入的 Cogs:")
    for cog in bot.cogs:
        print(f" - {cog}")

async def main():
    try:
        token = os.environ['token']
    except:
        try:
            token = info["token"]
        except:
            token = None
    if token is None:
        print("Error: Token not found in environment variables.")
        return
    async with bot:
        #keep_alive.keep_alive()
        await bot.start(token)

asyncio.run(main())