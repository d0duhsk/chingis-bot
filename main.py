import discord
from discord.ext import commands
import random
import json
import os

TOKEN = os.getenv("TOKEN")
PREFIX = "S "
DATA_FILE = "hunnu_data.json"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ----------------
# DATA
# ----------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data():
    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)

data = load_data()

# ----------------
# START
# ----------------

@bot.command()
async def start(ctx):

    user=str(ctx.author.id)

    if user in data:
        await ctx.send("⚔ Чи аль хэдийн эхэлсэн.")
        return

    data[user]={
        "level":1,
        "exp":0,
        "gold":100,
        "army":10,
        "udam":None,
        "inventory":[]
    }

    save_data()

    await ctx.send("🐎 Чи Монголын дайчин боллоо!")

# ----------------
# PROFILE
# ----------------

@bot.command()
async def profile(ctx):

    user=str(ctx.author.id)

    if user not in data:
        await ctx.send("S start гэж бич.")
        return

    p=data[user]

    msg=f"""
👤 {ctx.author.name}

🏆 Level: {p['level']}
⚡ EXP: {p['exp']}
💰 Gold: {p['gold']}
🐎 Army: {p['army']}
🏹 Udam: {p['udam']}
"""

    await ctx.send(msg)

# ----------------
# WORK
# ----------------

@bot.command()
async def work(ctx):

    user=str(ctx.author.id)

    gold=random.randint(20,60)

    data[user]["gold"]+=gold

    save_data()

    await ctx.send(f"⛏ Чи {gold} алт оллоо")

# ----------------
# ROLL UDAM
# ----------------

udam=[
("Боржигин",1),
("Халх",15),
("Ойрад",30),
("Найман",30),
("Керейт",24)
]

@bot.command()
async def roll(ctx):

    user=str(ctx.author.id)

    r=random.randint(1,100)

    total=0

    for name,chance in udam:
        total+=chance
        if r<=total:
            data[user]["udam"]=name
            save_data()
            await ctx.send(f"🎲 Чи **{name}** удмыг авлаа")
            return

# ----------------
# BATTLE
# ----------------

@bot.command()
async def battle(ctx):

    user=str(ctx.author.id)

    win=random.choice([True,False])

    if win:
        reward=random.randint(50,150)
        data[user]["gold"]+=reward
        await ctx.send(f"⚔ Яллаа! {reward} алт")
    else:
        await ctx.send("💀 Чи ялагдлаа")

    save_data()

bot.run(TOKEN)
