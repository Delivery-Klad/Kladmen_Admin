import discord
from discord.ext import commands
import os
import time

BOT_PREFIX = '/'
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=discord.Intents.default())


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    game = discord.Game("Симулятор бана")
    await bot.change_presence(activity=game)


b_token = os.environ.get('Token')
bot.run(str(b_token))
