import os
import requests
import json

import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get

from webserver import keep_alive
from files.data import alphabet, alphabet_variants, alphabet_addiotional, ban_tags, stop_tags, roles

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
log_cannel, role_msg_id = None, None


def preload():
    global log_cannel, role_msg_id
    log_cannel = bot.get_channel(855557026712780826)
    role_msg_id = 938723422773592134


async def log(text, type="Info"):
    if type == "Info":
        await log_cannel.send(f'**{type}:** {text}')
    else:
        await log_cannel.send(f'> **{type}:** {text}')


def transform(msg):
    if len(msg.split(" ")) > 2:
        return False
    if " " in msg:
        msg = msg.replace(" ", f",{alphabet['space']},")
    for key in alphabet_addiotional:
        if key in msg:
            msg = msg.replace(key, f",{alphabet_addiotional[key]},")
    result = []
    duplicates = []
    for word in msg.split(","):
        temp = word.encode()
        if (240 in temp and 159 in temp) or (226 in temp and 150 in temp):
            try:
                result.index(word)
                return None
            except ValueError:
                result.append(word)
            continue
        for letter in word:
            try:
                result.index(alphabet[letter])
                if letter in alphabet_variants.keys():
                    if letter in duplicates:
                        return None
                    result.append(alphabet_variants[letter])
                    duplicates.append(letter)
                else:
                    return None
            except ValueError:
                result.append(alphabet[letter])
    return result


async def get_message(interaction: discord.Interaction, msg_id: str):
    try:
        return await interaction.channel.fetch_message(int(msg_id))
    except ValueError:
        await interaction.response.send_message("Может ты даун раз не можешь нормально айдишник указать?", ephemeral=False)
        await log(f"{interaction.user} `failed` to use command (`Wrong message id`)", "Error")
        return None
    except discord.errors.NotFound:
        await interaction.response.send_message("Сообщение не найдено", ephemeral=True)
        await log(f"{interaction.user} `failed` to use command (`Message not found`)", "Error")
        return None
    except Exception as e:
        await interaction.response.send_message(f"Что-то пошло не так ({type(e)})", ephemeral=True)
        await log(f"{interaction.user} `failed` to use command (`Unknown error`)", "Error")
        return None


def detect_text(url):
    words = []
    img_data = b""
    for chunk in requests.get(url, stream=True):
        img_data += chunk
    headers = {"X-Api-Key": os.environ.get("recog_key")}
    result = requests.post("https://api.api-ninjas.com/v1/imagetotext", files={'image': img_data}, headers=headers)
    for i in result.json():
        words.append(i["text"].lower())
    return words


@bot.event
async def on_ready():
    preload()
    print("Logged in as: " + bot.user.name + "\n")
    game = discord.Game("Симулятор бана")
    await bot.change_presence(activity=game)
    try:
        synced = await bot.tree.sync()
        await log(f"Logged in as: `{bot.user.name}` (Synced `{len(synced)}` commands)")
    except Exception as e:
        await log(f"Logged in as: `{bot.user.name}`")


@bot.tree.command(name="help", description = "Bot command description")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Bot help", colour=discord.Colour.red())
    embed.add_field(name="/daun `message_id`", value=f"Add {alphabet['d']} {alphabet['a']} {alphabet['u']} {alphabet['n']} emojies to message", inline=False)
    embed.add_field(name="/reation `text` `message_id`", value="Add emojies from your text to message", inline=False)
    embed.add_field(name="To get message id", value="Настройки -> Расширенные -> Режим разработчика")
    await interaction.response.send_message(embed=embed, ephemeral=False)
    await log(f'{interaction.user} used `/help` in channel `{interaction.channel}`')


@bot.tree.command(name="daun", description = "Add D A U N emojies to message")
@app_commands.describe(msg_id="message id")
async def daun(interaction: discord.Interaction, msg_id: str):
    msg = await get_message(interaction, msg_id)
    if msg is None:
        return
    await msg.add_reaction(alphabet['d'])
    await msg.add_reaction(alphabet['a'])
    await msg.add_reaction(alphabet['u'])
    await msg.add_reaction(alphabet['n'])
    await interaction.response.send_message("Ок", ephemeral=True)
    await log(f'{interaction.user} used `/daun` on message: `{msg_id}`')


