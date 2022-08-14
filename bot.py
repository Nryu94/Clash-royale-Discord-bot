import discord
import os
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot(intents=discord.Intents.all())

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    game = discord.Game("吸大麻")
    await bot.change_presence(status=discord.Status.idle, activity=game)

if __name__ == "__main__":
    bot.run(os.getenv("Bot_Token"))