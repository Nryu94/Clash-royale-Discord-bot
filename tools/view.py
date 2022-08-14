import discord
from discord.ui import Button


class View(discord.ui.View):
    def __init__(self, url):
        super().__init__(timeout=None)
        self.add_item(Button(label="複製牌組", url=url))
        self.add_item(Button(label="推薦網站(純推薦)", url="https://royaleapi.com"))


