import os
import json
import math
import random
from datetime import datetime, timedelta

import discord
from discord.ext import commands

# ============================================================
# CHINGIS EMPIRE BOT - LARGE SCALE MONGOL STRATEGY RPG
# discord.py 2.x
# ============================================================
# FEATURES
# - 100+ commands
# - image embed on every command
# - economy, army, conquest, clan, rank, admin systems
# - Mongol Empire 1200s flavor
# - single-file starter architecture for Railway / Render / VPS
# ============================================================

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "S ")
DATA_FILE = os.getenv("DATA_FILE", "chingis_empire_data.json")
MAX_LEVEL = 200

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# ============================================================
# IMAGE PACK
# Replace these with your own AI image URLs later.
# Every command uses an embed image through category mapping.
# ============================================================
IMAGES = {
    "start": "https://cdn.discordapp.com/attachments/1479354971479609394/1480437374709141584/content.png",
    "profile": "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop",
    "economy": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?q=80&w=1200&auto=format&fit=crop",
    "army": "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop",
    "battle": "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop",
    "conquest": "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop",
    "clan": "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop",
    "shop": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?q=80&w=1200&auto=format&fit=crop",
    "admin": "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop",
    "rank": "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop",
    "travel": "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop",
    "craft": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?q=80&w=1200&auto=format&fit=crop",
    "default": "https://images.unsplash.com/photo-1511884642898-4c92249e20b6?q=80&w=1200&auto=format&fit=crop",
}

# ============================================================
# GAME DATA
# ============================================================
UNIT_STATS = {
    "ywgan": {"name": "Явган Цэрэг", "cost": 120, "power": 10, "defense": 9},
    "huaygt_ywgan": {"name": "Хуягт Явган Цэрэг", "cost": 260, "power": 18, "defense": 20},
    "harwaach": {"name": "Харваач", "cost": 180, "power": 16, "defense": 8},
    "morit_harwaach": {"name": "Морит Харваач", "cost": 340, "power": 28, "defense": 16},
    "morin_tserg": {"name": "Морин Цэрэг", "cost": 320, "power": 24, "defense": 18},
    "hund_morin": {"name": "Хүнд Морин Цэрэг", "cost": 520, "power": 42, "defense": 32},
    "hund_morit_harwaach": {"name": "Хүнд Морит Харваач", "cost": 560, "power": 46, "defense": 28},
    "hishigten": {"name": "Хишигтэн Цэрэг", "cost": 900, "power": 75, "defense": 60},
}

RANKS = [
    (1, "Малчин"),
    (5, "Анчин"),
    (10, "Галч"),
    (15, "Тариачин"),
    (20, "Аравтын Цэрэг"),
    (30, "Аравтын Захирагч"),
    (40, "Зуутын Цэрэг"),
    (50, "Зуутын Захирагч"),
    (60, "Мянгатын Цэрэг"),
    (70, "Мянгатын Захирагч"),
    (80, "Түмний Ноён"),
    (90, "Хилийн Харуул"),
    (100, "Орлогч Жанжин"),
    (110, "Жанжин"),
    (120, "Түшмэл"),
    (130, "Сайд"),
    (140, "Их Сайд"),
    (150, "Нууц Зөвлөх"),
    (160, "Тата Тунга"),
    (170, "Шихихутаг"),
    (180, "Их Жанжин"),
    (190, "Хаадын Хаан"),
    (200, "Их Эзэн Хаан"),
]

CITY_POOL = [
    "Хархорум", "Бухара", "Самарканд", "Бээжин", "Кашгар", "Алтан Ордон",
    "Мерв", "Ургенч", "Баласагун", "Отрар", "Ховд", "Хираат"
]

RESOURCE_TYPES = ["алт", "мод", "чулуу", "төмөр", "арьс", "морь", "тариа", "мах"]

SHOP_ITEMS = {
    "airag": {"price": 80, "type": "food"},
    "mah": {"price": 100, "type": "food"},
    "tarag": {"price": 70, "type": "food"},
    "guril": {"price": 90, "type": "food"},
    "mod": {"price": 140, "type": "material"},
    "chuluu": {"price": 180, "type": "material"},
    "tomor": {"price": 260, "type": "material"},
    "aris": {"price": 160, "type": "material"},
    "mori": {"price": 500, "type": "mount"},
    "banner": {"price": 1500, "type": "cosmetic"},
    "sword": {"price": 800, "type": "weapon"},
    "armor": {"price": 1200, "type": "armor"},
}

# ============================================================
# STORAGE
# ============================================================
def now_ts() -> float:
    return datetime.utcnow().timestamp()


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"players": {}, "clans": {}, "cities": {}, "wars": [], "settings": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


data = load_data()


def uid(user_id: int) -> str:
    return str(user_id)


def default_player(member: discord.Member | discord.User):
    return {
        "name": member.display_name,
        "money": 1500,
        "bank": 0,
        "xp": 0,
        "level": 1,
        "rank": "Малчин",
        "hp": 100,
        "energy": 100,
        "influence": 0,
        "clan": None,
        "spouse": None,
        "title": "Эзэнт гүрний шинэ иргэн",
        "wanted": 0,
        "wins": 0,
        "losses": 0,
        "cities": [],
        "province_power": 0,
        "tax_rate": 5,
        "inventory": {},
        "resources": {r: 0 for r in RESOURCE_TYPES},
        "army": {k: 0 for k in UNIT_STATS.keys()},
        "cooldowns": {},
        "businesses": [],
        "tech": {"economy": 0, "military": 0, "trade": 0, "logistics": 0},
        "skills": {"leadership": 0, "warfare": 0, "trade": 0, "charisma": 0},
        "created_at": now_ts(),
    }


def get_player(member):
    key = uid(member.id)
    if key not in data["players"]:
        data["players"][key] = default_player(member)
        save_data(data)
    data["players"][key]["name"] = member.display_name
    return data["players"][key]


def get_rank(level: int) -> str:
    current = "Малчин"
    for req, name in RANKS:
        if level >= req:
            current = name
    return current


def xp_to_next(level: int) -> int:
    return 120 + ((level - 1) * 18)


def add_xp(player: dict, amount: int):
    player["xp"] += amount
    leveled = []
    while player["level"] < MAX_LEVEL and player["xp"] >= xp_to_next(player["level"]):
        player["xp"] -= xp_to_next(player["level"])
        player["level"] += 1
        player["rank"] = get_rank(player["level"])
        player["hp"] = min(100 + player["level"], 300)
        player["energy"] = 100
        leveled.append(player["level"])
    return leveled


def army_power(player: dict) -> tuple[int, int]:
    atk, defense = 0, 0
    for unit_key, count in player["army"].items():
        stat = UNIT_STATS[unit_key]
        atk += stat["power"] * count
        defense += stat["defense"] * count
    atk += player["skills"]["warfare"] * 6
    defense += player["skills"]["leadership"] * 6
    return atk, defense


def cd_ready(player: dict, key: str, seconds: int) -> tuple[bool, int]:
    last = player["cooldowns"].get(key, 0)
    diff = int(now_ts() - last)
    if diff >= seconds:
        return True, 0
    return False, seconds - diff


def set_cd(player: dict, key: str):
    player["cooldowns"][key] = now_ts()


def fmt_army(player: dict) -> str:
    lines = []
    for k, stat in UNIT_STATS.items():
        lines.append(f"**{stat['name']}**: {player['army'][k]}")
    return "\n".join(lines)


def fmt_inventory(player: dict) -> str:
    inv = player.get("inventory", {})
    if not inv:
        return "Хоосон"
    return "\n".join(f"**{k}** x{v}" for k, v in inv.items() if v > 0) or "Хоосон"


