import discord
from discord.ext import commands
import os
import json
import random
import asyncio
from datetime import datetime, timedelta

# =========================
# CONFIG
# =========================
TOKEN = "END_DISCORD_BOT_TOKEN"   # <-- Энд өөрийн bot token-оо тавь
PREFIX = "S "
DATA_FILE = "hunnu_data.json"
MAX_LEVEL = 200

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# =========================
# RANK SYSTEM
# level, rank_name, work_salary_base, image_url
# =========================
RANKS = [
    (200, "☀️ Их Эзэн Хаан", 5000, "https://images.unsplash.com/photo-1518562180175-34a163b1a9a6?q=80&w=1200&auto=format&fit=crop"),
    (196, "👑 Их Хаан", 4600, "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop"),
    (192, "🦅 9 Өрлөгийн Нэг", 4300, "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop"),
    (188, "🐺 4 Нохосын Нэг", 4100, "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200&auto=format&fit=crop"),
    (184, "⚖ Шихихутаг", 3900, "https://images.unsplash.com/photo-1493246318656-5bfd4cfb29b8?q=80&w=1200&auto=format&fit=crop"),
    (180, "📜 Тата Тунга", 3700, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=1200&auto=format&fit=crop"),
    (176, "🥣 Хааны Их Буурч", 3500, "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?q=80&w=1200&auto=format&fit=crop"),
    (170, "🏛 Их Сайд", 3300, "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?q=80&w=1200&auto=format&fit=crop"),
    (164, "🛡 Шадар Сайд", 3100, "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1200&auto=format&fit=crop"),
    (158, "⚖ Төрийн Сайд", 2900, "https://images.unsplash.com/photo-1519074069444-1ba4fff66d16?q=80&w=1200&auto=format&fit=crop"),
    (152, "🏯 Дээд Түшмэл", 2700, "https://images.unsplash.com/photo-1500534623283-312aade485b7?q=80&w=1200&auto=format&fit=crop"),
    (146, "📜 Их Түшмэл", 2500, "https://images.unsplash.com/photo-1464219222984-216ebffaaf85?q=80&w=1200&auto=format&fit=crop"),
    (140, "🛡 Ахлах Түшмэл", 2300, "https://images.unsplash.com/photo-1508672019048-805c876b67e2?q=80&w=1200&auto=format&fit=crop"),
    (134, "🏹 Түшмэл", 2100, "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1200&auto=format&fit=crop"),
    (128, "🐎 Түмтийн Ноён", 1900, "https://images.unsplash.com/photo-1517022812141-23620dba5c23?q=80&w=1200&auto=format&fit=crop"),
    (122, "⚔ Түмтийн Ахлагч", 1800, "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200&auto=format&fit=crop"),
    (116, "🛡 Түмт", 1700, "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=80&w=1200&auto=format&fit=crop"),
    (110, "🐺 Мянганы Ноён", 1600, "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1200&auto=format&fit=crop"),
    (104, "🐎 Мянгат", 1500, "https://images.unsplash.com/photo-1511497584788-876760111969?q=80&w=1200&auto=format&fit=crop"),
    (98, "⚔ Мянганы Ахлагч", 1400, "https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=1200&auto=format&fit=crop"),
    (92, "🛡 Зууны Ноён", 1300, "https://images.unsplash.com/photo-1500048993953-d23a436266cf?q=80&w=1200&auto=format&fit=crop"),
    (86, "🏇 Зуут", 1200, "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=1200&auto=format&fit=crop"),
    (80, "⚔ Зууны Ахлагч", 1100, "https://images.unsplash.com/photo-1500534314209-a26db0f5b2af?q=80&w=1200&auto=format&fit=crop"),
    (74, "🪖 Аравтын Ноён", 1000, "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?q=80&w=1200&auto=format&fit=crop"),
    (68, "⚔ Аравтын Ахлагч", 900, "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop"),
    (62, "🛡 Хишигтэн", 800, "https://images.unsplash.com/photo-1502082553048-f009c37129b9?q=80&w=1200&auto=format&fit=crop"),
    (56, "🥣 Буурч", 700, "https://images.unsplash.com/photo-1511300636408-a63a89df3482?q=80&w=1200&auto=format&fit=crop"),
    (50, "🩺 Эмч", 620, "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?q=80&w=1200&auto=format&fit=crop"),
    (44, "🔥 Түлээчин", 560, "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=80&w=1200&auto=format&fit=crop"),
    (38, "🔨 Дархан", 500, "https://images.unsplash.com/photo-1511818966892-d7d671e672a2?q=80&w=1200&auto=format&fit=crop"),
    (32, "📯 Элч", 450, "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop"),
    (26, "🏹 Анчин", 400, "https://images.unsplash.com/photo-1500534623283-312aade485b7?q=80&w=1200&auto=format&fit=crop"),
    (20, "🐑 Малчин", 350, "https://images.unsplash.com/photo-1504593811423-6dd665756598?q=80&w=1200&auto=format&fit=crop"),
    (14, "🌾 Тариачин", 300, "https://images.unsplash.com/photo-1464226184884-fa280b87c399?q=80&w=1200&auto=format&fit=crop"),
    (8, "👤 Цэрэг", 230, "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1200&auto=format&fit=crop"),
    (0, "🌱 Шинэ Хүн", 150, "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop"),
]

# =========================
# DATA
# =========================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

data = load_data()

def default_user():
    return {
        "money": 0,
        "bank": 0,
        "level": 1,
        "exp": 0,
        "messages": 0,
        "last_work": None,
        "last_daily": None
    }

def get_user(user_id: int):
    uid = str(user_id)
    if uid not in data:
        data[uid] = default_user()
        save_data(data)
    return data[uid]

# =========================
# RANK / LEVEL
# =========================
def get_rank_data(level: int):
    for req_level, name, salary, image in RANKS:
        if level >= req_level:
            return {
                "level_req": req_level,
                "name": name,
                "salary": salary,
                "image": image
            }
    return {
        "level_req": 0,
        "name": "🌱 Шинэ Хүн",
        "salary": 150,
        "image": ""
    }

def exp_needed(level: int):
    return 100 + (level * 25)

def add_exp(user, amount: int):
    if user["level"] >= MAX_LEVEL:
        user["exp"] = 0
        return False

    user["exp"] += amount
    leveled_up = False

    while user["level"] < MAX_LEVEL and user["exp"] >= exp_needed(user["level"]):
        user["exp"] -= exp_needed(user["level"])
        user["level"] += 1
        leveled_up = True

    if user["level"] >= MAX_LEVEL:
        user["level"] = MAX_LEVEL
        user["exp"] = 0

    return leveled_up

# =========================
# TIME HELPERS
# =========================
def now_str():
    return datetime.utcnow().isoformat()

def parse_time(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts)
    except:
        return None

# =========================
# EVENTS
# =========================
@bot.event
async def on_ready():
    print(f"{bot.user} online боллоо!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user = get_user(message.author.id)
    user["messages"] += 1

    # chat бүрээс exp авна
    gained = random.randint(2, 5)
    old_level = user["level"]
    leveled = add_exp(user, gained)
    save_data(data)

    if leveled:
        rank = get_rank_data(user["level"])
        embed = discord.Embed(
            title="🎉 Level Up!",
            description=(
                f"{message.author.mention} **{old_level} → {user['level']}** level хүрлээ!\n"
                f"👑 Шинэ цол: **{rank['name']}**"
            ),
            color=0xD4AF37
        )
        embed.set_image(url=rank["image"])
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

# =========================
# COMMANDS
# =========================
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📜 Chingis Bot Command List",
        description=f"Prefix: `{PREFIX}`",
        color=0xC9A33A
    )
    embed.add_field(
        name="Үндсэн",
        value=(
            f"`{PREFIX}profile` - Профайл\n"
            f"`{PREFIX}rank` - Одоогийн цол\n"
            f"`{PREFIX}balance` - Мөнгө\n"
            f"`{PREFIX}work` - Ажил хийж мөнгө олох\n"
            f"`{PREFIX}daily` - Өдрийн шагнал\n"
            f"`{PREFIX}deposit <дүн>` - Банканд хийх\n"
            f"`{PREFIX}withdraw <дүн>` - Банкнаас авах\n"
            f"`{PREFIX}leaderboard` - Хамгийн өндөр level"
        ),
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command()
async def profile(ctx, member: discord.Member = None):
    member = member or ctx.author
    user = get_user(member.id)
    rank = get_rank_data(user["level"])

    current_exp = user["exp"]
    needed = exp_needed(user["level"]) if user["level"] < MAX_LEVEL else 0

    embed = discord.Embed(
        title=f"👤 {member.display_name}-ийн Profile",
        color=0xC9A33A
    )
    embed.add_field(name="👑 Цол", value=rank["name"], inline=False)
    embed.add_field(name="⭐ Level", value=user["level"], inline=True)
    embed.add_field(name="✨ EXP", value=f"{current_exp}/{needed}" if user["level"] < MAX_LEVEL else "MAX", inline=True)
    embed.add_field(name="💰 Хэтэвч", value=f"{user['money']}", inline=True)
    embed.add_field(name="🏦 Банк", value=f"{user['bank']}", inline=True)
    embed.add_field(name="💬 Messages", value=f"{user['messages']}", inline=True)
    embed.add_field(name="🛠 Work цалин", value=f"{rank['salary']}+", inline=True)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_image(url=rank["image"])
    await ctx.send(embed=embed)

@bot.command()
async def rank(ctx):
    user = get_user(ctx.author.id)
    rank = get_rank_data(user["level"])

    embed = discord.Embed(
        title="👑 Таны Цол",
        description=f"Та одоогоор **{rank['name']}** байна.",
        color=0xC9A33A
    )
    embed.add_field(name="⭐ Level", value=str(user["level"]), inline=True)
    embed.add_field(name="💰 Work Salary", value=f"{rank['salary']}+", inline=True)
    embed.set_image(url=rank["image"])
    await ctx.send(embed=embed)

@bot.command(aliases=["bal", "money"])
async def balance(ctx, member: discord.Member = None):
    member = member or ctx.author
    user = get_user(member.id)

    embed = discord.Embed(
        title=f"💰 {member.display_name}-ийн хөрөнгө",
        color=0x2ECC71
    )
    embed.add_field(name="Хэтэвч", value=str(user["money"]), inline=True)
    embed.add_field(name="Банк", value=str(user["bank"]), inline=True)
    embed.add_field(name="Нийт", value=str(user["money"] + user["bank"]), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def work(ctx):
    user = get_user(ctx.author.id)
    now = datetime.utcnow()
    last_work = parse_time(user["last_work"])

    cooldown = timedelta(minutes=15)
    if last_work and now - last_work < cooldown:
        remain = cooldown - (now - last_work)
        minutes = int(remain.total_seconds() // 60)
        seconds = int(remain.total_seconds() % 60)
        await ctx.send(f"⏳ Дахин ажил хийх хүртэл `{minutes}м {seconds}с` хүлээ.")
        return

    rank = get_rank_data(user["level"])
    salary_base = rank["salary"]
    earned = random.randint(max(1, salary_base - 120), salary_base + 180)

    user["money"] += earned
    user["last_work"] = now_str()

    bonus_exp = random.randint(5, 12)
    old_level = user["level"]
    leveled = add_exp(user, bonus_exp)

    save_data(data)

    embed = discord.Embed(
        title="🛠 Ажил хийлээ",
        description=f"{ctx.author.mention} **{earned} мөнгө** оллоо!",
        color=0xF1C40F
    )
    embed.add_field(name="👑 Цол", value=rank["name"], inline=False)
    embed.add_field(name="💵 Суурь цалин", value=str(salary_base), inline=True)
    embed.add_field(name="✨ EXP", value=f"+{bonus_exp}", inline=True)
    embed.set_image(url=rank["image"])

    if leveled:
        new_rank = get_rank_data(user["level"])
        embed.add_field(
            name="🎉 Level Up",
            value=f"{old_level} → {user['level']}\nШинэ цол: **{new_rank['name']}**",
            inline=False
        )

    await ctx.send(embed=embed)

@bot.command()
async def daily(ctx):
    user = get_user(ctx.author.id)
    now = datetime.utcnow()
    last_daily = parse_time(user["last_daily"])

    cooldown = timedelta(hours=24)
    if last_daily and now - last_daily < cooldown:
        remain = cooldown - (now - last_daily)
        hours = int(remain.total_seconds() // 3600)
        minutes = int((remain.total_seconds() % 3600) // 60)
        await ctx.send(f"⏳ Daily авах хүртэл `{hours}ц {minutes}м` үлдлээ.")
        return

    rank = get_rank_data(user["level"])
    reward = 500 + (rank["salary"] // 2)

    user["money"] += reward
    user["last_daily"] = now_str()

    bonus_exp = random.randint(10, 20)
    add_exp(user, bonus_exp)

    save_data(data)

    embed = discord.Embed(
        title="🎁 Daily Reward",
        description=f"Та өнөөдрийн шагналаар **{reward} мөнгө** авлаа!",
        color=0x3498DB
    )
    embed.add_field(name="✨ Bonus EXP", value=f"+{bonus_exp}", inline=True)
    embed.add_field(name="👑 Цол", value=rank["name"], inline=True)
    embed.set_image(url=rank["image"])
    await ctx.send(embed=embed)

@bot.command()
async def deposit(ctx, amount: str):
    user = get_user(ctx.author.id)

    if amount.lower() == "all":
        amt = user["money"]
    else:
        if not amount.isdigit():
            await ctx.send("❌ Зөв тоо оруул. Жишээ: `S deposit 500` эсвэл `S deposit all`")
            return
        amt = int(amount)

    if amt <= 0:
        await ctx.send("❌ Эерэг тоо оруул.")
        return
    if user["money"] < amt:
        await ctx.send("❌ Хэтэвчинд чинь хүрэлцэхгүй мөнгө байна.")
        return

    user["money"] -= amt
    user["bank"] += amt
    save_data(data)
    await ctx.send(f"🏦 **{amt}** мөнгийг банканд хийлээ.")

@bot.command()
async def withdraw(ctx, amount: str):
    user = get_user(ctx.author.id)

    if amount.lower() == "all":
        amt = user["bank"]
    else:
        if not amount.isdigit():
            await ctx.send("❌ Зөв тоо оруул. Жишээ: `S withdraw 500` эсвэл `S withdraw all`")
            return
        amt = int(amount)

    if amt <= 0:
        await ctx.send("❌ Эерэг тоо оруул.")
        return
    if user["bank"] < amt:
        await ctx.send("❌ Банканд хүрэлцэхгүй мөнгө байна.")
        return

    user["bank"] -= amt
    user["money"] += amt
    save_data(data)
    await ctx.send(f"💰 **{amt}** мөнгийг банкнаас авлаа.")

@bot.command(aliases=["lb", "top"])
async def leaderboard(ctx):
    if not data:
        await ctx.send("Одоохондоо дата алга.")
        return

    sorted_users = sorted(
        data.items(),
        key=lambda x: (x[1].get("level", 1), x[1].get("money", 0) + x[1].get("bank", 0)),
        reverse=True
    )[:10]

    embed = discord.Embed(
        title="🏆 Level Leaderboard",
        color=0x9B59B6
    )

    desc = ""
    for i, (uid, udata) in enumerate(sorted_users, start=1):
        member = ctx.guild.get_member(int(uid))
        name = member.display_name if member else f"User {uid}"
        rank = get_rank_data(udata.get("level", 1))
        desc += f"**{i}. {name}** — Lv.{udata.get('level', 1)} | {rank['name']}\n"

    embed.description = desc if desc else "Мэдээлэл алга."
    await ctx.send(embed=embed)

# =========================
# ERROR HANDLER
# =========================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Коммандын утга дутуу байна.")
        return
    await ctx.send(f"⚠ Алдаа гарлаа: `{error}`")

# =========================
# RUN
# =========================
bot.run(TOKEN)
