import discord
import os
import ssl
import aiohttp
import certifi
from googletrans import Translator
from datetime import datetime
from tools.set_embed import EmbedPages
from discord.ext import commands, pages

translator = Translator(service_urls=['translate.googleapis.com'])
ssl_context = ssl.create_default_context(cafile=certifi.where())
headers = {
    "Authorization": "Bearer {}".format(os.getenv("ClashRoyalToken"))
}
print(headers)

class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_datetime(self, timestamp: str):
        time = datetime.strptime(timestamp, "%Y%m%dT%H%M%S.%fZ")
        return time

    @commands.slash_command(description="獲取賽事信息")
    @discord.option("name", description="聯賽名稱", required=True)
    @discord.option("limit", description="搜索數量", default=10, max_value=20, min_value=1)
    async def search_tournament(self, ctx, name: str, limit: int):

        PATH = "https://api.clashroyale.com/v1/tournaments?name=" + name + "&limit=" + str(limit)

        async with aiohttp.ClientSession() as session:
            async with session.get(PATH, headers=headers, ssl_context=ssl_context) as resp:
                if resp.status == 200:
                    tournaments = await resp.json()
                    tournaments = tournaments["items"]

                    interaction = EmbedPages(len(tournaments))
                    for i in range(len(tournaments)):
                        time = await self.get_datetime(tournaments[i]["createdTime"])

                        if tournaments[i]["type"] == "open":
                            status = "__開放__"
                        else:
                            status = "__需要密碼__"

                        if "description" in tournaments[i]:
                            description = tournaments[i]["description"]
                        else:
                            description = "沒有描述"

                        interaction.tournaments_pages[i].title = f'聯賽：{tournaments[i]["name"]}'
                        interaction.tournaments_pages[i].description = f'描述：*{description}*'
                        interaction.tournaments_pages[i].add_field(name=f'創建時間：```{time}```', value="\u200b", inline=False)
                        interaction.tournaments_pages[i].add_field(name="🏷聯賽標籤", value=f'`{tournaments[i]["tag"]}`', inline=True)
                        interaction.tournaments_pages[i].add_field(name="🎫進場限制", value=status, inline=True)
                        interaction.tournaments_pages[i].add_field(name="級別上限", value=f'*{tournaments[i]["levelCap"]}*', inline=True)
                        interaction.tournaments_pages[i].add_field(name="👤目前人數", value=f'*{tournaments[i]["capacity"]}*', inline=True)
                        interaction.tournaments_pages[i].add_field(name="👥人數上限", value=f'*{tournaments[i]["maxCapacity"]}*', inline=True)

                    paginator = pages.Paginator(
                        pages=interaction.tournaments_pages,
                        use_default_buttons=interaction.use_default_buttons,
                        author_check=interaction.author_check,
                        custom_buttons=interaction.custom_buttons
                    )
                    await paginator.respond(ctx.interaction)
                else:
                    await ctx.respond("搜尋不到符合條件的資料", ephemeral=True)

    @discord.slash_command(description="查詢即將到來的挑戰活動")
    async def get_challenge(self, ctx):

        PATH = "https://api.clashroyale.com/v1/challenges"

        async with aiohttp.ClientSession() as session:
            async with session.get(PATH, headers=headers, ssl_context=ssl_context) as resp:
                challenges = await resp.json()

                interaction = EmbedPages(len(challenges))
                for i in range(len(challenges)):
                    startTime = await self.get_datetime(challenges[i]["startTime"])
                    endTime = await self.get_datetime(challenges[i]["endTime"])
                    name = translator.translate(challenges[i]["challenges"][0]["name"], dest="zh-tw").text
                    description = translator.translate(challenges[i]["challenges"][0]["description"], dest="zh-tw").text

                    interaction.challenge_pages[i].title = f'活動名稱：{name}'
                    interaction.challenge_pages[i].description = f'> 描述：*{description}*'
                    interaction.challenge_pages[i].add_field(name=f'開始時間：`{startTime}`', value="\u200b", inline=False)
                    interaction.challenge_pages[i].add_field(name=f'結束時間：`{endTime}`', value="\u200b", inline=False)
                    interaction.challenge_pages[i].set_image(url=challenges[i]["challenges"][0]["iconUrl"])

                paginator = pages.Paginator(
                    pages=interaction.challenge_pages,
                    use_default_buttons=interaction.use_default_buttons,
                    author_check=interaction.author_check,
                    custom_buttons=interaction.custom_buttons
                )
                await paginator.respond(ctx.interaction)


def setup(bot):
    bot.add_cog(Tournament(bot))
