import os

import discord
from discord.ext import commands

from webserver import keep_alive

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


keep_alive()
try:
    bot.run(os.environ.get('Token'))
except discord.errors.HTTPException:
    print("\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n")
    os.system("python restarter.py")
    os.system('kill 1')
