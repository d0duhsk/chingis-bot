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
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

data = load_data()

def check_user(user_id):
    return str(user_id) in data

# ----------------
# READY
# ----------------

@bot.event
async def on_ready():
    print(f"{bot.user} online боллоо!")

# ----------------
# START
# ----------------

@bot.command()
async def start(ctx):
    user = str(ctx.author.id)

    if user in data:
        await ctx.send("⚔ Чи аль хэдийн эхэлсэн байна.")
        return

    data[user] = {
        "level": 1,
        "exp": 0,
        "gold": 100,
        "army": 10,
        "udam": None,
        "inventory": []
    }

    save_data()
    await ctx.send("🐎 Чи Монголын дайчин боллоо!")

# ----------------
# PROFILE
# ----------------

@bot.command()
async def profile(ctx):
    user = str(ctx.author.id)

    if user not in data:
        await ctx.send("Эхлээд `S start` гэж бич.")
        return

    p = data[user]

    msg = f"""
👤 {ctx.author.name}

🏆 Level: {p['level']}
⚡ EXP: {p['exp']}
💰 Gold: {p['gold']}
🐎 Army: {p['army']}
🏹 Udam: {p['udam']}
🎒 Inventory: {len(p['inventory'])} item
"""
    await ctx.send(msg)

# ----------------
# WORK
# ----------------

@bot.command()
async def work(ctx):
    user = str(ctx.author.id)

    if user not in data:
        await ctx.send("Эхлээд `S start` гэж бич.")
        return

    gold = random.randint(20, 60)
    data[user]["gold"] += gold
    data[user]["exp"] += 10

    save_data()
    await ctx.send(f"⛏ Чи {gold} алт олж, 10 exp авлаа!")

# ----------------
# ROLL UDAM
# ----------------

udam = [
    ("Боржигин", 1),
    ("Халх", 15),
    ("Ойрад", 30),
    ("Найман", 30),
    ("Керейт", 24)
]

@bot.command()
async def roll(ctx):
    user = str(ctx.author.id)

    if user not in data:
        await ctx.send("Эхлээд `S start` гэж бич.")
        return

    r = random.randint(1, 100)
    total = 0

    for name, chance in udam:
        total += chance
        if r <= total:
            data[user]["udam"] = name
            save_data()
            await ctx.send(f"🎲 Чи **{name}** удмыг авлаа!")
            return

# ----------------
# BATTLE
# ----------------

@bot.command()
async def battle(ctx):
    user = str(ctx.author.id)

    if user not in data:
        await ctx.send("Эхлээд `S start` гэж бич.")
        return

    win = random.choice([True, False])

    if win:
        reward = random.randint(50, 150)
        data[user]["gold"] += reward
        data[user]["exp"] += 20
        await ctx.send(f"⚔ Чи яллаа! {reward} алт, 20 exp авлаа!")
    else:
        await ctx.send("💀 Чи ялагдлаа!")

    save_data()

bot.run(TOKEN)