@bot.tree.command(name="reaction", description = "Add emojies from your text to message")
@app_commands.describe(text="reaction text", msg_id="message id")
async def reaction(interaction: discord.Interaction, text: str, msg_id: str):
    text = text.lower()
    if len(text) > 35:
        await interaction.response.send_message("Слишком длинный текст", ephemeral=True)
        await log(f'{interaction.user} failed to use `/reaction` with text: `{text}` (`Too long text`)', "Error")
        return
    for i in text:
        if 122 < ord(i) > 97 and ord(i) != 32:
            await interaction.response.send_message("Русский текст? Пиздец ты баобаб конечно", ephemeral=False)
            await log(f'{interaction.user} failed to use `/reaction` with text: `{text}` (`Russian letters`)', "Error")
            return
        elif ord(i) in [44, 46, 33, 63, 45, 95]:
            await interaction.response.send_message("Знаки препинания? я звоню в дурку", ephemeral=False)
            await log(f'{interaction.user} failed to use `/reaction` with text: `{text}` `(Punctuation marks`)', "Error")
            return
    msg = await get_message(interaction, msg_id)
    if msg is None:
        return
    await interaction.response.defer(ephemeral=True)
    reactions = transform(text)
    if reactions is None:
        await interaction.followup.send("Каждый символ должен повторяться не более 1 раза (a, b, o, p, m - 2 раза)", ephemeral=True)
        return
    elif not reactions:
        await interaction.followup.send("Максимальная длина - 2 слова", ephemeral=True)
        return
    elif len(reactions) > 20:
        await interaction.followup.send("Максимальное количество emoji - 20", ephemeral=True)
        return
    for i in reactions:
        await msg.add_reaction(i)
    await interaction.followup.send("Ок", ephemeral=True)
    await log(f'{interaction.user} used `/reaction` with text: `{text}` on message: `{msg_id}`')


@bot.tree.command(name="approve", description = "Set approved role for user")
@app_commands.describe(user="User mention")
async def approve_user(interaction: discord.Interaction, user: str):
    if interaction.channel.name != "без-роли":
        await interaction.response.send_message("Команда недоступна в этом чате", ephemeral=True)
        return
    await log(f'{interaction.user} used `/approve` on user: `{user}`')
    try:
        _member = get(bot.get_all_members(), id=int(user[2:-1]))
    except ValueError:
        await interaction.response.send_message("Пользователь не найден", ephemeral=True)
        return
    if _member is None:
        await interaction.response.send_message("Пользователь не найден", ephemeral=True)
        return
    if get(interaction.user.roles, name="approver"):
        role = discord.utils.get(_member.guild.roles, name='DJ')
        await _member.add_roles(role)
        await interaction.response.send_message("Роль выдана", ephemeral=False)
    else:
        await interaction.response.send_message("Это так не работает", ephemeral=False)


@bot.event
async def on_message(ctx: discord.message.Message):
    return
    try:
        for att in ctx.attachments:
            print(att)
            response = requests.get(
                f'https://api.imagga.com/v2/tags?image_url={att}',
                auth=(os.environ.get('img_key'), os.environ.get('img_pass')), timeout=15
            )
            print(response.status_code)
            print(response.text)
            output = json.loads(response.text)
            all_tags = []
            tags_counter, tags_counter2 = 0, 0
            result_tags = []
            permitted_tags = []
            
            for i in output["result"]["tags"]:
                all_tags.append(i["tag"]["en"])
            for i in ban_tags:
                if i in all_tags:
                    tags_counter += 1
                    result_tags.append(i)
            for i in stop_tags:
                if i in all_tags:
                    tags_counter2 += 1
                    permitted_tags.append(i)
            in_url = "anime" in str(att)
            result = True if (tags_counter > 7 and tags_counter2 < 2) or (in_url and tags_counter > 2) else False
            result_tags.sort()
            permitted_tags.sort()
            all_tags.sort()
            
            text_recognition = detect_text(att)
            recognition_result = "anime" in text_recognition or "аниме" in text_recognition
            await log(f"Attachment: {att}\n"
                      f"**Imagga**\n**`Triggered tags ({tags_counter}):`** {result_tags}\n"
                      f"**`Permitted tags ({tags_counter2}):`** {permitted_tags}\n"
                      f"**`'anime' in image url:`** {in_url}\n"
                      f"**`Anime image detected:`** {result}\n"
                      f"**`All image tags:`** {all_tags}\n"
                      f"**Text recognition**\n"
                      f"**`Text on image:`** {text_recognition}\n"
                      f"**`Anime detected:`** {recognition_result}\n"
                      f"**`Summary:`** Anime detected {recognition_result or in_url or result}")
    except Exception as e:
        await log("Error in image tagging\n\n" + str(e))

        
@bot.event
async def on_raw_reaction_add(ctx):
    if ctx.message_id == role_msg_id:
        _member = ctx.member
        role = discord.utils.get(_member.guild.roles, name=roles[ctx.emoji.name])
        await _member.add_roles(role)
        await log(f"`'{_member}'` выбрал роль `'{role}'`")


@bot.event
async def on_raw_reaction_remove(ctx):
    if ctx.message_id == role_msg_id:
        _member = get(bot.get_all_members(), id=ctx.user_id)
        role = discord.utils.get(_member.guild.roles, name=roles[ctx.emoji.name])
        await _member.remove_roles(role)
        await log(f"`'{_member}'` убрал роль `'{role}'`")


keep_alive()
try:
    bot.run(os.environ.get('token'))
except discord.errors.HTTPException:
    print("\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n")
    os.system("python restarter.py")
    os.system('kill 1')
