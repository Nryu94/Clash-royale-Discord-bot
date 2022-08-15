import discord
import os
import ssl
import certifi
import orjson
import aiohttp
from tools.set_embed import EmbedPages
from discord.ext import commands, pages

with open("config/location.json", "rb") as jf1:
    jid = orjson.loads(jf1.read())

with open("config/constants.json", "rb") as jf2:
    badge = orjson.loads(jf2.read())

ssl_context = ssl.create_default_context(cafile=certifi.where())
headers = {
    "Authorization": "Bearer {}".format(os.getenv("ClashRoyalToken"))
}


class Clan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @discord.option("location", description="部落所在地區", default="global")
    @discord.option("limit", description="搜索數量", default=10, max_value=20)
    async def get_top_clans(self, ctx, location: str, limit: int):
        """按獎杯獲取頂級部落列表"""

        if location == "global":
            PATH = "https://api.clashroyale.com/v1/locations/global/rankings/clans?limit=" + str(limit)
        else:
            PATH = "https://api.clashroyale.com/v1/locations/" + jid[location]["id"] + "/rankings/clans?limit=" + limit

        async with aiohttp.ClientSession() as session:
            async with session.get(PATH, headers=headers, ssl_context=ssl_context) as resp:
                if resp.status == 200:
                    clans = await resp.json()
                    clan = clans["items"]

                    interaction = EmbedPages(len(clan))
                    for i in range(len(clan)):
                        interaction.pages[i].add_field(name=f'***排行 {i + 1}***', value="\u200b", inline=False)
                        interaction.pages[i].add_field(name="部落名稱", value=f'**{clan[i]["name"]}**', inline=True)
                        interaction.pages[i].add_field(name="🏷部落標籤", value=f'`{clan[i]["tag"]}`', inline=True)
                        interaction.pages[i].add_field(name="👥成員數量", value=f'*{clan[i]["members"]}*', inline=True)
                        interaction.pages[i].add_field(name="🎖部落積分", value=f'*{clan[i]["clanScore"]}*', inline=True)
                        interaction.pages[i].add_field(name=f'{jid[clan[i]["location"]["name"]]["flag"]}所在地區', value=clan[i]["location"]["name"], inline=True)

                        for k in badge["alliance_badges"]:
                            if clan[i]["badgeId"] == k["id"]:
                                imgurl = "https://royaleapi.github.io/cr-api-assets/badges/{}.png".format(k["name"])
                                interaction.pages[i].set_thumbnail(url=imgurl)
                                break

                    paginator = pages.Paginator(
                        pages=interaction.pages,
                        use_default_buttons=interaction.use_default_buttons,
                        author_check=interaction.author_check,
                        custom_buttons=interaction.custom_buttons
                    )
                    await paginator.respond(ctx.interaction)
                else:
                    await ctx.respond("搜尋不到符合條件的資料", ephemeral=True)

    @commands.slash_command()
    @discord.option("location", description="部落所在地區", default="global")
    @discord.option("limit", description="搜索數量", default=10, max_value=20)
    async def get_top_clanwar_clans(self, ctx, location: str, limit: int):
        """按部落戰爭獲取頂級部落列表"""

        if location == "global":
            PATH = "https://api.clashroyale.com/v1/locations/global/rankings/clanwars?limit=" + str(limit)
        else:
            PATH = "https://api.clashroyale.com/v1/locations/" + jid[location]["id"] + "/rankings/clanwars?limit=" + limit

        async with aiohttp.ClientSession() as session:
            async with session.get(PATH, headers=headers, ssl_context=ssl_context) as resp:
                if resp.status == 200:
                    clans = await resp.json()
                    clan = clans["items"]

                    interaction = EmbedPages(len(clan))
                    for i in range(len(clan)):
                        interaction.pages[i].add_field(name=f'***排行 {i+1}***', value="\u200b", inline=False)
                        interaction.pages[i].add_field(name="部落名稱", value=f'**{clan[i]["name"]}**', inline=True)
                        interaction.pages[i].add_field(name="🏷部落標籤", value=f'`{clan[i]["tag"]}`', inline=True)
                        interaction.pages[i].add_field(name="👥成員數量", value=f'*{clan[i]["members"]}*', inline=True)
                        interaction.pages[i].add_field(name="🎖部落積分", value=f'*{clan[i]["clanScore"]}*', inline=True)
                        interaction.pages[i].add_field(name=f'{jid[clan[i]["location"]["name"]]["flag"]}所在地區', value=clan[i]["location"]["name"], inline=True)

                        for k in badge["alliance_badges"]:
                            if clan[i]["badgeId"] == k["id"]:
                                imgurl = "https://royaleapi.github.io/cr-api-assets/badges/{}.png".format(k["name"])
                                interaction.pages[i].set_thumbnail(url=imgurl)
                                break

                    paginator = pages.Paginator(
                        pages=interaction.pages,
                        use_default_buttons=interaction.use_default_buttons,
                        author_check=interaction.author_check,
                        custom_buttons=interaction.custom_buttons
                    )
                    await paginator.respond(ctx.interaction)
                else:
                    await ctx.respond("搜尋不到符合條件的資料", ephemeral=True)

    @commands.slash_command()
    @discord.option("name", description="部落名稱", required=True, min_length=3)
    @discord.option("limit", description="搜索數量", required=True, max_value=20)
    @discord.option("location", description="部落地區", default=None)
    @discord.option("minm", description="部落最小成員數量(1~50)", default=None, min_value=1, max_value=50)
    @discord.option("mins", description="部落的最低獎杯分數", default=None)
    async def search_clans(self,
                           ctx,
                           name: str,
                           limit: int,
                           location: str,
                           minm: int,
                           mins: int):
        """搜索部落"""
        args = [z for z in [location, minm, mins] if z is not None]

        if location in args:
            location = jid[location]["id"]
            if minm in args:
                if mins in args:
                    PATH = f'https://api.clashroyale.com/v1/clans?name={name}&locationId={location}&minMembers={minm}&minScore={mins}&limit={limit}'
                else:
                    PATH = f'https://api.clashroyale.com/v1/clans?name={name}&locationId={location}&minMembers={minm}&limit={limit}'
            elif mins in args:
                PATH = f'https://api.clashroyale.com/v1/clans?name={name}&locationId={location}&minScore={mins}&limit={limit}'
            else:
                PATH = f'https://api.clashroyale.com/v1/clans?name={name}&locationId={location}&limit={limit}'
        elif minm in args:
            if mins in args:
                PATH = f'https://api.clashroyale.com/v1/clans?name={name}&minMembers={minm}&minScore={mins}&limit={limit}'
            else:
                PATH = f'https://api.clashroyale.com/v1/clans?name={name}&minMembers={minm}&limit={limit}'
        elif mins in args:
            PATH = f'https://api.clashroyale.com/v1/clans?name={name}&minScore={mins}&limit={limit}'
        else:
            PATH = f'https://api.clashroyale.com/v1/clans?name={name}&limit={limit}'

        async with aiohttp.ClientSession() as session:
            async with session.get(PATH, headers=headers, ssl_context=ssl_context) as resp:
                if resp.status == 200:
                    clans = await resp.json()
                    clan = clans["items"]

                    if not clan:
                        await ctx.respond("搜索不到符合條件的部落", ephemeral=True)
                    else:
                        interaction = EmbedPages(len(clan))
                        for i in range(len(clan)):
                            interaction.search_pages[i].add_field(name="部落名稱", value=f'**{clan[i]["name"]}**', inline=False)
                            interaction.search_pages[i].add_field(name="🏷部落標籤", value=f'`{clan[i]["tag"]}`', inline=True)
                            interaction.search_pages[i].add_field(name="👥成員數量", value=f'*{clan[i]["members"]}*', inline=True)
                            interaction.search_pages[i].add_field(name=f'🏆部落戰爭獎杯', value=f'*{clan[i]["clanWarTrophies"]}*', inline=True)
                            interaction.search_pages[i].add_field(name="🎖部落積分", value=f'*{clan[i]["clanScore"]}*', inline=True)
                            interaction.search_pages[i].add_field(name=f'{jid[clan[i]["location"]["name"]]["flag"]}所在地區', value=clan[i]["location"]["name"], inline=True)

                            for k in badge["alliance_badges"]:
                                if clan[i]["badgeId"] == k["id"]:
                                    imgurl = "https://royaleapi.github.io/cr-api-assets/badges/{}.png".format(k["name"])
                                    interaction.search_pages[i].set_thumbnail(url=imgurl)
                                    break

                        paginator = pages.Paginator(
                            pages=interaction.search_pages,
                            use_default_buttons=interaction.use_default_buttons,
                            author_check=interaction.author_check,
                            custom_buttons=interaction.custom_buttons
                        )
                        await paginator.respond(ctx.interaction)
                else:
                    await ctx.respond("搜尋不到符合條件的資料", ephemeral=True)


def setup(bot):
    bot.add_cog(Clan(bot))
