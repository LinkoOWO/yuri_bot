import discord, csv, asyncio, json
from discord.ext import commands
from discord import app_commands
from discord import Embed
import mymod

with open("error.json", "r", encoding="utf-8") as jfile:
    j = json.load(jfile)

class Vocab(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="insert", description="新增單字")
    async def insert(self, interaction: discord.Interaction):
        await interaction.response.send_message("請輸入單字:", ephemeral=True)
        try:
            voc = await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == interaction.user)
            await interaction.followup.send("請輸入詞性:", ephemeral=True)
            pos = await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == interaction.user)
            await interaction.followup.send("請輸入中文意思:", ephemeral=True)
            mean = await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == interaction.user)
        except asyncio.TimeoutError:
            await interaction.followup.send("Timeout! 請重新輸入", ephemeral=True)
            return

        a = str(mymod.sqlinsert(voc.content, pos.content, mean.content))
        await interaction.followup.send(j[a], ephemeral=True)

    @app_commands.command(name="esearch", description="以英文查詢單字（開頭）")
    async def esearch(self, interaction: discord.Interaction, keyword: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            a = mymod.sqlsearchE_prefix(keyword)
            if isinstance(a, int):
                await interaction.followup.send(j.get(str(a), "未知錯誤"))
                return
            if isinstance(a, tuple):
                a = [a]
            if not a:
                await interaction.followup.send("沒有找到符合的資料")
                return
            
            pages = [a[i:i + 10] for i in range(0, len(a), 10)]
            total_pages = len(pages)
            for idx, page in enumerate(pages, start=1):
                embed = discord.Embed(title=f"🔍 英文查詢結果 ({idx}/{total_pages})", color=0x3498db)
                for entry in page:
                    embed.add_field(
                        name=f"{entry[1]} ({entry[2]})",
                        value=f"**ID**: `{entry[0]}`\n**中文意思**: {entry[3]}",
                        inline=False
                    )
                await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"錯誤: {e}")

    @app_commands.command(name="csearch", description="以中文查詢單字")
    async def csearch(self, interaction: discord.Interaction, keyword: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            a = mymod.sqlsearchC(keyword)
            if isinstance(a, int):
                await interaction.followup.send(j.get(str(a), "未知錯誤"))
                return
            if isinstance(a, tuple):
                a = [a]
            if not a:
                await interaction.followup.send("沒有找到符合的資料")
                return
            
            pages = [a[i:i + 10] for i in range(0, len(a), 10)]
            total_pages = len(pages)
            for idx, page in enumerate(pages, start=1):
                embed = discord.Embed(title=f"🔍 中文查詢結果 ({idx}/{total_pages})", color=0x3498db)
                for entry in page:
                    embed.add_field(
                        name=f"{entry[1]} ({entry[2]})",
                        value=f"**ID**: `{entry[0]}`\n**中文意思**: {entry[3]}",
                        inline=False
                    )
                await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"錯誤: {e}")

    @app_commands.command(name="quest", description="填充題測驗")
    async def quest(self, interaction: discord.Interaction, times: int):
        a = mymod.question(times)
        if not a:
            await interaction.response.send_message("目前資料庫沒有單字，請先新增", ephemeral=True)
            return

        await interaction.response.send_message("開始測驗！請依序回答下列題目：", ephemeral=True)
        for i in range(times):
            Qword = a[i][1]
            embed = Embed(
    title=f"📘 Question {i + 1}",
    description=f"請閱讀下列單字資訊：",
    color=0x3498db
)
            embed.add_field(name="單字", value=Qword, inline=False)
            embed.add_field(name="詞性 (POS)", value=a[i][2], inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)
            Aword = await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == interaction.user)
            if a[i][3] == Aword.content:
                await interaction.followup.send("正確！", ephemeral=True)
            else:
                await interaction.followup.send(f"錯誤，正確答案是：{a[i][3]}", ephemeral=True)
        await interaction.followup.send("測驗結束", ephemeral=True)

    @app_commands.command(name="recreate", description="重置資料庫（需管理員）")
    @app_commands.checks.has_permissions(administrator=True)
    async def recreate(self, interaction: discord.Interaction):
        await interaction.response.send_message("確定要重置資料嗎？(y/n)", ephemeral=True)
        check = await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == interaction.user)
        if check.content.lower() == "y":
            try:
                mymod.sqlrecreate()
                await interaction.followup.send("資料庫已重建", ephemeral=True)
            except:
                await interaction.followup.send("重建失敗", ephemeral=True)
        elif check.content.lower() == "n":
            await interaction.followup.send("操作已取消", ephemeral=True)
        else:
            await interaction.followup.send(j["6"], ephemeral=True)

    @app_commands.command(name="delete", description="刪除單字")
    async def delete(self, interaction: discord.Interaction, voc: str, pos: str):
        a = mymod.sqlsearch(voc, pos)
        if not a:
            await interaction.response.send_message("找不到該單字", ephemeral=True)
            return
        await interaction.response.send_message(f"輸入為: {a[1]}\nPOS: {a[2]}\nMean: {a[3]}\n是否刪除? (y/n)", ephemeral=True)
        check = await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == interaction.user)
        if check.content == "y":
            try:
                mymod.sqldelete(voc, pos, a[3], 1)
                await interaction.followup.send("刪除成功", ephemeral=True)
            except:
                await interaction.followup.send("刪除失敗", ephemeral=True)
        else:
            await interaction.followup.send("操作已取消", ephemeral=True)

    @app_commands.command(name="update", description="更新單字")
    async def update(self, interaction: discord.Interaction, voc: str, pos: str, new_mean: str):
        a = mymod.sqlsearch(voc, pos)
        if not a:
            await interaction.response.send_message("找不到該單字或詞性", ephemeral=True)
            return
        try:
            result = mymod.sqlupdate(voc, pos, new_mean)
            if result == 0:
                await interaction.response.send_message("更新成功", ephemeral=True)
            else:
                await interaction.response.send_message("更新失敗", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"更新錯誤: {e}", ephemeral=True)

    @app_commands.command(name="multiinsert", description="手動批量新增單字")
    async def multiinsert(self, interaction: discord.Interaction, entries: str):
        # 格式: 單字, 詞性, 中文意思;單字, 詞性, 中文意思;
        try:
            for entry in entries.split(';'):
                parts = entry.split(',')
                if len(parts) != 3:
                    await interaction.response.send_message("格式錯誤，請使用格式: 單字, 詞性, 中文意思", ephemeral=True)
                    return
                mymod.sqlinsert(*map(str.strip, parts))
            await interaction.response.send_message("批量新增成功", ephemeral=True)
        except:
            await interaction.response.send_message("發生錯誤", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Vocab(bot))