import discord
from discord.ext import commands
import os
import time

string1 = 'nNНнHh'
string2 = '!Ii|иИeEеЕе́'
string3 = 'МмMm'
string4 = 'еЕэЭeEе́'
BOT_PREFIX = '/'
bot = commands.Bot(command_prefix=BOT_PREFIX)
ban_msg = ["2д", "2D", "2d", "2Д", ":two::regional_indicator_d:", "2 д", "2 D", "2 d", "2 Д", "китайские мультики", "японские мультики",
           "бурятские мультики", "Китайские мультики", "Японские мультики", "Бурятские мультики"]


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    game = discord.Game("Симулятор бана")
    await bot.change_presence(activity=game)


@bot.event
async def on_message(msg):
    pass


b_token = os.environ.get('Token')
bot.run(str(b_token))
