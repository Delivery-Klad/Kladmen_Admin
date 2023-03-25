import os

import discord
from discord import app_commands
from discord.ext import commands

from webserver import keep_alive

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
log_cannel = None

alphabet = {
    "a": "\U0001F1E6",
    "b": "\U0001F1E7",
    "c": "\U0001F1E8",
    "d": "\U0001F1E9",
    "e": "\U0001F1EA",
    "f": "\U0001F1EB",
    "g": "\U0001F1EC",
    "h": "\U0001F1ED",
    "i": "\U0001F1EE",
    "j": "\U0001F1EF",
    "k": "\U0001F1F0",
    "l": "\U0001F1F1",
    "m": "\U0001F1F2",
    "n": "\U0001F1F3",
    "o": "\U0001F1F4",
    "p": "\U0001F1F5",
    "q": "\U0001F1F6",
    "r": "\U0001F1F7",
    "s": "\U0001F1F8",
    "t": "\U0001F1F9",
    "u": "\U0001F1FA",
    "v": "\U0001F1FB",
    "w": "\U0001F1FC",
    "x": "\U0001F1FD",
    "y": "\U0001F1FE",
    "z": "\U0001F1FF",
    "space": "\U000025AA"
}

alphabet_variants = {
    "a": "\U0001F170",
    "b": "\U0001F171",
    "o": "\U0001F17E",
    "p": "\U0001F17F",
    "m": "\U000024C2"
}

alphabet_addiotional = {
    "ab": "\U0001F18E",
    "cl": "\U0001F191",
    "ok": "\U0001F197",
    "sos": "\U0001F198",
    "ng": "\U0001F196",
    "vs": "\U0001F19A"
}


def preload():
    global log_cannel, role_msg_id
    log_cannel = bot.get_channel(855557026712780826)


async def log(text, type="Info"):
    if type == "Info":
        await log_cannel.send(f'**{type}:** {text}')
    else:
        await log_cannel.send(f'> **{type}:** {text}')


async def failed_use(interaction, text):
    await log_cannel.send(f'> **Error:** {interaction.user} `failed` to use command (`{text}`)')


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