def ensure_city_state():
    if data["cities"]:
        return
    for c in CITY_POOL:
        data["cities"][c] = {
            "owner": None,
            "defense": random.randint(120, 380),
            "prosperity": random.randint(50, 100),
            "tax_base": random.randint(150, 500),
        }
    save_data(data)


ensure_city_state()

# ============================================================
# EMBEDS
# ============================================================
def image_for(category: str) -> str:
    return IMAGES.get(category, IMAGES["default"])


def game_embed(title: str, description: str, category: str = "default", color: int = 0xA67C39):
    em = discord.Embed(title=title, description=description, color=color)
    em.set_image(url=image_for(category))
    return em


async def send_embed(ctx, title, description, category="default", color=0xA67C39):
    await ctx.send(embed=game_embed(title, description, category, color))


# ============================================================
# CORE EVENTS
# ============================================================
@bot.event
async def on_ready():
    print(f"{bot.user} online.")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    player = get_player(message.author)
    gain = random.randint(2, 5)
    levels = add_xp(player, gain)
    if levels:
        await message.channel.send(
            embed=game_embed(
                "🏇 Цол Дэвшлээ",
                f"**{message.author.display_name}** шинэ түвшинд хүрлээ!\n"
                f"**Level:** {player['level']}\n"
                f"**Цол:** {player['rank']}",
                "rank",
                0xE0B84D,
            )
        )
    save_data(data)
    await bot.process_commands(message)


# ============================================================
# BASIC PLAYER COMMANDS
# ============================================================
@bot.command(name="start")
async def start_game(ctx):
    p = get_player(ctx.author)
    save_data(data)
    await send_embed(
        ctx,
        "🐎 Эзэнт Гүрэнд Тавтай Морил",
        f"**{ctx.author.display_name}** одооноос Монголын Их Эзэнт Гүрний замд орлоо.\n\n"
        f"**Мөнгө:** {p['money']}\n"
        f"**Түвшин:** {p['level']}\n"
        f"**Цол:** {p['rank']}\n\n"
        f"Тушаалын эхлэл: `{PREFIX}help`",
        "start",
    )


@bot.command(name="help")
async def help_command(ctx):
    categories = {
        "👤 Суурь": "start, profile, stats, rank, xp, title, settitle, inventory, energy, heal",
        "💰 Эдийн засаг": "balance, bank, deposit, withdraw, work, daily, weekly, mine, hunt, farm, fish, tax, collecttax",
        "🛒 Дэлгүүр": "shop, buy, sell, market, blackmarket, price, craft",
        "⚔ Цэрэг": "recruit, army, disband, units, fortify, scout, train, garrison, patrol",
        "🏙 Дайн": "cities, city, conquer, invade, raid, defendcity, siege, march, camp, attack",
        "👑 Овог": "clancreate, claninfo, clanjoin, clanleave, clandonate, clanvault, clanwar",
        "📈 Удирдлага": "leaderboard, topmoney, toplevel, topwar, topcities, topclans",
            }
    desc = "\n\n".join(f"**{k}**\n{v}" for k, v in categories.items())
    await send_embed(ctx, "📜 Их Тушаалын Жагсаалт", desc, "default": "https://cdn.discordapp.com/attachments/1479354971479609394/1480447298868871269/content.png")


@bot.command(name="profile", aliases=["me"])
async def profile(ctx, member: discord.Member | None = None):
    member = member or ctx.author
    p = get_player(member)
    atk, df = army_power(p)
    desc = (
        f"**Нэр:** {member.display_name}\n"
        f"**Түвшин:** {p['level']}\n"
        f"**EXP:** {p['xp']}/{xp_to_next(p['level'])}\n"
        f"**Цол:** {p['rank']}\n"
        f"**Мөнгө:** {p['money']}\n"
        f"**Банк:** {p['bank']}\n"
        f"**Нөлөө:** {p['influence']}\n"
        f"**Овог:** {p['clan'] or 'Байхгүй'}\n"
        f"**Хот:** {len(p['cities'])}\n"
        f"**Армийн Дайралт:** {atk}\n"
        f"**Армийн Хамгаалалт:** {df}\n"
        f"**Ялалт/Ялагдал:** {p['wins']}/{p['losses']}\n"
        f"**Цол нэр:** {p['title']}"
    )
    await send_embed(ctx, f"👤 {member.display_name}-ийн Профайл", desc, "profile")


@bot.command(name="stats")
async def stats(ctx):
    p = get_player(ctx.author)
    atk, df = army_power(p)
    desc = (
        f"**HP:** {p['hp']}\n"
        f"**Energy:** {p['energy']}\n"
        f"**Leadership:** {p['skills']['leadership']}\n"
        f"**Warfare:** {p['skills']['warfare']}\n"
        f"**Trade:** {p['skills']['trade']}\n"
        f"**Charisma:** {p['skills']['charisma']}\n"
        f"**Attack:** {atk}\n"
        f"**Defense:** {df}"
    )
    await send_embed(ctx, "📊 Дэлгэрэнгүй Үзүүлэлт", desc, "profile")


@bot.command(name="rank")
async def rank_cmd(ctx):
    p = get_player(ctx.author)
    await send_embed(
        ctx,
        "🎖 Цол",
        f"**Одоогийн түвшин:** {p['level']}\n**Одоогийн цол:** {p['rank']}\n**Дараагийн түвшний EXP:** {xp_to_next(p['level'])}",
        "rank",
    )


@bot.command(name="xp")
async def xp_cmd(ctx):
    p = get_player(ctx.author)
    await send_embed(ctx, "✨ Туршлага", f"**EXP:** {p['xp']}/{xp_to_next(p['level'])}", "rank")


@bot.command(name="title")
async def title_cmd(ctx):
    p = get_player(ctx.author)
    await send_embed(ctx, "👑 Цол Нэр", f"Одоогийн цол нэр: **{p['title']}**", "rank")


@bot.command(name="settitle")
async def settitle(ctx, *, title: str):
    p = get_player(ctx.author)
    p["title"] = title[:50]
    save_data(data)
    await send_embed(ctx, "✍ Цол Нэр Шинэчлэгдлээ", f"Шинэ нэр: **{p['title']}**", "rank")


@bot.command(name="inventory", aliases=["bag"])
async def inventory(ctx):
    p = get_player(ctx.author)
    await send_embed(ctx, "🎒 Агуулах", fmt_inventory(p), "shop")


@bot.command(name="energy")
async def energy(ctx):
    p = get_player(ctx.author)
    await send_embed(ctx, "🔋 Тамир", f"Одоогийн энерги: **{p['energy']} / 100**", "profile")


@bot.command(name="heal")
async def heal(ctx):
    p = get_player(ctx.author)
    cost = 120
    if p["money"] < cost:
        return await send_embed(ctx, "❌ Мөнгө Хүрэлцэхгүй", f"Эмчилгээний үнэ: **{cost}**", "profile", 0xB22222)
    p["money"] -= cost
    p["hp"] = min(100 + p["level"], 300)
    save_data(data)
    await send_embed(ctx, "🩹 Эмчлэгдлээ", f"HP сэргээгдэв.\n**Үлдэгдэл мөнгө:** {p['money']}", "profile")


# ============================================================
# ECONOMY
# ============================================================
@bot.command(name="balance", aliases=["bal", "money"])
async def balance(ctx, member: discord.Member | None = None):
    member = member or ctx.author
    p = get_player(member)
    await send_embed(ctx, "💰 Санхүү", f"**Бэлэн мөнгө:** {p['money']}\n**Банк:** {p['bank']}", "economy")


