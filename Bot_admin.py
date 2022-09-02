import discord
from discord.ext import commands
import os
import time

BOT_PREFIX = '/'
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    game = discord.Game("Симулятор бана")
    await bot.change_presence(activity=game)


@bot.event
async def on_message(ctx):
    print(ctx.content)


bot.run(os.environ.get('Token'))
