import discord
from discord.ext import commands
import os
import json
import random
from datetime import datetime, timedelta

# =========================================================
# CONFIG
# =========================================================
TOKEN = os.getenv("TOKEN")  # Railway / Render / hosting дээр env var-аар хийнэ
PREFIX = "S "
DATA_FILE = "hunnu_data.json"
MAX_LEVEL = 20

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# =========================================================
# IMAGE URLS
# Эднийг дараа нь өөрийн AI зургаар солиорой
# =========================================================
IMAGES = {
    "start": "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop",
    "profile": "https://cdn.discordapp.com/attachments/123456789/123456789/khan.png",
    "shop": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?q=80&w=1200&auto=format&fit=crop",
    "hunt": "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop",
    "mine": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop",
    "farm": "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?q=80&w=1200&auto=format&fit=crop",
    "duel": "https://images.unsplash.com/photo-1517466787929-bc90951d0974?q=80&w=1200&auto=format&fit=crop",
    "clan": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200&auto=format&fit=crop",
    "horse": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?q=80&w=1200&auto=format&fit=crop",
    "boss": "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1200&auto=format&fit=crop",
    "leaderboard": "https://images.unsplash.com/photo-1521295121783-8a321d551ad2?q=80&w=1200&auto=format&fit=crop",
    "admin": "https://images.unsplash.com/photo-1516321497487-e288fb19713f?q=80&w=1200&auto=format&fit=crop",
    "army": "https://images.unsplash.com/photo-1508672019048-805c876b67e2?q=80&w=1200&auto=format&fit=crop",
    "city": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=1200&auto=format&fit=crop",
    "bank": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=1200&auto=format&fit=crop",
    "war": "https://images.unsplash.com/photo-1505666287802-931dc83948e9?q=80&w=1200&auto=format&fit=crop",
    "market": "https://images.unsplash.com/photo-1488459716781-31db52582fe9?q=80&w=1200&auto=format&fit=crop",
    "food": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=1200&auto=format&fit=crop",
}

# =========================================================
# RANKS
# =========================================================
RANKS = [
    (1, "Малчин"),
    (5, "Тариачин"),
    (10, "Түлээчин"),
    (15, "Анчин"),
    (20, "Цэрэг"),
    (30, "Аравт"),
    (40, "Зуут"),
    (55, "Мянгат"),
    (70, "Буурч"),
    (85, "Хишигтэн"),
    (100, "Түшмэл"),
    (120, "Ноён"),
    (140, "Жанжин"),
    (160, "Сайд"),
    (180, "Хан"),
    (200, "Их Эзэн Хаан"),
]

UDAMS = ["Боржигин", "Жалайр", "Хонгирад", "Хэрэйд", "Найман", "Мэргид", "Ойрад", "Халх"]

SHOP_ITEMS = {
    "airag": {"price": 50, "type": "food"},
    "mah": {"price": 80, "type": "food"},
    "talh": {"price": 35, "type": "food"},
    "mod": {"price": 60, "type": "resource"},
    "chuluu": {"price": 70, "type": "resource"},
    "tomor": {"price": 120, "type": "resource"},
    "aris": {"price": 110, "type": "resource"},
    "shir": {"price": 140, "type": "resource"},
    "selem": {"price": 500, "type": "weapon"},
    "num_sum": {"price": 450, "type": "weapon"},
    "huayg": {"price": 650, "type": "armor"},
    "mor": {"price": 1200, "type": "mount"},
}

# =========================================================
# DATA HELPERS
# =========================================================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

def get_rank(level: int) -> str:
    current = "Энгийн иргэн"
    for lvl, rank in RANKS:
        if level >= lvl:
            current = rank
    return current

def exp_to_next(level: int) -> int:
    return 100 + (level * 25)

def make_player(user_id: str, name: str):
    return {
        "name": name,
        "gold": 500,
        "silver": 0,
        "bank": 0,
        "level": 1,
        "exp": 0,
        "hp": 100,
        "energy": 100,
        "army": 0,
        "horse": None,
        "clan": None,
        "city": None,
        "udam": random.choice(UDAMS),
        "title": "Шинэ тоглогч",
        "inventory": [],
        "storage": [],
        "married_to": None,
        "daily_last": None,
        "weekly_last": None,
        "monthly_last": None,
        "work_last": None,
        "hunt_last": None,
        "mine_last": None,
        "chop_last": None,
        "fish_last": None,
        "farm_last": None,
        "cooldowns": {},
        "wins": 0,
        "losses": 0,
        "prestige": 0,
        "created_at": datetime.utcnow().isoformat()
    }

def ensure_player(user: discord.User):
    uid = str(user.id)
    if uid not in data:
        data[uid] = make_player(uid, user.name)
        save_data()
    else:
        data[uid]["name"] = user.name
    return data[uid]

def add_item(player: dict, item_name: str, qty: int = 1):
    for _ in range(qty):
        player["inventory"].append(item_name)

def remove_item(player: dict, item_name: str, qty: int = 1) -> bool:
    if player["inventory"].count(item_name) < qty:
        return False
    for _ in range(qty):
        player["inventory"].remove(item_name)
    return True

def add_exp(player: dict, amount: int):
    player["exp"] += amount
    leveled = []
    while player["level"] < MAX_LEVEL and player["exp"] >= exp_to_next(player["level"]):
        player["exp"] -= exp_to_next(player["level"])
        player["level"] += 1
        player["title"] = get_rank(player["level"])
        leveled.append(player["level"])
    return leveled