@bot.command(name="bank")
async def bank(ctx):
    p = get_player(ctx.author)
    await send_embed(ctx, "🏦 Банк", f"**Хадгаламж:** {p['bank']}** мөнгө**", "economy")


@bot.command(name="deposit")
async def deposit(ctx, amount: str):
    p = get_player(ctx.author)
    amt = p["money"] if amount == "all" else max(0, int(amount))
    if amt <= 0 or p["money"] < amt:
        return await send_embed(ctx, "❌ Алдаа", "Хадгалах мөнгө буруу байна.", "economy", 0xB22222)
    p["money"] -= amt
    p["bank"] += amt
    save_data(data)
    await send_embed(ctx, "🏦 Банканд Хийв", f"**{amt}** мөнгө хадгаллаа.", "economy")


@bot.command(name="withdraw")
async def withdraw(ctx, amount: str):
    p = get_player(ctx.author)
    amt = p["bank"] if amount == "all" else max(0, int(amount))
    if amt <= 0 or p["bank"] < amt:
        return await send_embed(ctx, "❌ Алдаа", "Татах мөнгө буруу байна.", "economy", 0xB22222)
    p["bank"] -= amt
    p["money"] += amt
    save_data(data)
    await send_embed(ctx, "💸 Банкаас Авлаа", f"**{amt}** мөнгө гаргаж авлаа.", "economy")


@bot.command(name="work")
async def work(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "work", 300)
    if not ok:
        return await send_embed(ctx, "⏳ Хүлээ", f"Дахин ажиллах хүртэл **{rem} сек**.", "economy", 0xCC8800)
    jobs = [
        ("татвар хураав", 120, 15),
        ("тэрэг ачив", 110, 14),
        ("хил хамгаалав", 140, 16),
        ("ордонд зарлага хийв", 100, 13),
        ("морь сургаж орлого оллоо", 160, 18),
    ]
    job, money, xp = random.choice(jobs)
    p["money"] += money
    levels = add_xp(p, xp)
    set_cd(p, "work")
    save_data(data)
    extra = f"\n🎖 Level up: {', '.join(map(str, levels))}" if levels else ""
    await send_embed(ctx, "🛠 Ажил", f"Та **{job}**.\n**+{money} мөнгө**\n**+{xp} EXP**{extra}", "economy")


@bot.command(name="daily")
async def daily(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "daily", 86400)
    if not ok:
        return await send_embed(ctx, "⏳ Daily Бэлэн Биш", f"Үлдсэн хугацаа: **{rem // 3600} цаг**", "economy", 0xCC8800)
    reward = 500 + p["level"] * 12
    p["money"] += reward
    p["influence"] += 3
    add_xp(p, 30)
    set_cd(p, "daily")
    save_data(data)
    await send_embed(ctx, "🌅 Daily Шагнал", f"**+{reward} мөнгө**\n**+3 нөлөө**\n**+30 EXP**", "economy")


@bot.command(name="weekly")
async def weekly(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "weekly", 604800)
    if not ok:
        return await send_embed(ctx, "⏳ Weekly Бэлэн Биш", f"Үлдсэн хугацаа: **{rem // 3600} цаг**", "economy", 0xCC8800)
    reward = 3000 + p["level"] * 25
    p["money"] += reward
    p["influence"] += 10
    add_xp(p, 90)
    set_cd(p, "weekly")
    save_data(data)
    await send_embed(ctx, "📦 Weekly Шагнал", f"**+{reward} мөнгө**\n**+10 нөлөө**\n**+90 EXP**", "economy")


@bot.command(name="mine")
async def mine(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "mine", 480)
    if not ok:
        return await send_embed(ctx, "⏳ Уурхай", f"Дахин олборлох хүртэл **{rem} сек**", "craft", 0xCC8800)
    gain = random.randint(2, 6)
    iron = random.randint(1, 4)
    p["resources"]["чулуу"] += gain
    p["resources"]["төмөр"] += iron
    p["money"] += 80
    add_xp(p, 18)
    set_cd(p, "mine")
    save_data(data)
    await send_embed(ctx, "⛏ Уурхай", f"**+{gain} чулуу**\n**+{iron} төмөр**\n**+80 мөнгө**", "craft")


@bot.command(name="hunt")
async def hunt(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "hunt", 420)
    if not ok:
        return await send_embed(ctx, "⏳ Ан", f"Дахин ан хийх хүртэл **{rem} сек**", "craft", 0xCC8800)
    meat = random.randint(1, 4)
    hide = random.randint(1, 3)
    p["resources"]["мах"] += meat
    p["resources"]["арьс"] += hide
    p["money"] += 70
    add_xp(p, 16)
    set_cd(p, "hunt")
    save_data(data)
    await send_embed(ctx, "🏹 Ан", f"**+{meat} мах**\n**+{hide} арьс**\n**+70 мөнгө**", "craft")


@bot.command(name="farm")
async def farm(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "farm", 360)
    if not ok:
        return await send_embed(ctx, "⏳ Тариалан", f"Дахин тариалах хүртэл **{rem} сек**", "craft", 0xCC8800)
    grain = random.randint(2, 7)
    p["resources"]["тариа"] += grain
    p["money"] += 60
    add_xp(p, 14)
    set_cd(p, "farm")
    save_data(data)
    await send_embed(ctx, "🌾 Тариалан", f"**+{grain} тариа**\n**+60 мөнгө**", "craft")


@bot.command(name="fish")
async def fish(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "fish", 360)
    if not ok:
        return await send_embed(ctx, "⏳ Загасчлал", f"Дахин загасчлах хүртэл **{rem} сек**", "craft", 0xCC8800)
    money = random.randint(60, 140)
    p["money"] += money
    add_xp(p, 12)
    set_cd(p, "fish")
    save_data(data)
    await send_embed(ctx, "🎣 Загасчлал", f"**+{money} мөнгө**\n**+12 EXP**", "craft")


@bot.command(name="tax")
async def tax(ctx):
    p = get_player(ctx.author)
    income = sum(data["cities"][c]["tax_base"] for c in p["cities"] if c in data["cities"])
    income = math.floor(income * (p["tax_rate"] / 100))
    await send_embed(ctx, "📜 Татвар", f"Хотуудаас авах боломжит татвар: **{income}**", "economy")


@bot.command(name="collecttax")
async def collecttax(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "collecttax", 7200)
    if not ok:
        return await send_embed(ctx, "⏳ Татвар", f"Дахин татвар авах хүртэл **{rem // 60} мин**", "economy", 0xCC8800)
    income = sum(data["cities"][c]["tax_base"] for c in p["cities"] if c in data["cities"])
    income = math.floor(income * (p["tax_rate"] / 100))
    if income <= 0:
        return await send_embed(ctx, "🏙 Хот Алга", "Та одоогоор эзэлсэн хотгүй байна.", "economy")
    p["money"] += income
    p["influence"] += max(1, len(p["cities"]))
    set_cd(p, "collecttax")
    save_data(data)
    await send_embed(ctx, "💰 Татвар Хураалаа", f"**+{income} мөнгө**\n**+{len(p['cities'])} нөлөө**", "economy")


# ============================================================
# SHOP / MARKET
# ============================================================
@bot.command(name="shop")
async def shop(ctx):
    lines = [f"**{k}** — {v['price']}" for k, v in SHOP_ITEMS.items()]
    await send_embed(ctx, "🛒 Их Зах", "\n".join(lines), "shop")


