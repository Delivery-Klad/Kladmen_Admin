import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import *

BOT_PREFIX = '/'

Bot = commands.Bot(command_prefix=BOT_PREFIX)

ban_msg = ["anime", "аниме", "Anime", "Аниме", "а н и м е", "А н и м е", "АнИМе", "А Н И М Е", "АНиме", "aниме", "Aнимe", "Aniме", "ониме", "ниме", "нимэ"]


@Bot.event
async def on_ready():
    print("Logged in as: " + Bot.user.name + "\n")


@Bot.command(pass_context=True)
async def hello(ctx):
    await Bot.say("Алех лох")


@Bot.event
async def on_message(msg):
    try:
        for i in ban_msg:
            if i in msg.content:
                await msg.delete()
                #channel = msg.channel
                #await channel.send('Алех лох')
    except():
        oo = 2


Bot.run('NjI4NjY3NDQzMzc1NjM2NTAw.XZOinQ.xg29akjTEeC0daSKfSM1bByGHjc')