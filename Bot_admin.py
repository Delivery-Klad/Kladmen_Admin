import os

import discord
from discord import app_commands
from discord.ext import commands

from webserver import keep_alive

log_cannel_id = 855557026712780826
BOT_PREFIX = '!'
bot = commands.Bot(command_prefix=BOT_PREFIX,
                   intents=discord.Intents.all())


def channel():
    return bot.get_channel(log_cannel_id)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    game = discord.Game("Симулятор бана")
    await bot.change_presence(activity=game)
    try:
        synced = await bot.tree.sync()
        await channel().send(f"Logged in as: {bot.user.name}\nSynced {len(synced)} commands")
    except Exception as e:
        await channel().send(f"Logged in as: {bot.user.name}")


@bot.tree.command(name="test")
@app_commands.describe(test="test")
async def test(interaction: discord.Interaction, test: str):
    await interaction.response.send_message("test")


keep_alive()
try:
    bot.run(os.environ.get('Token'))
except discord.errors.HTTPException:
    print("\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n")
    os.system("python restarter.py")
    os.system('kill 1')
