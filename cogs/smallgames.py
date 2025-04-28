import discord, random, asyncio
from discord.ext import commands
from discord import app_commands


class smallgames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="guess", description="猜數字遊戲")
    async def guess(self, interaction: discord.Interaction):
        await interaction.response.defer()
        number = random.randint(1, 100)
        await interaction.followup.send(f"🎲 我已經選擇了一個 1 到 100 的數字,有5次機會猜猜是什麼!")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        for i in range(5):
            try:
                guess = await self.bot.wait_for('message', check=check, timeout=30.0)
                guess_number = int(guess.content)

                if guess_number < number:
                    await interaction.channel.send("⬆️ 太小了！再試一次！")
                elif guess_number > number:
                    await interaction.channel.send("⬇️ 太大了！再試一次！")
                else:
                    await interaction.channel.send(f"🎉 恭喜你！你猜對了，數字是 {number}!")
                    break
            except ValueError:
                await interaction.channel.send("❌ 請輸入一個有效的數字！")
            except asyncio.TimeoutError:
                await interaction.channel.send("⏰ 時間到！遊戲結束。")
                break
        await interaction.channel.send(f"🔍 正確答案是 {number}!")


async def setup(bot):
    await bot.add_cog(smallgames(bot))
    bot.tree.copy_global_to(guild=discord.Object(id=1339772094782771353))
    await bot.tree.sync(guild=discord.Object(id=1339772094782771353))