def human_time_left(last_iso: str, hours: int) -> str:
    if not last_iso:
        return "0m"
    last = datetime.fromisoformat(last_iso)
    nxt = last + timedelta(hours=hours)
    left = nxt - datetime.utcnow()
    if left.total_seconds() <= 0:
        return "0m"
    mins = int(left.total_seconds() // 60)
    h = mins // 60
    m = mins % 60
    return f"{h}h {m}m"

def on_cooldown(last_iso: str, hours: int) -> bool:
    if not last_iso:
        return False
    last = datetime.fromisoformat(last_iso)
    return datetime.utcnow() < last + timedelta(hours=hours)

def basic_embed(title: str, desc: str, image_key: str = "profile", color: int = 0xB8860B):
    em = discord.Embed(title=title, description=desc, color=color)
    if image_key in IMAGES:
        em.set_image(url=IMAGES[image_key])
    em.timestamp = datetime.utcnow()
    return em

# =========================================================
# EVENTS
# =========================================================
@bot.event
async def on_ready():
    print(f"{bot.user} online боллоо.")

# =========================================================
# CORE COMMANDS
# =========================================================
@bot.command()
async def start(ctx):
    player = ensure_player(ctx.author)
    save_data()
    embed = basic_embed(
        "🏹 Аян эхэллээ",
        f"{ctx.author.mention} амжилттай бүртгэгдлээ.\n\n"
        f"Удам: **{player['udam']}**\n"
        f"Эхний алт: **{player['gold']}**\n"
        f"Цол: **{player['title']}**",
        "start"
    )
    await ctx.send(embed=embed)

@bot.command()
async def profile(ctx, member: discord.Member = None):
    member = member or ctx.author
    player = ensure_player(member)
    embed = discord.Embed(
        title=f"👤 {member.display_name}-ийн Profile",
        color=0xDAA520
    )
    embed.add_field(name="Level", value=str(player["level"]), inline=True)
    embed.add_field(name="EXP", value=f"{player['exp']} / {exp_to_next(player['level'])}", inline=True)
    embed.add_field(name="Gold", value=str(player["gold"]), inline=True)
    embed.add_field(name="Rank", value=get_rank(player["level"]), inline=True)
    embed.add_field(name="Udam", value=player["udam"], inline=True)
    embed.add_field(name="Army", value=str(player["army"]), inline=True)
    embed.add_field(name="HP", value=str(player["hp"]), inline=True)
    embed.add_field(name="Energy", value=str(player["energy"]), inline=True)
    embed.add_field(name="Clan", value=str(player["clan"] or "Байхгүй"), inline=True)
    embed.add_field(name="Wins / Losses", value=f"{player['wins']} / {player['losses']}", inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_image(url=IMAGES["profile"])
    await ctx.send(embed=embed)

@bot.command()
async def stats(ctx):
    player = ensure_player(ctx.author)
    power = player["level"] * 10 + player["army"] * 3 + len(player["inventory"]) * 2
    embed = basic_embed(
        "📊 Stats",
        f"⚔ Power: **{power}**\n"
        f"❤️ HP: **{player['hp']}**\n"
        f"⚡ Energy: **{player['energy']}**\n"
        f"🏅 Prestige: **{player['prestige']}**",
        "profile"
    )
    await ctx.send(embed=embed)

@bot.command()
async def level(ctx):
    player = ensure_player(ctx.author)
    embed = basic_embed(
        "📈 Level",
        f"Level: **{player['level']}**\nEXP: **{player['exp']} / {exp_to_next(player['level'])}**\nRank: **{get_rank(player['level'])}**",
        "leaderboard"
    )
    await ctx.send(embed=embed)

@bot.command()
async def exp(ctx):
    player = ensure_player(ctx.author)
    await ctx.send(embed=basic_embed("✨ EXP", f"EXP: **{player['exp']} / {exp_to_next(player['level'])}**", "leaderboard"))

@bot.command()
async def gold(ctx):
    player = ensure_player(ctx.author)
    await ctx.send(embed=basic_embed("💰 Gold", f"Таны алт: **{player['gold']}**", "bank"))

@bot.command()
async def silver(ctx):
    player = ensure_player(ctx.author)
    await ctx.send(embed=basic_embed("🥈 Silver", f"Таны мөнгө: **{player['silver']}**", "bank"))

@bot.command()
async def inventory(ctx):
    player = ensure_player(ctx.author)
    items = player["inventory"][:30]
    txt = ", ".join(items) if items else "Хоосон"
    await ctx.send(embed=basic_embed("🎒 Inventory", txt, "shop"))

@bot.command()
async def storage(ctx):
    player = ensure_player(ctx.author)
    items = player["storage"][:30]
    txt = ", ".join(items) if items else "Хоосон"
    await ctx.send(embed=basic_embed("📦 Storage", txt, "shop"))

@bot.command()
async def rank(ctx):
    player = ensure_player(ctx.author)
    await ctx.send(embed=basic_embed("👑 Rank", f"Таны цол: **{get_rank(player['level'])}**", "profile"))

@bot.command()
async def title(ctx):
    player = ensure_player(ctx.author)
    await ctx.send(embed=basic_embed("📛 Title", f"Таны title: **{player['title']}**", "profile"))

@bot.command()
async def energy(ctx):
    player = ensure_player(ctx.author)
    await ctx.send(embed=basic_embed("⚡ Energy", f"Energy: **{player['energy']}**", "profile"))

@bot.command()
async def hp(ctx):
    player = ensure_player(ctx.author)
    await ctx.send(embed=basic_embed("❤️ HP", f"HP: **{player['hp']}**", "profile"))

@bot.command()
async def help(ctx):
    text = (
        f"**{PREFIX}start, {PREFIX}profile, {PREFIX}stats, {PREFIX}daily, {PREFIX}work, {PREFIX}hunt, {PREFIX}mine, {PREFIX}chop, {PREFIX}farm, {PREFIX}fish**\n"
        f"**{PREFIX}shop, {PREFIX}buy <item>, {PREFIX}sell <item>, {PREFIX}inventory**\n"
        f"**{PREFIX}duel @user, {PREFIX}army, {PREFIX}recruit, {PREFIX}trainarmy**\n"
        f"**{PREFIX}clan, {PREFIX}createclan <name>, {PREFIX}joinclan <name>**\n"
        f"**{PREFIX}leaderboard, {PREFIX}rank, {PREFIX}udam, {PREFIX}horse**\n"
        f"**Admin:** {PREFIX}givegold, {PREFIX}setlevel, {PREFIX}addexp, {PREFIX}resetplayer"
    )
    await ctx.send(embed=basic_embed("📜 Help", text, "admin"))

# =========================================================
# ECONOMY COMMANDS
# =========================================================
@bot.command()
async def daily(ctx):
    player = ensure_player(ctx.author)
    if on_cooldown(player["daily_last"], 24):
        await ctx.send(embed=basic_embed("⏳ Daily", f"Дахин авах хүртэл: **{human_time_left(player['daily_last'], 24)}**", "bank"))
        return
    amount = random.randint(250, 600)
    player["gold"] += amount
    player["daily_last"] = datetime.utcnow().isoformat()
    levels = add_exp(player, random.randint(15, 35))
    save_data()
    msg = f"{ctx.author.mention} өдөр тутмын шагналаар **{amount} gold** авлаа."
    if levels:
        msg += f"\n🎉 Level up: **{player['level']}**"
    await ctx.send(embed=basic_embed("🎁 Daily Reward", msg, "bank"))

@bot.command()
async def weekly(ctx):
    player = ensure_player(ctx.author)
    if on_cooldown(player["weekly_last"], 24 * 7):
        await ctx.send(embed=basic_embed("⏳ Weekly", f"Үлдсэн хугацаа: **{human_time_left(player['weekly_last'], 24 * 7)}**", "bank"))
        return
    amount = random.randint(1800, 3200)
    player["gold"] += amount
    player["weekly_last"] = datetime.utcnow().isoformat()
    add_exp(player, random.randint(40, 80))
    save_data()
    await ctx.send(embed=basic_embed("🗓 Weekly Reward", f"Та **{amount} gold** авлаа.", "bank"))

@bot.command()
async def monthly(ctx):
    player = ensure_player(ctx.author)
    if on_cooldown(player["monthly_last"], 24 * 30):
        await ctx.send(embed=basic_embed("⏳ Monthly", f"Үлдсэн хугацаа: **{human_time_left(player['monthly_last'], 24 * 30)}**", "bank"))
        return
    amount = random.randint(7000, 12000)
    player["gold"] += amount
    player["monthly_last"] = datetime.utcnow().isoformat()
    add_exp(player, random.randint(100, 180))
    save_data()
    await ctx.send(embed=basic_embed("📅 Monthly Reward", f"Та **{amount} gold** авлаа.", "bank"))

@bot.command()
async def work(ctx):
    player = ensure_player(ctx.author)
    if on_cooldown(player["work_last"], 1):
        await ctx.send(embed=basic_embed("⏳ Work", f"Амрах хугацаа: **{human_time_left(player['work_last'], 1)}**", "market"))
        return
    jobs = [
        ("мал маллаж", 90, 180),
        ("ачаа зөөж", 80, 170),
        ("худалдаа хийж", 100, 200),
        ("дарханд тусалж", 120, 220),
        ("харуул хийж", 110, 210),
    ]
    job, lo, hi = random.choice(jobs)
    amount = random.randint(lo, hi)
    player["gold"] += amount
    player["work_last"] = datetime.utcnow().isoformat()
    add_exp(player, random.randint(8, 18))
    save_data()
    await ctx.send(embed=basic_embed("🛠 Work", f"{ctx.author.mention} {job} **{amount} gold** оллоо.", "market"))

@bot.command()
async def beg(ctx):
    player = ensure_player(ctx.author)
    amount = random.randint(10, 75)
    player["gold"] += amount
    save_data()
    await ctx.send(embed=basic_embed("🙏 Beg", f"Танд **{amount} gold** өглөө.", "market"))

@bot.command()
async def bank(ctx):
    player = ensure_player(ctx.author)
    await ctx.send(embed=basic_embed("🏦 Bank", f"Bank balance: **{player['bank']} gold**", "bank"))

@bot.command()
async def deposit(ctx, amount: int):
    player = ensure_player(ctx.author)
    if amount <= 0 or amount > player["gold"]:
        await ctx.send("Алт хүрэхгүй байна.")
        return
    player["gold"] -= amount
    player["bank"] += amount
    save_data()
    await ctx.send(embed=basic_embed("🏦 Deposit", f"Та bank руу **{amount} gold** хийлээ.", "bank"))

@bot.command()
async def withdraw(ctx, amount: int):
    player = ensure_player(ctx.author)
    if amount <= 0 or amount > player["bank"]:
        await ctx.send("Bank balance хүрэхгүй байна.")
        return
    player["bank"] -= amount
    player["gold"] += amount
    save_data()
    await ctx.send(embed=basic_embed("🏦 Withdraw", f"Та bank-аас **{amount} gold** авлаа.", "bank"))

@bot.command()
async def pay(ctx, member: discord.Member, amount: int):
    sender = ensure_player(ctx.author)
    receiver = ensure_player(member)
    if member.bot or amount <= 0 or sender["gold"] < amount:
        await ctx.send("Гүйлгээ амжилтгүй.")
        return
    sender["gold"] -= amount
    receiver["gold"] += amount
    save_data()
    await ctx.send(embed=basic_embed("💸 Pay", f"{ctx.author.mention} → {member.mention} : **{amount} gold**", "bank"))

@bot.command()
async def gamble(ctx, amount: int):
    player = ensure_player(ctx.author)
    if amount <= 0 or player["gold"] < amount:
        await ctx.send("Алт хүрэхгүй байна.")
        return
    if random.random() < 0.45:
        player["gold"] += amount
        result = f"Хожлоо. **+{amount} gold**"
    else:
        player["gold"] -= amount
        result = f"Хожигдлоо. **-{amount} gold**"
    save_data()
    await ctx.send(embed=basic_embed("🎲 Gamble", result, "market"))

@bot.command()
async def coinflip(ctx, amount: int):
    await gamble(ctx, amount)

@bot.command()
async def dice(ctx, amount: int):
    await gamble(ctx, amount)

@bot.command()
async def slots(ctx, amount: int):
    player = ensure_player(ctx.author)
    if amount <= 0 or player["gold"] < amount:
        await ctx.send("Алт хүрэхгүй байна.")
        return
    icons = ["🍇", "🍒", "🍋", "💎", "⚔️"]
    roll = [random.choice(icons) for _ in range(3)]
    if len(set(roll)) == 1:
        win = amount * 3
        player["gold"] += win
        result = f"{' '.join(roll)}\n🎉 Jackpot! **+{win} gold**"
    else:
        player["gold"] -= amount
        result = f"{' '.join(roll)}\n❌ **-{amount} gold**"
    save_data()
    await ctx.send(embed=basic_embed("🎰 Slots", result, "market"))

# =========================================================
# RESOURCE COMMANDS
# =========================================================
def resource_action(player, key_last, hours, gold_range, exp_range, item_name=None):
    if on_cooldown(player[key_last], hours):
        return None, human_time_left(player[key_last], hours)
    gold = random.randint(*gold_range)
    exp_gain = random.randint(*exp_range)
    player["gold"] += gold
    if item_name:
        add_item(player, item_name, 1)
    player[key_last] = datetime.utcnow().isoformat()
    levels = add_exp(player, exp_gain)
    save_data()
    return (gold, exp_gain, item_name, levels), None

@bot.command()
async def hunt(ctx):
    player = ensure_player(ctx.author)
    result, left = resource_action(player, "hunt_last", 1, (100, 240), (12, 26), "mah")
    if left:
        await ctx.send(embed=basic_embed("⏳ Hunt", f"Дахин ан хийх хүртэл: **{left}**", "hunt"))
        return
    gold_gain, exp_gain, item_name, levels = result
    txt = f"Та ан хийж **{gold_gain} gold**, **{exp_gain} exp** авлаа.\nОлз: **{item_name}**"
    if levels:
        txt += f"\n🎉 Level up: **{player['level']}**"
    await ctx.send(embed=basic_embed("🏹 Hunt", txt, "hunt"))

@bot.command()
async def mine(ctx):
    player = ensure_player(ctx.author)
    result, left = resource_action(player, "mine_last", 1, (110, 260), (12, 24), "tomor")
    if left:
        await ctx.send(embed=basic_embed("⛏ Mine", f"Cooldown: **{left}**", "mine"))
        return
    gold_gain, exp_gain, item_name, levels = result
    await ctx.send(embed=basic_embed("⛏ Mine", f"Та хүдэр олборлож **{gold_gain} gold**, **{exp_gain} exp** авлаа.\nОлз: **{item_name}**", "mine"))

@bot.command()
async def chop(ctx):
    player = ensure_player(ctx.author)
    result, left = resource_action(player, "chop_last", 1, (90, 210), (10, 20), "mod")
    if left:
        await ctx.send(embed=basic_embed("🪓 Chop", f"Cooldown: **{left}**", "farm"))
        return
    gold_gain, exp_gain, item_name, levels = result
    await ctx.send(embed=basic_embed("🪓 Chop", f"Та мод бэлтгэж **{gold_gain} gold**, **{exp_gain} exp** авлаа.\nОлз: **{item_name}**", "farm"))

@bot.command()
async def farm(ctx):
    player = ensure_player(ctx.author)
    result, left = resource_action(player, "farm_last", 1, (80, 200), (10, 18), "talh")
    if left:
        await ctx.send(embed=basic_embed("🌾 Farm", f"Cooldown: **{left}**", "farm"))
        return
    gold_gain, exp_gain, item_name, levels = result
    await ctx.send(embed=basic_embed("🌾 Farm", f"Та ажиллаж **{gold_gain} gold**, **{exp_gain} exp** авлаа.\nОлз: **{item_name}**", "farm"))

@bot.command()
async def fish(ctx):
    player = ensure_player(ctx.author)
    result, left = resource_action(player, "fish_last", 1, (80, 220), (8, 18), "mah")
    if left:
        await ctx.send(embed=basic_embed("🎣 Fish", f"Cooldown: **{left}**", "food"))
        return
    gold_gain, exp_gain, item_name, levels = result
    await ctx.send(embed=basic_embed("🎣 Fish", f"Та загас барьж **{gold_gain} gold**, **{exp_gain} exp** авлаа.", "food"))

# =========================================================
# SHOP
# =========================================================
@bot.command()
async def shop(ctx):
    lines = []
    for item, info in SHOP_ITEMS.items():
        lines.append(f"**{item}** — {info['price']} gold")
    await ctx.send(embed=basic_embed("🏪 Shop", "\n".join(lines), "shop"))

@bot.command()
async def buy(ctx, item_name: str):
    player = ensure_player(ctx.author)
    item_name = item_name.lower()
    if item_name not in SHOP_ITEMS:
        await ctx.send("Тийм item байхгүй.")
        return
    price = SHOP_ITEMS[item_name]["price"]
    if player["gold"] < price:
        await ctx.send("Алт хүрэхгүй байна.")
        return
    player["gold"] -= price
    add_item(player, item_name, 1)
    save_data()
    await ctx.send(embed=basic_embed("🛒 Buy", f"Та **{item_name}** худалдаж авлаа.", "shop"))

@bot.command()
async def sell(ctx, item_name: str):
    player = ensure_player(ctx.author)
    item_name = item_name.lower()
    if item_name not in SHOP_ITEMS:
        await ctx.send("Тийм item байхгүй.")
        return
    if not remove_item(player, item_name, 1):
        await ctx.send("Таны inventory-д байхгүй байна.")
        return
    gain = SHOP_ITEMS[item_name]["price"] // 2
    player["gold"] += gain
    save_data()
    await ctx.send(embed=basic_embed("💱 Sell", f"Та **{item_name}** зарж **{gain} gold** авлаа.", "shop"))

@bot.command()
async def use(ctx, item_name: str):
    player = ensure_player(ctx.author)
    item_name = item_name.lower()
    if not remove_item(player, item_name, 1):
        await ctx.send("Тэр item алга.")
        return

    if item_name in ["airag", "mah", "talh"]:
        player["energy"] = min(100, player["energy"] + 20)
        player["hp"] = min(100, player["hp"] + 10)
        msg = f"Та **{item_name}** хэрэглэж HP/ENERGY сэргээв."
    elif item_name == "mor":
        player["horse"] = "Дайны Морь"
        msg = "Та морьтой боллоо."
    else:
        msg = f"Та **{item_name}** ашиглалаа."
    save_data()
    await ctx.send(embed=basic_embed("🧪 Use Item", msg, "food"))

@bot.command()
async def item(ctx, *, item_name: str):
    item_name = item_name.lower()
    if item_name not in SHOP_ITEMS:
        await ctx.send("Тийм item байхгүй.")
        return
    info = SHOP_ITEMS[item_name]
    await ctx.send(embed=basic_embed("📦 Item Info", f"Нэр: **{item_name}**\nҮнэ: **{info['price']}**\nТөрөл: **{info['type']}**", "shop"))

# =========================================================
# BATTLE / RPG
# =========================================================
@bot.command()
async def duel(ctx, member: discord.Member):
    if member.bot or member == ctx.author:
        await ctx.send("Өөр хүн сонго.")
        return
    p1 = ensure_player(ctx.author)
    p2 = ensure_player(member)

    power1 = p1["level"] * 10 + p1["army"] * 3 + random.randint(0, 50)
    power2 = p2["level"] * 10 + p2["army"] * 3 + random.randint(0, 50)

    if power1 >= power2:
        winner, loser = p1, p2
        winner_user, loser_user = ctx.author, member
        reward = random.randint(80, 220)
        winner["gold"] += reward
        winner["wins"] += 1
        loser["losses"] += 1
        add_exp(winner, 20)
        text = f"⚔ {winner_user.mention} яллаа!\nШагнал: **{reward} gold**"
    else:
        winner, loser = p2, p1
        winner_user, loser_user = member, ctx.author
        reward = random.randint(80, 220)
        winner["gold"] += reward
        winner["wins"] += 1
        loser["losses"] += 1
        add_exp(winner, 20)
        text = f"⚔ {winner_user.mention} яллаа!\nШагнал: **{reward} gold**"

    save_data()
    await ctx.send(embed=basic_embed("⚔ Duel", text, "duel"))

@bot.command()
async def attack(ctx):
    player = ensure_player(ctx.author)
    damage = random.randint(10, 40) + player["level"] * 2
    reward = random.randint(60, 180)
    player["gold"] += reward
    add_exp(player, random.randint(12, 24))
    save_data()
    await ctx.send(embed=basic_embed("🗡 Attack", f"Та мангас цохиж **{damage} damage** өглөө.\nШагнал: **{reward} gold**", "boss"))

@bot.command()
async def defend(ctx):
    player = ensure_player(ctx.author)
    block = random.randint(15, 50)
    add_exp(player, random.randint(5, 12))
    save_data()
    await ctx.send(embed=basic_embed("🛡 Defend", f"Та **{block}%** хамгаалалт хийлээ.", "boss"))

@bot.command()
async def heal(ctx):
    player = ensure_player(ctx.author)
    if player["gold"] < 100:
        await ctx.send("Эмчлүүлэх алт хүрэхгүй.")
        return
    player["gold"] -= 100
    player["hp"] = min(100, player["hp"] + 35)
    save_data()
    await ctx.send(embed=basic_embed("💚 Heal", f"Та эмчлүүлж HP: **{player['hp']}** боллоо.", "food"))

@bot.command()
async def revive(ctx):
    player = ensure_player(ctx.author)
    player["hp"] = 100
    player["energy"] = 100
    save_data()
    await ctx.send(embed=basic_embed("✨ Revive", "Та бүрэн сэргээлээ.", "boss"))

# =========================================================
# HORSE / ARMY
# =========================================================
@bot.command()
async def horse(ctx):
    player = ensure_player(ctx.author)
    text = player["horse"] if player["horse"] else "Танд морь алга."
    await ctx.send(embed=basic_embed("🐎 Horse", text, "horse"))

@bot.command()
async def stable(ctx):
    player = ensure_player(ctx.author)
    await ctx.send(embed=basic_embed("🏇 Stable", f"Таны морь: **{player['horse'] or 'Байхгүй'}**", "horse"))

@bot.command()
async def feedhorse(ctx):
    player = ensure_player(ctx.author)
    if not player["horse"]:
        await ctx.send("Таньд морь алга.")
        return
    await ctx.send(embed=basic_embed("🌾 Feed Horse", "Та морио тэжээлээ.", "horse"))

@bot.command()
async def trainhorse(ctx):
    player = ensure_player(ctx.author)
    if not player["horse"]:
        await ctx.send("Морь байхгүй.")
        return
    add_exp(player, 10)
    save_data()
    await ctx.send(embed=basic_embed("🏇 Train Horse", "Морь илүү хүчтэй боллоо.", "horse"))

@bot.command()
async def army(ctx):
    player = ensure_player(ctx.author)
    power = player["army"] * 3 + player["level"] * 10
    await ctx.send(embed=basic_embed("⚔ Army", f"Цэрэг: **{player['army']}**\nArmy Power: **{power}**", "army"))

@bot.command()
async def recruit(ctx, amount: int = 1):
    player = ensure_player(ctx.author)
    if amount <= 0:
        await ctx.send("Зөв тоо өг.")
        return
    cost = amount * 120
    if player["gold"] < cost:
        await ctx.send("Алт хүрэхгүй байна.")
        return
    player["gold"] -= cost
    player["army"] += amount
    save_data()
    await ctx.send(embed=basic_embed("🪖 Recruit", f"Та **{amount}** цэрэг элсүүллээ.", "army"))

@bot.command()
async def dismiss(ctx, amount: int = 1):
    player = ensure_player(ctx.author)
    if amount <= 0 or player["army"] < amount:
        await ctx.send("Цэрэг хүрэхгүй.")
        return
    player["army"] -= amount
    save_data()
    await ctx.send(embed=basic_embed("📤 Dismiss", f"Та **{amount}** цэрэг халлаа.", "army"))

@bot.command()
async def trainarmy(ctx):
    player = ensure_player(ctx.author)
    if player["army"] <= 0:
        await ctx.send("Арми байхгүй.")
        return
    cost = max(50, player["army"] * 10)
    if player["gold"] < cost:
        await ctx.send("Алт хүрэхгүй байна.")
        return
    player["gold"] -= cost
    add_exp(player, 15)
    save_data()
    await ctx.send(embed=basic_embed("🏹 Train Army", f"Армиа сургаж **{cost} gold** зарцууллаа.", "army"))

# =========================================================
# CLAN SYSTEM
# =========================================================
clans = {}

@bot.command()
async def createclan(ctx, *, name: str):
    player = ensure_player(ctx.author)
    if player["clan"]:
        await ctx.send("Та аль хэдийн clan-тай байна.")
        return
    if name in clans:
        await ctx.send("Ийм clan аль хэдийн байна.")
        return
    clans[name] = {"owner": str(ctx.author.id), "members": [str(ctx.author.id)], "bank": 0, "level": 1}
    player["clan"] = name
    save_data()
    await ctx.send(embed=basic_embed("🏳 Create Clan", f"**{name}** clan үүслээ.", "clan"))

@bot.command()
async def clan(ctx):
    player = ensure_player(ctx.author)
    if not player["clan"]:
        await ctx.send(embed=basic_embed("🏳 Clan", "Та clan-гүй байна.", "clan"))
        return
    c = clans.get(player["clan"], {"members": [], "bank": 0, "level": 1})
    await ctx.send(embed=basic_embed(
        "🏳 Clan Info",
        f"Нэр: **{player['clan']}**\nГишүүд: **{len(c['members'])}**\nBank: **{c['bank']}**\nLevel: **{c['level']}**",
        "clan"
    ))

@bot.command()
async def joinclan(ctx, *, name: str):
    player = ensure_player(ctx.author)
    if player["clan"]:
        await ctx.send("Та clan-тай байна.")
        return
    if name not in clans:
        await ctx.send("Тийм clan байхгүй.")
        return
    clans[name]["members"].append(str(ctx.author.id))
    player["clan"] = name
    save_data()
    await ctx.send(embed=basic_embed("🤝 Join Clan", f"Та **{name}** clan-д нэгдлээ.", "clan"))

@bot.command()
async def leaveclan(ctx):
    player = ensure_player(ctx.author)
    name = player["clan"]
    if not name:
        await ctx.send("Та clan-гүй.")
        return
    if name in clans and str(ctx.author.id) in clans[name]["members"]:
        clans[name]["members"].remove(str(ctx.author.id))
    player["clan"] = None
    save_data()
    await ctx.send(embed=basic_embed("🚪 Leave Clan", f"Та **{name}** clan-аас гарлаа.", "clan"))

# =========================================================
# SOCIAL
# =========================================================
@bot.command()
async def marry(ctx, member: discord.Member):
    p1 = ensure_player(ctx.author)
    p2 = ensure_player(member)
    if member.bot or member == ctx.author:
        await ctx.send("Болохгүй.")
        return
    p1["married_to"] = str(member.id)
    p2["married_to"] = str(ctx.author.id)
    save_data()
    await ctx.send(embed=basic_embed("💍 Marry", f"{ctx.author.mention} ❤️ {member.mention}", "profile"))

@bot.command()
async def divorce(ctx):
    p = ensure_player(ctx.author)
    if not p["married_to"]:
        await ctx.send("Та гэрлээгүй байна.")
        return
    other_id = p["married_to"]
    if other_id in data:
        data[other_id]["married_to"] = None
    p["married_to"] = None
    save_data()
    await ctx.send(embed=basic_embed("💔 Divorce", "Гэрлэлт цуцлагдлаа.", "profile"))

@bot.command()
async def partner(ctx):
    p = ensure_player(ctx.author)
    if not p["married_to"]:
        await ctx.send("Таньд хань байхгүй.")
        return
    member = ctx.guild.get_member(int(p["married_to"]))
    name = member.mention if member else "Unknown"
    await ctx.send(embed=basic_embed("❤️ Partner", f"Таны хань: {name}", "profile"))

@bot.command()
async def gift(ctx, member: discord.Member, item_name: str):
    sender = ensure_player(ctx.author)
    receiver = ensure_player(member)
    if not remove_item(sender, item_name, 1):
        await ctx.send("Тэр item байхгүй.")
        return
    add_item(receiver, item_name, 1)
    save_data()
    await ctx.send(embed=basic_embed("🎁 Gift", f"{ctx.author.mention} {member.mention}-д **{item_name}** өглөө.", "shop"))

# =========================================================
# LEADERBOARD
# =========================================================
@bot.command()
async def leaderboard(ctx):
    players = sorted(data.items(), key=lambda x: x[1].get("level", 1), reverse=True)[:10]
    lines = []
    for i, (uid, p) in enumerate(players, start=1):
        lines.append(f"**{i}.** {p['name']} — Lv.{p['level']} — {p['gold']} gold")
    await ctx.send(embed=basic_embed("🏆 Leaderboard", "\n".join(lines) if lines else "Хоосон", "leaderboard"))

@bot.command()
async def topgold(ctx):
    players = sorted(data.items(), key=lambda x: x[1].get("gold", 0), reverse=True)[:10]
    lines = [f"**{i}.** {p['name']} — {p['gold']} gold" for i, (_, p) in enumerate(players, 1)]
    await ctx.send(embed=basic_embed("💰 Top Gold", "\n".join(lines) if lines else "Хоосон", "leaderboard"))

@bot.command()
async def toplevel(ctx):
    players = sorted(data.items(), key=lambda x: x[1].get("level", 1), reverse=True)[:10]
    lines = [f"**{i}.** {p['name']} — Lv.{p['level']}" for i, (_, p) in enumerate(players, 1)]
    await ctx.send(embed=basic_embed("📈 Top Level", "\n".join(lines) if lines else "Хоосон", "leaderboard"))

@bot.command()
async def ranks(ctx):
    text = "\n".join([f"Lv.{lvl} — **{name}**" for lvl, name in RANKS])
    await ctx.send(embed=basic_embed("👑 Rank List", text, "profile"))

@bot.command()
async def udam(ctx):
    player = ensure_player(ctx.author)
    await ctx.send(embed=basic_embed("🧬 Udam", f"Таны удам: **{player['udam']}**", "profile"))

@bot.command()
async def udamroll(ctx):
    player = ensure_player(ctx.author)
    cost = 500
    if player["gold"] < cost:
        await ctx.send("Удам солих алт хүрэхгүй байна.")
        return
    player["gold"] -= cost
    old = player["udam"]
    player["udam"] = random.choice(UDAMS)
    save_data()
    await ctx.send(embed=basic_embed("🎲 Udam Roll", f"**{old}** → **{player['udam']}**", "profile"))

# =========================================================
# ADMIN COMMANDS
# =========================================================
def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

@bot.command()
@is_admin()
async def givegold(ctx, member: discord.Member, amount: int):
    player = ensure_player(member)
    player["gold"] += amount
    save_data()
    await ctx.send(embed=basic_embed("🛡 Admin GiveGold", f"{member.mention} → **+{amount} gold**", "admin"))

@bot.command()
@is_admin()
async def removegold(ctx, member: discord.Member, amount: int):
    player = ensure_player(member)
    player["gold"] = max(0, player["gold"] - amount)
    save_data()
    await ctx.send(embed=basic_embed("🛡 Admin RemoveGold", f"{member.mention} → **-{amount} gold**", "admin"))

@bot.command()
@is_admin()
async def setgold(ctx, member: discord.Member, amount: int):
    player = ensure_player(member)
    player["gold"] = max(0, amount)
    save_data()
    await ctx.send(embed=basic_embed("🛡 Admin SetGold", f"{member.mention} gold = **{amount}**", "admin"))

@bot.command()
@is_admin()
async def addexpadmin(ctx, member: discord.Member, amount: int):
    player = ensure_player(member)
    levels = add_exp(player, amount)
    save_data()
    await ctx.send(embed=basic_embed("🛡 Admin AddEXP", f"{member.mention} → **+{amount} exp**\nCurrent level: **{player['level']}**", "admin"))

@bot.command(name="setlevel")
@is_admin()
async def setlevel_command(ctx, member: discord.Member, level_value: int):
    player = ensure_player(member)
    player["level"] = max(1, min(MAX_LEVEL, level_value))
    player["exp"] = 0
    player["title"] = get_rank(player["level"])
    save_data()
    await ctx.send(embed=basic_embed("🛡 Admin SetLevel", f"{member.mention} level = **{player['level']}**", "admin"))

@bot.command()
@is_admin()
async def resetplayer(ctx, member: discord.Member):
    data[str(member.id)] = make_player(str(member.id), member.name)
    save_data()
    await ctx.send(embed=basic_embed("🛡 Admin ResetPlayer", f"{member.mention} reset хийгдлээ.", "admin"))

@bot.command()
@is_admin()
async def giveitem(ctx, member: discord.Member, item_name: str):
    player = ensure_player(member)
    add_item(player, item_name.lower(), 1)
    save_data()
    await ctx.send(embed=basic_embed("🛡 Admin GiveItem", f"{member.mention} **{item_name}** авлаа.", "admin"))

@bot.command()
@is_admin()
async def announce(ctx, *, text: str):
    await ctx.send(embed=basic_embed("📢 Announcement", text, "admin"))

@bot.command()
@is_admin()
async def savedata(ctx):
    save_data()
    await ctx.send(embed=basic_embed("💾 Save", "Data хадгалагдлаа.", "admin"))

# =========================================================
# 100+ COMMAND AUTO-REGISTRATION
# Эд нар бүгд зурагтай embed command хэлбэрээр ажиллана
# =========================================================
AUTO_COMMANDS = {
    # info / utility
    "avatar": ("🖼 Avatar", "Таны avatar-г харах команд.", "profile"),
    "banner": ("🏳 Banner", "Profile banner систем.", "profile"),
    "history": ("📚 History", "Таны түүхэн бүртгэл.", "profile"),
    "cooldowns": ("⏳ Cooldowns", "Cooldown системийн мэдээлэл.", "profile"),
    "power": ("💥 Power", "Тулааны хүчний тооцоолол.", "profile"),
    "rename": ("✏ Rename", "Нэр солих систем placeholder.", "profile"),
    "nextrank": ("⬆ Next Rank", "Дараагийн цол руу ахихад EXP цуглуул.", "profile"),
    "prestige": ("🌟 Prestige", "Prestige систем placeholder.", "leaderboard"),
    "rebirth": ("♻ Rebirth", "Rebirth систем placeholder.", "leaderboard"),
    "milestones": ("🎯 Milestones", "Milestone reward систем.", "leaderboard"),
    "rewards": ("🎁 Rewards", "Level reward систем.", "leaderboard"),
    "tax": ("💼 Tax", "Татвар хураах placeholder.", "bank"),
    "interest": ("📊 Interest", "Bank interest placeholder.", "bank"),
    "blackjack": ("🃏 Blackjack", "Blackjack placeholder. Одоохондоо gamble ашигла.", "market"),
    "roulette": ("🎡 Roulette", "Roulette placeholder. Одоохондоо gamble ашигла.", "market"),
    "lottery": ("🎟 Lottery", "Lottery систем placeholder.", "market"),
    "claimlottery": ("🏆 Claim Lottery", "Lottery reward placeholder.", "market"),
    "market": ("🏪 Market", "Player market placeholder.", "market"),
    "listitem": ("📋 List Item", "Market дээр item listing хийх placeholder.", "market"),
    "unlist": ("❌ Unlist", "Listing болиулах placeholder.", "market"),
    "marketbuy": ("🛒 Market Buy", "Market purchase placeholder.", "market"),
    "merchant": ("🧔 Merchant", "Худалдаачин ирлээ.", "market"),
    "repair": ("🔧 Repair", "Item засварлах placeholder.", "shop"),
    "upgrade": ("⬆ Upgrade", "Item upgrade placeholder.", "shop"),
    "enchant": ("✨ Enchant", "Item enchant placeholder.", "shop"),
    "craft": ("🛠 Craft", "Craft систем placeholder.", "shop"),
    "recipe": ("📜 Recipe", "Craft recipe placeholder.", "shop"),
    "harvest": ("🌾 Harvest", "Harvest placeholder.", "farm"),
    "forage": ("🍄 Forage", "Forage placeholder.", "farm"),
    "cook": ("🍖 Cook", "Cook placeholder.", "food"),
    "smith": ("⚒ Smith", "Smith placeholder.", "mine"),
    "tailor": ("🧵 Tailor", "Tailor placeholder.", "shop"),
    "build": ("🏗 Build", "Build placeholder.", "city"),
    "dig": ("🕳 Dig", "Dig placeholder.", "mine"),
    "caravan": ("🐫 Caravan", "Caravan placeholder.", "market"),
    "trade": ("🤝 Trade", "Trade placeholder.", "market"),
    "labor": ("🧱 Labor", "Labor placeholder.", "market"),
    "skill": ("🌀 Skill", "Skill command placeholder.", "boss"),
    "skills": ("📚 Skills", "Skills list placeholder.", "boss"),
    "boss": ("👹 Boss", "Boss fight placeholder.", "boss"),
    "raid": ("🔥 Raid", "Raid placeholder.", "war"),
    "dungeon": ("🏰 Dungeon", "Dungeon placeholder.", "war"),
    "tower": ("🗼 Tower", "Tower placeholder.", "war"),
    "arena": ("⚔ Arena", "Arena placeholder.", "war"),
    "combo": ("💥 Combo", "Combo placeholder.", "war"),
    "crit": ("🎯 Crit", "Critical strike placeholder.", "war"),
    "spar": ("🥊 Spar", "Friendly spar placeholder.", "duel"),
    "ride": ("🐎 Ride", "Ride placeholder.", "horse"),
    "march": ("🚶 March", "March placeholder.", "army"),
    "camp": ("⛺ Camp", "Camp placeholder.", "army"),
    "siege": ("🏹 Siege", "Siege placeholder.", "war"),
    "patrol": ("🚩 Patrol", "Patrol placeholder.", "army"),
    "guard": ("🛡 Guard", "Guard placeholder.", "army"),
    "clanmembers": ("👥 Clan Members", "Clan members placeholder.", "clan"),
    "clanbank": ("🏦 Clan Bank", "Clan bank placeholder.", "clan"),
    "clandeposit": ("💰 Clan Deposit", "Clan deposit placeholder.", "clan"),
    "clanwithdraw": ("💸 Clan Withdraw", "Clan withdraw placeholder.", "clan"),
    "clanupgrade": ("⬆ Clan Upgrade", "Clan upgrade placeholder.", "clan"),
    "clanwar": ("⚔ Clan War", "Clan war placeholder.", "war"),
    "claninvite": ("📨 Clan Invite", "Clan invite placeholder.", "clan"),
    "clankick": ("👢 Clan Kick", "Clan kick placeholder.", "clan"),
    "clanpromote": ("📈 Clan Promote", "Clan promote placeholder.", "clan"),
    "clandemote": ("📉 Clan Demote", "Clan demote placeholder.", "clan"),
    "empire": ("👑 Empire", "Empire info placeholder.", "city"),
    "city": ("🏙 City", "City info placeholder.", "city"),
    "village": ("🏘 Village", "Village info placeholder.", "city"),
    "land": ("🗺 Land", "Land info placeholder.", "city"),
    "conquer": ("🏴 Conquer", "Conquer placeholder.", "war"),
    "occupy": ("📍 Occupy", "Occupy placeholder.", "war"),
    "collecttax": ("🧾 Collect Tax", "Collect tax placeholder.", "city"),
    "buildfarm": ("🌾 Build Farm", "Build farm placeholder.", "city"),
    "buildmine": ("⛏ Build Mine", "Build mine placeholder.", "city"),
    "buildwall": ("🧱 Build Wall", "Build wall placeholder.", "city"),
    "upgradecity": ("⬆ Upgrade City", "Upgrade city placeholder.", "city"),
    "govern": ("📜 Govern", "Govern placeholder.", "city"),
    "revolt": ("🔥 Revolt", "Revolt placeholder.", "war"),
    "defendcity": ("🛡 Defend City", "Defend city placeholder.", "war"),
    "attackcity": ("⚔ Attack City", "Attack city placeholder.", "war"),
    "map": ("🗺 Map", "Map placeholder.", "city"),
    "bloodline": ("🩸 Bloodline", "Bloodline placeholder.", "profile"),
    "talent": ("🌠 Talent", "Talent placeholder.", "profile"),
    "talentroll": ("🎲 Talent Roll", "Talent roll placeholder.", "profile"),
    "destiny": ("🌌 Destiny", "Destiny placeholder.", "profile"),
    "blessings": ("🙏 Blessings", "Blessings placeholder.", "profile"),
    "curse": ("☠ Curse", "Curse placeholder.", "profile"),
    "aura": ("✨ Aura", "Aura placeholder.", "profile"),
    "rarity": ("💎 Rarity", "Rarity placeholder.", "profile"),
    "adopt": ("👶 Adopt", "Adopt placeholder.", "profile"),
    "child": ("🧒 Child", "Child placeholder.", "profile"),
    "family": ("🏠 Family", "Family placeholder.", "profile"),
    "bond": ("🔗 Bond", "Bond placeholder.", "profile"),
    "ally": ("🤝 Ally", "Ally placeholder.", "profile"),
    "enemy": ("😈 Enemy", "Enemy placeholder.", "profile"),
    "ping": ("🏓 Ping", "Pong!", "admin"),
    "choose": ("🎯 Choose", "Random choose placeholder.", "admin"),
    "8ball": ("🎱 8Ball", "8Ball placeholder.", "admin"),
    "quote": ("📖 Quote", "Random quote placeholder.", "profile"),
    "mongol": ("🐎 Mongol Fact", "Монгол түүхийн fact placeholder.", "profile"),
    "dailyfact": ("📚 Daily Fact", "Daily fact placeholder.", "profile"),

    # extra admin-style placeholders to push 100+
    "setexp": ("🛡 Set EXP", "Admin placeholder.", "admin"),
    "setbank": ("🛡 Set Bank", "Admin placeholder.", "admin"),
    "resetmoney": ("🛡 Reset Money", "Admin placeholder.", "admin"),
    "wipeinventory": ("🛡 Wipe Inventory", "Admin placeholder.", "admin"),
    "healuser": ("🛡 Heal User", "Admin placeholder.", "admin"),
    "reviveuser": ("🛡 Revive User", "Admin placeholder.", "admin"),
    "sethp": ("🛡 Set HP", "Admin placeholder.", "admin"),
    "setenergy": ("🛡 Set Energy", "Admin placeholder.", "admin"),
    "settitle": ("🛡 Set Title", "Admin placeholder.", "admin"),
    "setrank": ("🛡 Set Rank", "Admin placeholder.", "admin"),
    "setudam": ("🛡 Set Udam", "Admin placeholder.", "admin"),
    "settalent": ("🛡 Set Talent", "Admin placeholder.", "admin"),
    "admincreateclan": ("🛡 Admin Create Clan", "Admin placeholder.", "admin"),
    "deleteclan": ("🛡 Delete Clan", "Admin placeholder.", "admin"),
    "addclanbank": ("🛡 Add Clan Bank", "Admin placeholder.", "admin"),
    "setclanlevel": ("🛡 Set Clan Level", "Admin placeholder.", "admin"),
    "forcewar": ("🛡 Force War", "Admin placeholder.", "admin"),
    "stopwar": ("🛡 Stop War", "Admin placeholder.", "admin"),
    "setcityowner": ("🛡 Set City Owner", "Admin placeholder.", "admin"),
    "resetcity": ("🛡 Reset City", "Admin placeholder.", "admin"),
    "givearmy": ("🛡 Give Army", "Admin placeholder.", "admin"),
    "setarmy": ("🛡 Set Army", "Admin placeholder.", "admin"),
    "reloadshop": ("🛡 Reload Shop", "Admin placeholder.", "admin"),
    "reloadconfig": ("🛡 Reload Config", "Admin placeholder.", "admin"),
    "backupdata": ("🛡 Backup Data", "Admin placeholder.", "admin"),
    "loaddata": ("🛡 Load Data", "Admin placeholder.", "admin"),
    "maintenance": ("🛡 Maintenance", "Maintenance placeholder.", "admin"),
    "shutdown": ("🛡 Shutdown", "Shutdown placeholder.", "admin"),
    "restartmsg": ("🛡 RestartMsg", "Restart message placeholder.", "admin"),
}

def create_auto_command(cmd_name, title, desc, image_key):
    async def auto_cmd(ctx):
        ensure_player(ctx.author)
        await ctx.send(embed=basic_embed(title, desc, image_key))
    auto_cmd.__name__ = f"cmd_{cmd_name}"
    bot.command(name=cmd_name)(auto_cmd)

for cmd_name, (title, desc, image_key) in AUTO_COMMANDS.items():
    if bot.get_command(cmd_name) is None:
        create_auto_command(cmd_name, title, desc, image_key)

# =========================================================
# ERROR HANDLER
# =========================================================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Command-ын утга дутуу байна.")
        return
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Энэ command admin эрхтэй хүнд л ажиллана.")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("Утга буруу байна.")
        return
    await ctx.send(f"Алдаа гарлаа: {error}")

# =========================================================
# RUN
# =========================================================
if not TOKEN:
    print("TOKEN env var олдсонгүй.")
else:
    bot.run(TOKEN)
