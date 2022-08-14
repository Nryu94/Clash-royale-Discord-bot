import discord
import os
import io
import orjson
import aiohttp
import certifi
import ssl
from random import sample
from decimal import Decimal
from tools.synthesis import Deck
from tools.view import View
from discord.ext import commands

with open("config/emoji.json", "rb") as jf1:
    emoji = orjson.loads(jf1.read())

with open("config/constants.json", "rb") as jf2:
    constants = orjson.loads(jf2.read())

ssl_context = ssl.create_default_context(cafile=certifi.where())
headers = {
    "Authorization": "Bearer {}".format(os.getenv("ClashRoyal_Token"))
}


class Decks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="隨機生成牌組")
    async def get_deck(self, ctx):
        PATH = "https://api.clashroyale.com/v1/cards"

        async with aiohttp.ClientSession() as session:
            async with session.get(PATH, headers=headers, ssl_context=ssl_context) as resp:
                cards = await resp.json()

                await ctx.defer()
                elixir = 0
                deck = sample(cards["items"], 8)
                synthesis = Deck(*[card["iconUrls"]["medium"] for card in deck])

                view_url = "https://link.clashroyale.com/deck/cnt?deck="
                for i in deck:
                    view_url += str(i["id"]) + ";"
                    for j in constants["cards"]:
                        if i["id"] == j["id"]:
                            elixir += j["elixir"]
                            break

                try:
                    target = await synthesis()
                    file = discord.File(io.BytesIO(target), filename="image.png")
                    elixir = "{:.1f}".format(Decimal(elixir / 8))

                    embed = discord.Embed(
                        title=f'{emoji["elixir"]}{elixir}',
                        colour=discord.Colour.nitro_pink()
                    )
                    embed.set_image(url="attachment://image.png")

                    await ctx.interaction.followup.send(file=file, embed=embed, view=View(view_url))
                except:
                    await ctx.interaction.followup.send("哥布林大麻遇到前所未見的陌生人...", view=View(view_url))

def setup(bot):
    bot.add_cog(Decks(bot))