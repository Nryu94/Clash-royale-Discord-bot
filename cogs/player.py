import discord
import os
import io
import orjson
import aiohttp
import certifi
import ssl
from tools.view import View
from tools.synthesis import Deck
from tools.set_embed import EmbedPages
from discord.ext import commands, pages

with open("config/emoji.json", "rb") as jf1:
    emoji = orjson.loads(jf1.read())

with open("config/constants.json", "rb") as jf2:
    arena = orjson.loads(jf2.read())

ssl_context = ssl.create_default_context(cafile=certifi.where())
headers = {
    "Authorization": "Bearer {}".format(os.getenv("ClashRoyalToken"))
}


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @discord.option("location", description="玩家所在地區", default="global")
    @discord.option("limit", description="搜索數量", default=10, max_value=20)
    async def get_top_players(self, ctx: discord.ApplicationContext, location: str, limit: int):
        """獲取頂級玩家列表"""

        with open("config/location.json", "rb") as jf3:
            jid = orjson.loads(jf3.read())

        if location == "global":
            PATH = "https://api.clashroyale.com/v1/locations/global/rankings/players?limit=" + str(limit)
        else:
            PATH = "https://api.clashroyale.com/v1/locations/" + jid[location]["id"] + "/rankings/players?limit=" + limit

        async with aiohttp.ClientSession() as session:
            async with session.get(PATH, headers=headers, ssl_context=ssl_context) as resp:
                if resp.status == 200:
                    players = await resp.json()
                    player = players["items"]

                    interaction = EmbedPages(len(player))
                    for i in range(len(player)):
                        if "clan" not in player[i]:
                            clan_name = "沒有部落"
                        else:
                            clan_name = player[i]["clan"]["name"]

                        interaction.top_player_pages[i].add_field(name=f'***排行 {i+1}***', value="\u200b", inline=False)
                        interaction.top_player_pages[i].add_field(name="玩家名稱", value=f'**{player[i]["name"]}**', inline=True)
                        interaction.top_player_pages[i].add_field(name="🏷玩家標籤", value=f'`{player[i]["tag"]}`', inline=True)
                        interaction.top_player_pages[i].add_field(name=f'{emoji["expLevel"]}經驗等級', value=f'*{player[i]["expLevel"]}*', inline=True)
                        interaction.top_player_pages[i].add_field(name="🏆玩家獎杯", value=f'*{player[i]["trophies"]}*', inline=True)
                        interaction.top_player_pages[i].add_field(name=f'{emoji["clan"]}玩家部落', value=f'**{clan_name}**', inline=True)

                        for k in arena["arenas"]:
                            if player[i]["arena"]["id"] == k["id"]:
                                imgurl = "https://royaleapi.github.io/cr-api-assets/arenas/arena{}.png".format(k["arena_id"])
                                interaction.top_player_pages[i].set_thumbnail(url=imgurl)
                                break

                    paginator = pages.Paginator(
                        pages=interaction.top_player_pages,
                        use_default_buttons=interaction.use_default_buttons,
                        author_check=interaction.author_check,
                        custom_buttons=interaction.custom_buttons
                    )
                    await paginator.respond(ctx.interaction)
                else:
                    await ctx.respond("搜尋不到符合條件的資料", ephemeral=True)

    @commands.slash_command()
    @discord.option("tag", description="玩家標籤", required=True, min_length=3)
    async def get_player(self, ctx, tag: str):
        """獲取玩家相關信息"""

        PATH = "https://api.clashroyale.com/v1/players/%23" + tag[1:] + "/upcomingchests"

        async with aiohttp.ClientSession() as session:
            async with session.get(PATH, headers=headers, ssl_context=ssl_context) as resp:
                if resp.status == 200:
                    chests = await resp.json()
                    chests = chests["items"]

                    string = ''.join(str(x) for x in [f'{emoji[chest["name"]]}+{chest["index"]}' for chest in chests])
                    PATH = "https://api.clashroyale.com/v1/players/%23" + tag[1:]

                    async with session.get(PATH, headers=headers, ssl_context=ssl_context) as resp2:
                        try:
                            player = await resp2.json()

                            await ctx.defer()

                            view_url = "https://link.clashroyale.com/deck/cnt?deck="
                            synthesis = Deck(*[card["iconUrls"]["medium"] for card in player["currentDeck"]])
                            target = await synthesis()

                            for z in player["currentDeck"]:
                                view_url += str(z["id"]) + ";"

                            if "clan" not in player:
                                clan_name = "沒有部落"
                            else:
                                clan_name = player["clan"]["name"]

                            embed = discord.Embed(colour=discord.Colour.gold(), description=f'> {string}', title="即將到來的寶箱")
                            embed.add_field(name="玩家名稱", value=f'**{player["name"]}**', inline=True)
                            embed.add_field(name=f'{emoji["clan"]}玩家部落', value=f'**{clan_name}**', inline=True)
                            embed.add_field(name=f'{emoji["expLevel"]}經驗等級', value=f'*{player["expLevel"]}*', inline=True)
                            embed.add_field(name="🏆玩家獎杯", value=f'*{player["trophies"]}*', inline=True)
                            embed.add_field(name=f'{emoji["trophy"]}最高獎杯', value=f'*{player["bestTrophies"]}*', inline=True)
                            embed.add_field(name=f'{emoji["threeCrownWins"]}三冠勝', value=f'*{player["threeCrownWins"]}*', inline=True)
                            embed.add_field(name=f'{emoji["battle"]}總對戰數', value=f'*{player["battleCount"]}*', inline=True)
                            embed.add_field(name=f'{emoji["wins"]}勝場', value=f'*{player["wins"]}*', inline=True)
                            embed.add_field(name=f'{emoji["losses"]}輸場', value=f'*{player["losses"]}*', inline=True)
                            embed.set_footer(text=f'來自{ctx.author}的請求', icon_url=ctx.author.avatar)

                            for k in arena["arenas"]:
                                if player["arena"]["id"] == k["id"]:
                                    imgurl = "https://royaleapi.github.io/cr-api-assets/arenas/arena{}.png".format(k["arena_id"])
                                    embed.set_thumbnail(url=imgurl)
                                    break

                            file = discord.File(io.BytesIO(target), filename="image.png")
                            embed.set_image(url="attachment://image.png")

                            await ctx.interaction.followup.send(file=file, embed=embed, view=View(view_url))
                        except IndexError:
                            await ctx.respond("標籤輸入錯誤！", ephemeral=True)
                else:
                    await ctx.respond("搜尋不到符合條件的資料", ephemeral=True)


def setup(bot):
    bot.add_cog(Player(bot))
