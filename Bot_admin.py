from discord.ext import commands

d = dict(string='dict', int='dictionary')
string1 = 'nNНнHh'
string2 = '!Ii|иИeEеЕе́'
string3 = 'МмMm'
string4 = 'еЕэЭeEе́'
BOT_PREFIX = '/'
bot = commands.Bot(command_prefix=BOT_PREFIX)
ban_msg = ["2д", "2D", "2d", "2Д", ":two:", "2 д", "2 D", "2 d", "2 Д", ":regional_indicator_d:"]


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")


@bot.event
async def on_message(msg):
    try:
        string = 'ф'
        string = string[:-1]
        for i in range(len(string1)):
            string = string + str(string1[i])
            for u in range(len(string2)):
                string = string + str(string2[u])
                for y in range(len(string3)):
                    string = string + str(string3[y])
                    for a in range(len(string4)):
                        string = string + str(string4[a])
                        if string in msg.content:
                            await msg.delete()
                            await msg.channel.send(f"Don't do this {msg.author.mention}")
                            print(msg.author, " ", msg.content, " DELETED!!!!")
                        string = string[:-1]
                    string = string[:-1]
                string = string[:-1]
            string = ''
        for i in ban_msg:
            if i in msg.content:
                await msg.delete()
                await msg.channel.send(f"Don't do this {msg.author.mention}")
                print(msg.author, " ", msg.content, " DELETED!!!!")
        for i in range(len(string1)):
            string = string + str(string1[i] + " ")
            for u in range(len(string2)):
                string = string + str(string2[u] + " ")
                for y in range(len(string3)):
                    string = string + str(string3[y] + " ")
                    for a in range(len(string4)):
                        string = string + str(string4[a])
                        if string in msg.content:
                            await msg.delete()
                            await msg.channel.send(f"Don't do this {msg.author.mention}")
                            print(msg.author, " ", msg.content, " DELETED!!!!")
                        string = string[:-1]
                    string = string[:-2]
                string = string[:-2]
            string = ''
    except():
        oo = 2
        print(oo)


bot.run('NjI4NjY3NDQzMzc1NjM2NTAw.XZOinQ.xg29akjTEeC0daSKfSM1bByGHjc')