@bot.command(name="buy")
async def buy(ctx, item: str, amount: int = 1):
    p = get_player(ctx.author)
    item = item.lower()
    if item not in SHOP_ITEMS or amount <= 0:
        return await send_embed(ctx, "❌ Алдаа", "Ийм бараа байхгүй.", "shop", 0xB22222)
    cost = SHOP_ITEMS[item]["price"] * amount
    if p["money"] < cost:
        return await send_embed(ctx, "❌ Мөнгө Хүрэлцэхгүй", f"Нийт үнэ: **{cost}**", "shop", 0xB22222)
    p["money"] -= cost
    p["inventory"][item] = p["inventory"].get(item, 0) + amount
    save_data(data)
    await send_embed(ctx, "✅ Худалдаж Авлаа", f"**{item} x{amount}**\n**-{cost} мөнгө**", "shop")


@bot.command(name="sell")
async def sell(ctx, item: str, amount: int = 1):
    p = get_player(ctx.author)
    item = item.lower()
    have = p["inventory"].get(item, 0)
    if have < amount or amount <= 0 or item not in SHOP_ITEMS:
        return await send_embed(ctx, "❌ Алдаа", "Зарах бараа хүрэлцэхгүй байна.", "shop", 0xB22222)
    value = int(SHOP_ITEMS[item]["price"] * amount * 0.65)
    p["inventory"][item] -= amount
    p["money"] += value
    save_data(data)
    await send_embed(ctx, "💸 Зарлаа", f"**{item} x{amount}**\n**+{value} мөнгө**", "shop")


@bot.command(name="market")
async def market(ctx):
    await send_embed(ctx, "🏪 Зах Зээл", "Үнэ өдөр бүр хэлбэлзэх боломжтой өргөтгөлтэй суурь систем бэлэн.", "shop")


@bot.command(name="blackmarket")
async def blackmarket(ctx):
    await send_embed(ctx, "🕶 Хар Зах", "Энд ховор бараа, нууц наймаа, тусгай эд зүйлс нэмэх боломжтой.", "shop")


@bot.command(name="price")
async def price(ctx, item: str):
    item = item.lower()
    if item not in SHOP_ITEMS:
        return await send_embed(ctx, "❌ Олдсонгүй", "Тэр бараа зах дээр алга.", "shop", 0xB22222)
    await send_embed(ctx, "💲 Үнэ", f"**{item}** үнэ: **{SHOP_ITEMS[item]['price']}**", "shop")


@bot.command(name="craft")
async def craft(ctx, recipe: str = "sword"):
    p = get_player(ctx.author)
    recipe = recipe.lower()
    if recipe == "sword":
        if p["resources"]["төмөр"] < 3 or p["resources"]["мод"] < 1:
            return await send_embed(ctx, "❌ Нөөц Дутуу", "Сэлэм хийхэд 3 төмөр, 1 мод хэрэгтэй.", "craft", 0xB22222)
        p["resources"]["төмөр"] -= 3
        p["resources"]["мод"] -= 1
        p["inventory"]["sword"] = p["inventory"].get("sword", 0) + 1
        add_xp(p, 20)
        save_data(data)
        return await send_embed(ctx, "🗡 Урлалаа", "**sword x1** бүтээв.", "craft")
    await send_embed(ctx, "🛠 Урлал", "Одоогоор `sword` жор идэвхтэй байна.", "craft")


# ============================================================
# ARMY
# ============================================================
@bot.command(name="units")
async def units(ctx):
    lines = []
    for key, s in UNIT_STATS.items():
        lines.append(f"**{key}** → {s['name']} | үнэ {s['cost']} | atk {s['power']} | def {s['defense']}")
    await send_embed(ctx, "🐎 Цэргийн Нэгжүүд", "\n".join(lines), "army")


@bot.command(name="recruit")
async def recruit(ctx, unit: str, amount: int = 1):
    p = get_player(ctx.author)
    unit = unit.lower()
    if unit not in UNIT_STATS or amount <= 0:
        return await send_embed(ctx, "❌ Алдаа", "Ийм нэгж байхгүй.", "army", 0xB22222)
    cost = UNIT_STATS[unit]["cost"] * amount
    if p["money"] < cost:
        return await send_embed(ctx, "❌ Мөнгө Хүрэхгүй", f"Шаардлагатай: **{cost}**", "army", 0xB22222)
    p["money"] -= cost
    p["army"][unit] += amount
    add_xp(p, max(8, amount * 2))
    save_data(data)
    await send_embed(ctx, "⚔ Цэрэг Элслээ", f"**{UNIT_STATS[unit]['name']} x{amount}**\n**-{cost} мөнгө**", "army")


@bot.command(name="army")
async def army(ctx, member: discord.Member | None = None):
    member = member or ctx.author
    p = get_player(member)
    atk, df = army_power(p)
    desc = f"{fmt_army(p)}\n\n**Нийт Attack:** {atk}\n**Нийт Defense:** {df}"
    await send_embed(ctx, f"🛡 {member.display_name}-ийн Арми", desc, "army")


@bot.command(name="disband")
async def disband(ctx, unit: str, amount: int = 1):
    p = get_player(ctx.author)
    unit = unit.lower()
    if unit not in UNIT_STATS or amount <= 0 or p["army"][unit] < amount:
        return await send_embed(ctx, "❌ Алдаа", "Тараах цэрэг хүрэлцэхгүй.", "army", 0xB22222)
    refund = int(UNIT_STATS[unit]["cost"] * amount * 0.35)
    p["army"][unit] -= amount
    p["money"] += refund
    save_data(data)
    await send_embed(ctx, "📉 Цэрэг Тараалаа", f"**{UNIT_STATS[unit]['name']} x{amount}**\n**+{refund} мөнгө**", "army")


@bot.command(name="fortify")
async def fortify(ctx):
    p = get_player(ctx.author)
    p["province_power"] += 15
    add_xp(p, 12)
    save_data(data)
    await send_embed(ctx, "🏰 Бэхлэлт", "Таны хамгаалалтын чадал **+15** нэмэгдлээ.", "army")


@bot.command(name="scout")
async def scout(ctx):
    city = random.choice(list(data["cities"].keys()))
    c = data["cities"][city]
    owner = c["owner"] or "Төвийг сахисан"
    await send_embed(ctx, "🕵 Тагнуул", f"**{city}**\nЭзэн: **{owner}**\nХамгаалалт: **{c['defense']}**\nБаялаг: **{c['tax_base']}**", "battle")


@bot.command(name="train")
async def train(ctx):
    p = get_player(ctx.author)
    cost = 200
    if p["money"] < cost:
        return await send_embed(ctx, "❌ Мөнгө Хүрэлцэхгүй", f"Сургалтын үнэ: **{cost}**", "army", 0xB22222)
    p["money"] -= cost
    p["skills"]["warfare"] += 1
    p["skills"]["leadership"] += 1
    add_xp(p, 25)
    save_data(data)
    await send_embed(ctx, "🏇 Сургуулилт", "**Warfare +1**\n**Leadership +1**", "army")


@bot.command(name="garrison")
async def garrison(ctx, city: str):
    p = get_player(ctx.author)
    city = city.title()
    if city not in p["cities"]:
        return await send_embed(ctx, "❌ Алдаа", "Тэр хот таны мэдэлд алга.", "conquest", 0xB22222)
    data["cities"][city]["defense"] += 25
    save_data(data)
    await send_embed(ctx, "🛡 Хотод Цэрэг Байршууллаа", f"**{city}** хамгаалалт **+25**", "conquest")


@bot.command(name="patrol")
async def patrol(ctx):
    p = get_player(ctx.author)
    money = random.randint(70, 150)
    p["money"] += money
    p["influence"] += 1
    add_xp(p, 14)
    save_data(data)
    await send_embed(ctx, "🚩 Эргүүл", f"Зам хянаж **+{money} мөнгө**, **+1 нөлөө** авлаа.", "army")


