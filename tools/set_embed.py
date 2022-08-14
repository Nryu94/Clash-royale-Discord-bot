import discord
from __main__ import bot
from discord.ext import pages


class EmbedPages:
    def __init__(self, amount):
        self.pages = [self.toembed(x) for x in range(amount)]
        self.search_pages = [self.search_embed(x) for x in range(amount)]
        self.top_player_pages = [self.top_player_embed(x) for x in range(amount)]
        self.tournaments_pages = [self.tournaments_embed(x) for x in range(amount)]
        self.challenge_pages = [self.challenge_embed(x) for x in range(amount)]
        self.author_check = False
        self.use_default_buttons = False
        self.custom_buttons = [
            pages.PaginatorButton("first", emoji="⏮", style=discord.ButtonStyle.primary),
            pages.PaginatorButton("prev", emoji="◀️", style=discord.ButtonStyle.primary),
            pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),
            pages.PaginatorButton("next", emoji="▶️", style=discord.ButtonStyle.primary),
            pages.PaginatorButton("last", emoji="⏭", style=discord.ButtonStyle.primary)
        ]

    def toembed(self, arg):
        arg = discord.Embed(title="**頂級部落排行**", colour=discord.Color.brand_green())
        arg.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        return arg

    def search_embed(self, arg):
        arg = discord.Embed(colour=discord.Color.brand_green())
        arg.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        return arg

    def top_player_embed(self, arg):
        arg = discord.Embed(title="**頂級玩家排行**", colour=discord.Color.nitro_pink())
        arg.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        return arg

    def tournaments_embed(self, arg):
        arg = discord.Embed(colour=discord.Color.red())
        arg.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        return arg

    def challenge_embed(self, arg):
        arg = discord.Embed(colour=discord.Colour.blurple())
        arg.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        return arg