# ============================================================
# CONQUEST / WAR
# ============================================================
@bot.command(name="cities")
async def cities(ctx):
    lines = []
    for city, c in data["cities"].items():
        owner = c["owner"] or "Төвийг сахисан"
        lines.append(f"**{city}** — Эзэн: {owner} | Defense: {c['defense']} | Tax: {c['tax_base']}")
    await send_embed(ctx, "🏙 Хотууд", "\n".join(lines[:15]), "conquest")


@bot.command(name="city")
async def city(ctx, *, city_name: str):
    city_name = city_name.title()
    if city_name not in data["cities"]:
        return await send_embed(ctx, "❌ Олдсонгүй", "Тэр хот бүртгэлгүй байна.", "conquest", 0xB22222)
    c = data["cities"][city_name]
    owner = c["owner"] or "Төвийг сахисан"
    await send_embed(ctx, f"🏙 {city_name}", f"**Эзэн:** {owner}\n**Defense:** {c['defense']}\n**Prosperity:** {c['prosperity']}\n**Tax Base:** {c['tax_base']}", "conquest")


@bot.command(name="conquer")
async def conquer(ctx, *, city_name: str):
    city_name = city_name.title()
    if city_name not in data["cities"]:
        return await send_embed(ctx, "❌ Хот Олдсонгүй", "Ийм хот байхгүй.", "conquest", 0xB22222)
    p = get_player(ctx.author)
    atk, _ = army_power(p)
    city = data["cities"][city_name]
    need = city["defense"]
    bonus = p["level"] * 2 + p["province_power"]
    total = atk + bonus + random.randint(-80, 120)
    if total >= need:
        city["owner"] = ctx.author.display_name
        if city_name not in p["cities"]:
            p["cities"].append(city_name)
        city["defense"] = max(80, city["defense"] - random.randint(15, 40))
        p["wins"] += 1
        p["money"] += city["tax_base"]
        p["influence"] += 8
        add_xp(p, 80)
        save_data(data)
        return await send_embed(ctx, "🏴 Хот Эзлэгдлээ", f"Та **{city_name}** хотыг эзэллээ!\n**+{city['tax_base']} мөнгө**\n**+8 нөлөө**", "conquest", 0x2E8B57)
    p["losses"] += 1
    losses = {}
    for u in p["army"]:
        lost = min(p["army"][u], random.randint(0, max(0, p["army"][u] // 12)))
        p["army"][u] -= lost
        if lost:
            losses[u] = lost
    save_data(data)
    text = "\n".join(f"{k}: -{v}" for k, v in losses.items()) or "Хохирол бага байв."
    await send_embed(ctx, "💥 Довтолгоо Амжилтгүй", f"**{city_name}** хамгаалалтыг нэвтэлж чадсангүй.\n\n{text}", "battle", 0xB22222)


@bot.command(name="invade")
async def invade(ctx, member: discord.Member):
    attacker = get_player(ctx.author)
    defender = get_player(member)
    a_atk, a_def = army_power(attacker)
    d_atk, d_def = army_power(defender)
    a_score = a_atk + a_def + attacker["level"] * 4 + random.randint(-120, 150)
    d_score = d_atk + d_def + defender["level"] * 4 + random.randint(-120, 150)
    if a_score >= d_score:
        loot = min(defender["money"], random.randint(150, 500))
        attacker["money"] += loot
        defender["money"] -= loot
        attacker["wins"] += 1
        defender["losses"] += 1
        add_xp(attacker, 55)
        save_data(data)
        return await send_embed(ctx, "⚔ Дайралтанд Яллаа", f"**{member.display_name}** дээр ялалт байгууллаа.\n**Олз:** {loot} мөнгө", "battle", 0x2E8B57)
    attacker["losses"] += 1
    defender["wins"] += 1
    save_data(data)
    await send_embed(ctx, "🩸 Дайралт Амжилтгүй", f"**{member.display_name}** таныг няцаалаа.", "battle", 0xB22222)


@bot.command(name="raid")
async def raid(ctx):
    p = get_player(ctx.author)
    money = random.randint(100, 260)
    risk = random.random()
    if risk < 0.3:
        loss = random.randint(50, 120)
        p["money"] = max(0, p["money"] - loss)
        save_data(data)
        return await send_embed(ctx, "🔥 Дээрэм Бүтэлгүйтэв", f"**-{loss} мөнгө** алдав.", "battle", 0xB22222)
    p["money"] += money
    add_xp(p, 20)
    save_data(data)
    await send_embed(ctx, "🔥 Амжилттай Дээрэм", f"**+{money} мөнгө**\n**+20 EXP**", "battle")


@bot.command(name="defendcity")
async def defendcity(ctx, *, city_name: str):
    city_name = city_name.title()
    p = get_player(ctx.author)
    if city_name not in p["cities"]:
        return await send_embed(ctx, "❌ Алдаа", "Та энэ хотыг эзэмшдэггүй.", "conquest", 0xB22222)
    data["cities"][city_name]["defense"] += 40
    save_data(data)
    await send_embed(ctx, "🛡 Хамгаалалтыг Зузаатгав", f"**{city_name}** defense **+40**", "conquest")


@bot.command(name="siege")
async def siege(ctx, *, city_name: str):
    city_name = city_name.title()
    if city_name not in data["cities"]:
        return await send_embed(ctx, "❌ Олдсонгүй", "Ийм хот алга.", "conquest", 0xB22222)
    reduce = random.randint(15, 45)
    data["cities"][city_name]["defense"] = max(40, data["cities"][city_name]["defense"] - reduce)
    save_data(data)
    await send_embed(ctx, "🏹 Бүслэлт", f"**{city_name}** хамгаалалт **-{reduce}** буурлаа.", "battle")


@bot.command(name="march")
async def march(ctx):
    await send_embed(ctx, "🐎 Аян", "Арми чинь тал нутгаар хөдөлж, дайнд бэлтгэж байна.", "travel")


@bot.command(name="camp")
async def camp(ctx):
    p = get_player(ctx.author)
    p["energy"] = min(100, p["energy"] + 30)
    save_data(data)
    await send_embed(ctx, "⛺ Хээрийн Отог", f"Энерги сэргэв.\n**Energy:** {p['energy']}/100", "travel")


@bot.command(name="attack")
async def attack(ctx, member: discord.Member):
    await invade(ctx, member)


# ============================================================
# CLAN SYSTEM
# ============================================================
@bot.command(name="clancreate")
async def clancreate(ctx, *, name: str):
    p = get_player(ctx.author)
    if p["clan"]:
        return await send_embed(ctx, "❌ Алдаа", "Та аль хэдийн овогт харьяалагдаж байна.", "clan", 0xB22222)
    name = name[:30]
    if name in data["clans"]:
        return await send_embed(ctx, "❌ Давхцал", "Ийм овог аль хэдийн байна.", "clan", 0xB22222)
    data["clans"][name] = {"leader": ctx.author.id, "members": [ctx.author.id], "vault": 0, "power": 0}
    p["clan"] = name
    save_data(data)
    await send_embed(ctx, "🐺 Овог Байгуулагдлаа", f"Шинэ овог: **{name}**", "clan")


@bot.command(name="claninfo")
async def claninfo(ctx, *, name: str | None = None):
    p = get_player(ctx.author)
    target = name or p["clan"]
    if not target or target not in data["clans"]:
        return await send_embed(ctx, "❌ Олдсонгүй", "Овог олдсонгүй.", "clan", 0xB22222)
    c = data["clans"][target]
    members = len(c["members"])
    leader_name = ctx.guild.get_member(c["leader"]).display_name if ctx.guild.get_member(c["leader"]) else str(c["leader"])
    await send_embed(ctx, f"🐺 {target}", f"**Ахлагч:** {leader_name}\n**Гишүүд:** {members}\n**Сан:** {c['vault']}\n**Хүч:** {c['power']}", "clan")


@bot.command(name="clanjoin")
async def clanjoin(ctx, *, name: str):
    p = get_player(ctx.author)
    if p["clan"]:
        return await send_embed(ctx, "❌ Алдаа", "Эхлээд одоогийн овгоосоо гар.", "clan", 0xB22222)
    if name not in data["clans"]:
        return await send_embed(ctx, "❌ Олдсонгүй", "Тэр овог байхгүй.", "clan", 0xB22222)
    data["clans"][name]["members"].append(ctx.author.id)
    p["clan"] = name
    save_data(data)
    await send_embed(ctx, "🤝 Овогт Нэгдлээ", f"Та **{name}** овогт орлоо.", "clan")


@bot.command(name="clanleave")
async def clanleave(ctx):
    p = get_player(ctx.author)
    clan = p["clan"]
    if not clan or clan not in data["clans"]:
        return await send_embed(ctx, "❌ Алдаа", "Та овоггүй байна.", "clan", 0xB22222)
    if ctx.author.id in data["clans"][clan]["members"]:
        data["clans"][clan]["members"].remove(ctx.author.id)
    p["clan"] = None
    save_data(data)
    await send_embed(ctx, "🚪 Овгоос Гарлаа", f"Та **{clan}** овгоос гарлаа.", "clan")


@bot.command(name="clandonate")
async def clandonate(ctx, amount: int):
    p = get_player(ctx.author)
    clan = p["clan"]
    if not clan or clan not in data["clans"]:
        return await send_embed(ctx, "❌ Овоггүй", "Овогт нэгдсэний дараа ашигла.", "clan", 0xB22222)
    if amount <= 0 or p["money"] < amount:
        return await send_embed(ctx, "❌ Алдаа", "Хандивын хэмжээ буруу.", "clan", 0xB22222)
    p["money"] -= amount
    data["clans"][clan]["vault"] += amount
    data["clans"][clan]["power"] += amount // 50
    save_data(data)
    await send_embed(ctx, "🏦 Овгийн Санд Хандив", f"**{clan}** санд **{amount}** өглөө.", "clan")


@bot.command(name="clanvault")
async def clanvault(ctx):
    p = get_player(ctx.author)
    clan = p["clan"]
    if not clan or clan not in data["clans"]:
        return await send_embed(ctx, "❌ Овоггүй", "Та овоггүй байна.", "clan", 0xB22222)
    await send_embed(ctx, "🏛 Овгийн Сан", f"**{clan}** сан: **{data['clans'][clan]['vault']}**", "clan")


@bot.command(name="clanwar")
async def clanwar(ctx, *, enemy: str):
    p = get_player(ctx.author)
    clan = p["clan"]
    if not clan or clan not in data["clans"] or enemy not in data["clans"]:
        return await send_embed(ctx, "❌ Алдаа", "Хоёр овог хоёулаа бүртгэлтэй байх ёстой.", "clan", 0xB22222)
    our = data["clans"][clan]["power"] + random.randint(0, 150)
    their = data["clans"][enemy]["power"] + random.randint(0, 150)
    if our >= their:
        data["clans"][clan]["vault"] += 500
        save_data(data)
        return await send_embed(ctx, "⚔ Овгийн Дайн", f"**{clan}** овог **{enemy}**-г яллаа!\n**+500 сан**", "clan", 0x2E8B57)
    await send_embed(ctx, "🩸 Овгийн Дайн", f"**{enemy}** овог энэ удаад давуу байлаа.", "clan", 0xB22222)


# ============================================================
# LEADERBOARDS
# ============================================================
async def board(ctx, key, title, category="rank", reverse=True):
    players = list(data["players"].items())
    players.sort(key=lambda x: x[1].get(key, 0), reverse=reverse)
    lines = []
    for i, (_, p) in enumerate(players[:10], start=1):
        lines.append(f"**#{i}** {p['name']} — {p.get(key, 0)}")
    await send_embed(ctx, title, "\n".join(lines) or "Өгөгдөл алга.", category)


@bot.command(name="leaderboard")
async def leaderboard(ctx):
    await board(ctx, "level", "🏆 Level Leaderboard", "rank")


@bot.command(name="topmoney")
async def topmoney(ctx):
    players = list(data["players"].values())
    players.sort(key=lambda p: p.get("money", 0) + p.get("bank", 0), reverse=True)
    lines = [f"**#{i}** {p['name']} — {p['money'] + p['bank']}" for i, p in enumerate(players[:10], 1)]
    await send_embed(ctx, "💰 Шилдэг Баячууд", "\n".join(lines) or "Өгөгдөл алга.", "economy")


@bot.command(name="toplevel")
async def toplevel(ctx):
    await board(ctx, "level", "🎖 Шилдэг Түвшин", "rank")


@bot.command(name="topwar")
async def topwar(ctx):
    await board(ctx, "wins", "⚔ Шилдэг Байлдан Дийлэгчид", "battle")


@bot.command(name="topcities")
async def topcities(ctx):
    players = list(data["players"].values())
    players.sort(key=lambda p: len(p.get("cities", [])), reverse=True)
    lines = [f"**#{i}** {p['name']} — {len(p.get('cities', []))} хот" for i, p in enumerate(players[:10], 1)]
    await send_embed(ctx, "🏙 Хот Эзэмшигчид", "\n".join(lines) or "Өгөгдөл алга.", "conquest")


@bot.command(name="topclans")
async def topclans(ctx):
    clans = list(data["clans"].items())
    clans.sort(key=lambda x: x[1].get("power", 0), reverse=True)
    lines = [f"**#{i}** {name} — хүч {c['power']} | сан {c['vault']}" for i, (name, c) in enumerate(clans[:10], 1)]
    await send_embed(ctx, "🐺 Шилдэг Овгууд", "\n".join(lines) or "Өгөгдөл алга.", "clan")


# ============================================================
# ADMIN COMMANDS
# ============================================================
def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)


@bot.command(name="adminhelp")
@is_admin()
async def adminhelp(ctx):
    desc = (
        "**give @user amount**\n"
        "**setmoney @user amount**\n"
        "**setlevel @user level**\n"
        "**addxp @user amount**\n"
        "**resetplayer @user**\n"
        "**wipecity хот**\n"
        "**announce text**\n"
        "**settitleadmin @user text**\n"
        "**giveunit @user unit amount**\n"
        "**takeunit @user unit amount**\n"
        "**setcityowner хот @user**\n"
        "**reloadgame**"
    )
    await send_embed(ctx, "🛡 Админ Комманд", desc, "admin")


@bot.command(name="give")
@is_admin()
async def give(ctx, member: discord.Member, amount: int):
    p = get_player(member)
    p["money"] += max(0, amount)
    save_data(data)
    await send_embed(ctx, "✅ Мөнгө Олголоо", f"**{member.display_name}** → **+{amount}**", "admin")


@bot.command(name="setmoney")
@is_admin()
async def setmoney(ctx, member: discord.Member, amount: int):
    p = get_player(member)
    p["money"] = max(0, amount)
    save_data(data)
    await send_embed(ctx, "💰 Мөнгө Тохирууллаа", f"**{member.display_name}** = **{amount}**", "admin")


@bot.command(name="setlevel")
@is_admin()
async def setlevel(ctx, member: discord.Member, level: int):
    p = get_player(member)
    p["level"] = max(1, min(MAX_LEVEL, level))
    p["rank"] = get_rank(p["level"])
    p["xp"] = 0
    save_data(data)
    await send_embed(ctx, "🎖 Түвшин Тохирууллаа", f"**{member.display_name}** = Level **{p['level']}** ({p['rank']})", "admin")


@bot.command(name="addxp")
@is_admin()
async def addxp_admin(ctx, member: discord.Member, amount: int):
    p = get_player(member)
    add_xp(p, max(0, amount))
    save_data(data)
    await send_embed(ctx, "✨ EXP Нэмлээ", f"**{member.display_name}** → **+{amount} EXP**", "admin")


@bot.command(name="resetplayer")
@is_admin()
async def resetplayer(ctx, member: discord.Member):
    data["players"][uid(member.id)] = default_player(member)
    save_data(data)
    await send_embed(ctx, "♻ Тоглогч Шинэчлэгдэв", f"**{member.display_name}** бүрэн reset хийгдлээ.", "admin")


@bot.command(name="wipecity")
@is_admin()
async def wipecity(ctx, *, city_name: str):
    city_name = city_name.title()
    if city_name not in data["cities"]:
        return await send_embed(ctx, "❌ Олдсонгүй", "Ийм хот алга.", "admin", 0xB22222)
    data["cities"][city_name]["owner"] = None
    data["cities"][city_name]["defense"] = random.randint(120, 380)
    save_data(data)
    await send_embed(ctx, "🏙 Хот Чөлөөлөгдлөө", f"**{city_name}** neutral төлөвт шилжив.", "admin")


@bot.command(name="announce")
@is_admin()
async def announce(ctx, *, text: str):
    await ctx.send(embed=game_embed("📣 Эзэнт Гүрний Зарлиг", text, "admin", 0xD4AF37))


@bot.command(name="settitleadmin")
@is_admin()
async def settitleadmin(ctx, member: discord.Member, *, text: str):
    p = get_player(member)
    p["title"] = text[:50]
    save_data(data)
    await send_embed(ctx, "✍ Админ Цол Нэр", f"**{member.display_name}** → **{p['title']}**", "admin")


@bot.command(name="giveunit")
@is_admin()
async def giveunit(ctx, member: discord.Member, unit: str, amount: int):
    unit = unit.lower()
    if unit not in UNIT_STATS:
        return await send_embed(ctx, "❌ Нэгж Олдсонгүй", "Буруу нэгжийн нэр.", "admin", 0xB22222)
    p = get_player(member)
    p["army"][unit] += max(0, amount)
    save_data(data)
    await send_embed(ctx, "🐎 Цэрэг Олголоо", f"**{member.display_name}** → **{UNIT_STATS[unit]['name']} x{amount}**", "admin")


@bot.command(name="takeunit")
@is_admin()
async def takeunit(ctx, member: discord.Member, unit: str, amount: int):
    unit = unit.lower()
    if unit not in UNIT_STATS:
        return await send_embed(ctx, "❌ Нэгж Олдсонгүй", "Буруу нэгжийн нэр.", "admin", 0xB22222)
    p = get_player(member)
    p["army"][unit] = max(0, p["army"][unit] - max(0, amount))
    save_data(data)
    await send_embed(ctx, "📉 Цэрэг Хаслаа", f"**{member.display_name}** → **{UNIT_STATS[unit]['name']} -{amount}**", "admin")


@bot.command(name="setcityowner")
@is_admin()
async def setcityowner(ctx, city_name: str, member: discord.Member):
    city_name = city_name.title()
    if city_name not in data["cities"]:
        return await send_embed(ctx, "❌ Хот Алга", "Ийм хот бүртгэлгүй.", "admin", 0xB22222)
    p = get_player(member)
    data["cities"][city_name]["owner"] = member.display_name
    if city_name not in p["cities"]:
        p["cities"].append(city_name)
    save_data(data)
    await send_embed(ctx, "👑 Хот Эзэн Тохирууллаа", f"**{city_name}** → **{member.display_name}**", "admin")


@bot.command(name="reloadgame")
@is_admin()
async def reloadgame(ctx):
    global data
    data = load_data()
    ensure_city_state()
    await send_embed(ctx, "🔄 Өгөгдөл Дахин Ачааллаа", "Файл дахь мэдээлэл дахин уншигдлаа.", "admin")


# ============================================================
# EXTRA COMMAND PACK (to push total well past 100 commands)
# These are lightweight but fully working thematic commands.
# ============================================================
EXTRA_COMMANDS = {
    # economy extras
    "beg": ("economy", "🙏 Өршөөл", "Та замаар өнгөрөгчдөөс багахан хандив авлаа."),
    "gift": ("economy", "🎁 Бэлэг", "Ордноос танд өчүүхэн бэлэг ирэв."),
    "bonus": ("economy", "💎 Урамшуулал", "Таны хүчинд урамшуулал олгов."),
    "salary": ("economy", "📜 Цалин", "Албаны цалингаа авлаа."),
    "warehouse": ("shop", "📦 Агуулах", "Бараа, нөөцийн төв агуулахын тойм."),
    "resources": ("craft", "🪵 Нөөц", "Таны түүхий эдийн жагсаалт."),
    "woodcut": ("craft", "🪓 Мод Бэлтгэл", "Та ойгоос мод бэлтгэлээ."),
    "quarry": ("craft", "🪨 Чулуу", "Та чулуу олборлов."),
    "smelt": ("craft", "🔥 Хайлуулах", "Төмөр хайлуулах ажлыг эхлүүлэв."),
    "forge": ("craft", "⚒ Дархан", "Дархны газар зэвсэг цутгаж байна."),
    # military extras
    "stable": ("army", "🐴 Адууны Хашаа", "Морьдын бэлэн байдлыг шалгав."),
    "inspect": ("army", "🧐 Үзлэг", "Армийн эгнээг шалгалаа."),
    "banner": ("army", "🚩 Туг", "Таны тугийн сүр жавхаа өсөв."),
    "drill": ("army", "🏇 Дасгал", "Цэргүүд жагсаалын бэлтгэл хийв."),
    "tactics": ("army", "🗺 Тактик", "Та тулалдааны шинэ тактик боловсруулав."),
    "supply": ("army", "📦 Хангамж", "Армийн хүнс, сум зэвсгийг нөхөв."),
    "medic": ("army", "🩺 Эмч", "Шархдагсдад тусламж үзүүлэв."),
    "horsearcher": ("army", "🏹 Морин Харваач", "Морин харваачдын сургуулилтыг ажиглав."),
    "cavalry": ("army", "🐎 Морин Цэрэг", "Морин цэргийн бэлэн байдал хэвийн байна."),
    "kheshig": ("army", "👑 Хишигтэн", "Хишигтэн хамгаалалт ордныг манаж байна."),
    # conquest extras
    "province": ("conquest", "🗺 Муж", "Таны хилийн мужуудын байдал."),
    "frontier": ("conquest", "🏔 Хил", "Хилийн байдал тайван байна."),
    "border": ("conquest", "🚧 Хил Хязгаар", "Хилийн харуул нэмэгдэв."),
    "expand": ("conquest", "📍 Тэлэлт", "Эзэнт гүрний нөлөө өргөжив."),
    "govern": ("conquest", "🏛 Засаглал", "Хот, мужийн засаг захиргааг шалгав."),
    "prosperity": ("conquest", "🌟 Цэцэглэлт", "Хотын хөгжил өсөх шинжтэй байна."),
    "census": ("conquest", "📋 Тооллого", "Хүн ам, алба татварын тооллого хийгдэв."),
    "law": ("conquest", "⚖ Их Засаг", "Хууль цаазыг шинээр тунхаглав."),
    "decree": ("conquest", "📜 Зарлиг", "Төрийн зарлиг нийтэд хүрэв."),
    "tribute": ("conquest", "🏺 Алба", "Захирагдсан нутгаас алба ирэв."),
    # clan / diplomacy extras
    "alliance": ("clan", "🤝 Холбоо", "Холбоотны талаар хэлэлцэв."),
    "diplomacy": ("clan", "🕊 Дипломат", "Элч нарыг илгээв."),
    "treaty": ("clan", "📜 Гэрээ", "Энхийн гэрээний төсөл бэлэн болов."),
    "envoy": ("clan", "✉ Элч", "Элч мордов."),
    "respect": ("clan", "⭐ Нэр Хүнд", "Таны овгийн нэр хүнд өсөж байна."),
    "feast": ("clan", "🍖 Найр", "Их найр зохион байгууллаа."),
    "marry": ("clan", "💍 Гэрлэлт", "Улс төрийн гэрлэлт бол холбооны хэрэгсэл юм."),
    "heir": ("clan", "👶 Залгамжлагч", "Удам залгах асуудлыг хэлэлцэв."),
    "bloodline": ("clan", "🩸 Удам", "Таны угсаа гарлын сүр хүч нэмэгдэв."),
    "oath": ("clan", "🛡 Тангараг", "Тангараг өргөсөн цэргүүд үнэнч байна."),
    # utility extras
    "ping": ("default", "🏓 Ping", "Ботын хариу хэвийн байна."),
    "about": ("default", "📖 Тухай", "Chingis Empire RPG бол Монгол эзэнт гүрний сэдэвт стратеги бот юм."),
    "version": ("default", "🧩 Version", "Starter mega build v1."),
    "server": ("default", "🏰 Сервер", "Энэ сервер дээр эзэнт гүрний дайн өрнөж байна."),
    "rules": ("default", "📘 Дүрэм", "Серверийн дүрэм, шударга тоглоомыг мөрд."),
    "guide": ("default", "🗺 Гарын Авлага", "start → work → recruit → conquer гэсэн урсгалаар яв."),
    "faq": ("default", "❓ FAQ", "Хамгийн түгээмэл асуултын хариултууд энд байна."),
    "news": ("default", "📰 Мэдээ", "Өнөөдрийн эзэнт гүрний мэдээ ирлээ."),
    "event": ("default", "🎉 Event", "Түр хугацааны арга хэмжээ идэвхжиж болно."),
    "season": ("default", "🍂 Улирал", "Тал нутгийн улирал дайнд нөлөөлнө."),
    # more extras to comfortably exceed 100
    "horse": ("army", "🐴 Морь", "Таны шилдэг хүлгүүд аянд бэлэн."),
    "caravan": ("economy", "🐪 Жин Тэрэг", "Худалдааны жин ачаагаа хөдөлгөв."),
    "merchant": ("economy", "🧿 Наймаачин", "Наймаачид таны ордонд бараа дэлгэлээ."),
    "bazaar": ("shop", "🏪 Базар", "Өргөн зах ажиллаж байна."),
    "coin": ("economy", "🪙 Зоос", "Эргэлт дэх мөнгөн тэмдэгтийн байдал тогтвортой байна."),
    "treasury": ("economy", "🏛 Сангийн Яам", "Улсын сангийн тайланг үзлээ."),
    "crown": ("rank", "👑 Титэм", "Дээд эрх мэдлийн бэлгэдэл."),
    "throne": ("rank", "🪑 Сэнтий", "Сэнтийн төлөө өрсөлдөөн ширүүснэ."),
    "palace": ("rank", "🏯 Ордон", "Ордны амьдрал үргэлжилж байна."),
    "council": ("rank", "🧠 Зөвлөл", "Их зөвлөл хуралдав."),
    "minister": ("rank", "📜 Сайд", "Төрийн сайд нарын асуудал өрнөв."),
    "judge": ("rank", "⚖ Шүүлт", "Шихихутаг маягийн шүүн таслах ажил өрнөв."),
    "scribe": ("rank", "✒ Бичээч", "Төрийн бичээч зарлиг тэмдэглэв."),
    "messenger": ("travel", "📯 Элч Мордов", "Алс хязгаар руу элч илгээлээ."),
    "road": ("travel", "🛤 Зам", "Их зам дагуух хөдөлгөөн идэвхжив."),
    "campfire": ("travel", "🔥 Түүдэг", "Шөнийн отог тайван байна."),
    "steppe": ("travel", "🌾 Тал Нутгийн Салхи", "Тал нутгийн сүр хүч мэдрэгдэнэ."),
    "weather": ("travel", "☁ Цаг Агаар", "Цаг агаар аян дайнд нөлөөлж болно."),
    "oracle": ("default", "🔮 Зөн", "Ирээдүйд их дайн ирж болзошгүй."),
    "legend": ("default", "📚 Домог", "Чингисийн үеийн домог, сүр хүчний түүх үргэлжилнэ."),
    "story": ("default", "📖 Түүх", "Таны эзэнт гүрний түүх бичигдсээр байна."),
    "honor": ("rank", "🏅 Нэр Төр", "Нэр төр цусаар бус үйл хэргээр тогтдог."),
    "glory": ("rank", "✨ Алдар", "Ялалт алдар хүндийг авчирна."),
    "destiny": ("default", "🌌 Хувь Тавилан", "Их хааны зам хэцүү ч сүрлэг."),
    "bannerup": ("army", "🚩 Туг Өргөв", "Туг намирч, цэргүүдийн зориг өсөв."),
    "horn": ("army", "📯 Бүрээ", "Дайны бүрээ хангинав."),
    "charge": ("battle", "⚡ Дайралт", "Шуурхай дайралтын бэлтгэл хангагдав."),
    "retreat": ("battle", "↩ Ухралт", "Ухаалаг ухралт ч ялалтын нэг хэлбэр."),
    "ambush": ("battle", "🌫 Отолт", "Отолтын байршлыг тагнав."),
    "duel": ("battle", "🗡 Халз", "Ноёдын халз тулаан эхлэх дөхөв."),
    "bannerlord": ("rank", "🏇 Тугт Ноён", "Тугт ноёдын сүр хүчийг дурсав."),
    "empire": ("default", "🌍 Эзэнт Гүрэн", "Таны ирээдүйн зорилго бол дэлхийг нэгтгэх."),
    "homeland": ("default", "🏕 Эх Нутаг", "Эх нутгийн хүч таны сэтгэлд байна."),
}


def register_extra_command(cmd_name: str, category: str, title: str, text: str):
    async def _cmd(ctx):
        p = get_player(ctx.author)
        bonus_money = 0
        bonus_xp = 0
        if category == "economy":
            bonus_money = random.randint(20, 90)
            p["money"] += bonus_money
        if category in {"army", "battle", "conquest", "rank", "craft"}:
            bonus_xp = random.randint(4, 14)
            add_xp(p, bonus_xp)
        save_data(data)
        extra = []
        if bonus_money:
            extra.append(f"**+{bonus_money} мөнгө**")
        if bonus_xp:
            extra.append(f"**+{bonus_xp} EXP**")
        tail = "\n" + "\n".join(extra) if extra else ""
        await send_embed(ctx, title, text + tail, category)

    _cmd.__name__ = f"cmd_{cmd_name}"
    bot.command(name=cmd_name)(_cmd)


for _name, (_cat, _title, _text) in EXTRA_COMMANDS.items():
    register_extra_command(_name, _cat, _title, _text)


# ============================================================
# FINAL SAFETY
# ============================================================
if not TOKEN:
    raise RuntimeError("TOKEN environment variable is missing.")

bot.run(TOKEN)
