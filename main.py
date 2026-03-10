import os
import json
import math
import random
from datetime import datetime, timedelta

import discord
from discord.ext import commands

# ============================================================
# CHINGIS EMPIRE BOT - LARGE SCALE MONGOL STRATEGY RPG
# FINAL MERGED VERSION - NO ENERGY + IMPROVED UI
# discord.py 2.x
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
    "default": "https://cdn.discordapp.com/attachments/1479354971479609394/1480447298868871269/content.png",
    "help": "https://cdn.discordapp.com/attachments/1479354971479609394/1480447298868871269/content.png",
}

EMOJIS = {
    "money": "💰",
    "bank": "🏦",
    "xp": "✨",
    "rank": "🎖",
    "army": "⚔",
    "defense": "🛡",
    "city": "🏙",
    "clan": "🐺",
    "work": "🛠",
    "shop": "🛒",
    "market": "🏪",
    "blackmarket": "🕶",
    "inventory": "🎒",
    "resource": "🪵",
    "heal": "🩹",
    "tax": "📜",
    "crown": "👑",
    "horse": "🐎",
    "warning": "⚠",
    "success": "✅",
    "fail": "❌",
    "fire": "🔥",
    "star": "⭐",
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

RANK_IMAGES = {
    "Малчин": "https://cdn.discordapp.com/attachments/1479354971479609394/1480584566149353595/content.png",
    "Анчин": "https://cdn.discordapp.com/attachments/1479354971479609394/1480585631502569554/content.png",
    "Галч": "https://cdn.discordapp.com/attachments/1479354971479609394/1480586367347200091/content.png",
    "Тариачин": "https://cdn.discordapp.com/attachments/1479354971479609394/1480588713678344373/content.png",
    "Аравтын Цэрэг": "https://cdn.discordapp.com/attachments/1479354971479609394/1480590391513321502/content.png",
    "Аравтын Захирагч": "https://cdn.discordapp.com/attachments/1479354971479609394/1480591578451152986/content.png",
    "Зуутын Цэрэг": "https://cdn.discordapp.com/attachments/1479354971479609394/1480593895858376845/content.png",
    "Зуутын Захирагч": "https://cdn.discordapp.com/attachments/1479354971479609394/1480594237895737607/content.png",
    "Мянгатын Цэрэг": "https://cdn.discordapp.com/attachments/1479354971479609394/1480598658394361919/content.png",
    "Мянгатын Захирагч": "https://cdn.discordapp.com/attachments/1479354971479609394/1480598904432099358/content.png",
    "Түмний Ноён": "https://cdn.discordapp.com/attachments/1479354971479609394/1480600974153355264/content.png",
    "Хилийн Харуул": "https://cdn.discordapp.com/attachments/1479354971479609394/1480497484798230630/content.png",
    "Орлогч Жанжин": "https://cdn.discordapp.com/attachments/1479354971479609394/1480503409345036298/content.png",
    "Жанжин": "https://cdn.discordapp.com/attachments/1479354971479609394/1480507547344703561/content.png",
    "Түшмэл": "https://cdn.discordapp.com/attachments/1479354971479609394/1480508346170871899/content.png",
    "Сайд": "https://cdn.discordapp.com/attachments/1479354971479609394/1480510109166731284/content.png",
    "Их Сайд": "https://cdn.discordapp.com/attachments/1479354971479609394/1480515205137039440/content.png",
    "Нууц Зөвлөх": "https://cdn.discordapp.com/attachments/1479354971479609394/1480516407115386910/content.png",
    "Тата Тунга": "https://cdn.discordapp.com/attachments/1479354971479609394/1480519657852244119/content.png",
    "Шихихутаг": "https://cdn.discordapp.com/attachments/1479354971479609394/1480578865012277258/content.png",
    "Их Жанжин": "https://cdn.discordapp.com/attachments/1479354971479609394/1480579663125545223/content.png",
    "Хаадын Хаан": "https://cdn.discordapp.com/attachments/1479354971479609394/1480580903825833985/content.png",
    "Их Эзэн Хаан": "https://cdn.discordapp.com/attachments/1479354971479609394/1480583828052377772/content.png",
}

CITY_POOL = [
    "Хархорум", "Бухара", "Самарканд", "Бээжин", "Кашгар", "Алтан Ордон",
    "Мерв", "Ургенч", "Баласагун", "Отрар", "Ховд", "Хираат"
]

RESOURCE_TYPES = ["алт", "мод", "чулуу", "төмөр", "арьс", "морь", "тариа", "мах"]

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


def save_data(data_obj):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data_obj, f, ensure_ascii=False, indent=2) 


data = load_data()

# ============================================================
# WORK / SHOP SYSTEM UPGRADE
# ============================================================
for old_cmd in ["work", "shop", "buy", "sell", "market", "blackmarket", "price", "energy"]:
    try:
        bot.remove_command(old_cmd)
    except Exception:
        pass

ITEM_NAMES = {
    "airag": "Айраг",
    "mah": "Мах",
    "tarag": "Тараг",
    "guril": "Гурил",
    "mod": "Мод",
    "chuluu": "Чулуу",
    "tomor": "Төмөр",
    "aris": "Арьс",
    "mori": "Морь",
    "banner": "Туг",
    "sword": "Сэлэм",
    "armor": "Хуяг",
    "royal_banner": "Хааны Туг",
    "elite_armor": "Элит Хуяг",
    "war_horse": "Дайны Морь",
    "steel_blade": "Ган Сэлэм",
}

SHOP_CATEGORIES = {
    "food": "🍖 Хүнс",
    "material": "🪵 Материал",
    "mount": "🐎 Хүлэг",
    "cosmetic": "🎌 Гоёл",
    "weapon": "🗡 Зэвсэг",
    "armor": "🛡 Хуяг",
}

SHOP_ITEMS = {
    "airag": {"price": 55, "type": "food"},
    "mah": {"price": 80, "type": "food"},
    "tarag": {"price": 60, "type": "food"},
    "guril": {"price": 75, "type": "food"},
    "mod": {"price": 95, "type": "material"},
    "chuluu": {"price": 110, "type": "material"},
    "tomor": {"price": 180, "type": "material"},
    "aris": {"price": 140, "type": "material"},
    "mori": {"price": 1200, "type": "mount"},
    "banner": {"price": 850, "type": "cosmetic"},
    "sword": {"price": 1600, "type": "weapon"},
    "armor": {"price": 2100, "type": "armor"},
}

WORK_TIERS = [
    {
        "min_level": 1,
        "name": "Энгийн хөдөлмөр",
        "jobs": [
            ("тэрэг түрж ачаа зөөлөө", 90, 12),
            ("малын хашаа заслаа", 100, 13),
            ("галын түлээ бэлтгэлээ", 95, 12),
            ("жингийн замд туслав", 110, 14),
        ]
    },
    {
        "min_level": 10,
        "name": "Туршлагатай ажил",
        "jobs": [
            ("татварын бүртгэл хийлээ", 150, 18),
            ("ангийн отряд зохион байгууллаа", 170, 20),
            ("агуулах хамгаалж орлого оллоо", 165, 19),
            ("морь сургаж ноёдод нийлүүллээ", 180, 22),
        ]
    },
    {
        "min_level": 30,
        "name": "Захирагчийн ажил",
        "jobs": [
            ("жижиг мужийн татвар хураалаа", 240, 28),
            ("хилийн цэргийн хангалтыг зохицуулав", 260, 30),
            ("худалдааны гэрээ байгууллаа", 280, 31),
            ("цэргийн бэлтгэлийг хянаж урамшуулал авлаа", 300, 33),
        ]
    },
    {
        "min_level": 60,
        "name": "Ноёдын түвшний ажил",
        "jobs": [
            ("мужийн орлого захирч ашиг хүртлээ", 420, 42),
            ("цэргийн хангамжийн том гэрээ байгууллаа", 460, 45),
            ("алс нутгийн худалдааны замыг хамгаалав", 500, 48),
            ("ордны тусгай даалгавар биелүүлэв", 540, 50),
        ]
    },
    {
        "min_level": 100,
        "name": "Жанжны түвшний ажил",
        "jobs": [
            ("эзэнт гүрний стратегийн албанд ажиллав", 700, 65),
            ("чухал мужийн санхүүг удирдав", 760, 70),
            ("дайны бэлтгэл хангасан тул шагнуулав", 820, 76),
            ("хааны нууц үүрэг гүйцэтгэв", 900, 82),
        ]
    },
]

BLACKMARKET_ITEMS = {
    "royal_banner": {"price": 3500, "type": "cosmetic", "name": "Хааны Туг"},
    "elite_armor": {"price": 4200, "type": "armor", "name": "Элит Хуяг"},
    "war_horse": {"price": 3000, "type": "mount", "name": "Дайны Морь"},
    "steel_blade": {"price": 2800, "type": "weapon", "name": "Ган Сэлэм"},
}


def uid(user_id: int) -> str:
    return str(user_id)


def default_player(member):
    return {
        "name": member.display_name,
        "money": 1500,
        "bank": 0,
        "xp": 0,
        "level": 1,
        "rank": "Малчин",
        "hp": 100,
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
        "created_at": int(now_ts()),
        "work_streak": 0,
        "last_work_day": None,
        "market_discount": 0.0,
        "shop_stats": {"bought": 0, "sold": 0},
        "blackmarket_refresh": 0,
    }


def parse_amount(raw, max_amount: int):
    if raw is None:
        return 1

    text = str(raw).strip().lower()
    if text in ["all", "max", "bugd", "бүгд"]:
        return max_amount

    try:
        value = int(text)
        return value
    except Exception:
        return None


def ensure_player_upgrades(player: dict):
    player.setdefault("name", "player")
    player.setdefault("created_at", int(datetime.utcnow().timestamp()))
    player.setdefault("money", 0)
    player.setdefault("bank", 0)
    player.setdefault("xp", 0)
    player.setdefault("level", 1)
    player.setdefault("rank", "Малчин")
    player.setdefault("hp", 100)
    player.setdefault("influence", 0)
    player.setdefault("clan", None)
    player.setdefault("spouse", None)
    player.setdefault("title", "Эзэнт гүрний шинэ иргэн")
    player.setdefault("wanted", 0)
    player.setdefault("wins", 0)
    player.setdefault("losses", 0)
    player.setdefault("cities", [])
    player.setdefault("province_power", 0)
    player.setdefault("tax_rate", 5)
    player.setdefault("inventory", {})
    player.setdefault("resources", {r: 0 for r in RESOURCE_TYPES})
    player.setdefault("army", {k: 0 for k in UNIT_STATS.keys()})
    player.setdefault("cooldowns", {})
    player.setdefault("businesses", [])
    player.setdefault("skills", {})
    player.setdefault("tech", {})
    player.setdefault("work_streak", 0)
    player.setdefault("last_work_day", None)
    player.setdefault("market_discount", 0.0)
    player.setdefault("shop_stats", {})
    player["shop_stats"].setdefault("bought", 0)
    player["shop_stats"].setdefault("sold", 0)
    player.setdefault("blackmarket_refresh", 0)

    player["skills"].setdefault("leadership", 0)
    player["skills"].setdefault("warfare", 0)
    player["skills"].setdefault("trade", 0)
    player["skills"].setdefault("charisma", 0)

    player["tech"].setdefault("economy", 0)
    player["tech"].setdefault("military", 0)
    player["tech"].setdefault("trade", 0)
    player["tech"].setdefault("logistics", 0)

    player.pop("energy", None)

    player["money"] = max(0, int(player.get("money", 0)))
    player["bank"] = max(0, int(player.get("bank", 0)))
    player["xp"] = max(0, int(player.get("xp", 0)))
    player["level"] = max(1, int(player.get("level", 1)))
    player["wanted"] = max(0, int(player.get("wanted", 0)))
    player["influence"] = max(0, int(player.get("influence", 0)))
    player["market_discount"] = max(0.0, min(0.15, float(player.get("market_discount", 0.0))))


def get_player(member):
    key = uid(member.id)
    if key not in data["players"]:
        data["players"][key] = default_player(member)
        save_data(data)

    data["players"][key]["name"] = member.display_name
    ensure_player_upgrades(data["players"][key])
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
    ensure_player_upgrades(player)
    player["xp"] += amount
    leveled = []
    while player["level"] < MAX_LEVEL and player["xp"] >= xp_to_next(player["level"]):
        player["xp"] -= xp_to_next(player["level"])
        player["level"] += 1
        player["rank"] = get_rank(player["level"])
        player["hp"] = min(100 + player["level"], 300)
        leveled.append(player["level"])
    return leveled


def army_power(player: dict):
    atk, defense = 0, 0
    for unit_key, count in player["army"].items():
        stat = UNIT_STATS[unit_key]
        atk += stat["power"] * count
        defense += stat["defense"] * count
    atk += player["skills"]["warfare"] * 6
    defense += player["skills"]["leadership"] * 6
    return atk, defense


def cd_ready(player: dict, key: str, seconds: int):
    last = player["cooldowns"].get(key, 0)
    diff = int(now_ts() - last)
    if diff >= seconds:
        return True, 0
    return False, seconds - diff


def set_cd(player: dict, key: str):
    player["cooldowns"][key] = now_ts()


def get_item_display(item_key: str):
    if item_key in BLACKMARKET_ITEMS:
        return BLACKMARKET_ITEMS[item_key].get("name", item_key)
    return ITEM_NAMES.get(item_key, item_key)


def fmt_army(player: dict) -> str:
    lines = []
    for k, stat in UNIT_STATS.items():
        lines.append(f"**{stat['name']}**: {player['army'][k]}")
    return "\n".join(lines)


def fmt_inventory(player: dict) -> str:
    inv = player.get("inventory", {})
    if not inv:
        return "🎒 **Хоосон агуулах**"

    lines = []
    for k, v in inv.items():
        if v > 0:
            lines.append(f"• **{get_item_display(k)}** (`{k}`) × **{v}**")
    return "\n".join(lines) or "🎒 **Хоосон агуулах**"


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
# BUILDINGS (BIG EMPIRE BALANCE)
# ============================================================

BUILDINGS = {

    "ger": {
        "name": "Гэр",
        "price": 300,
        "desc": "Иргэдийн амьдрах байр. Хүн ам өсөх суурь.",
        "income": 10,
        "power": 0,
        "defense": 0,
        "limit": 500,
        "emoji": "⛺",
        "build_time": 0
    },

    "farm": {
        "name": "Ферм",
        "price": 700,
        "desc": "Хүнс үйлдвэрлэнэ. Орлого нэмэгдэнэ.",
        "income": 35,
        "power": 0,
        "defense": 0,
        "limit": 350,
        "emoji": "🌾",
        "build_time": 3
    },

    "stable": {
        "name": "Морин Хашаа",
        "price": 1200,
        "desc": "Морь, цэргийн хүчийг нэмэгдүүлнэ.",
        "income": 15,
        "power": 20,
        "defense": 5,
        "limit": 250,
        "emoji": "🐎",
        "build_time": 4
    },

    "forge": {
        "name": "Дархны Газар",
        "price": 1800,
        "desc": "Зэвсэг, хуяг үйлдвэрлэнэ. Mine bonus өгнө.",
        "income": 20,
        "power": 35,
        "defense": 10,
        "limit": 200,
        "emoji": "⚒️",
        "build_time": 5
    },

    "wall": {
        "name": "Хэрэм",
        "price": 2500,
        "desc": "Хотын хамгаалалтыг ихэсгэнэ.",
        "income": 0,
        "power": 0,
        "defense": 40,
        "limit": 300,
        "emoji": "🧱",
        "build_time": 6
    },

    "market": {
        "name": "Зах",
        "price": 2200,
        "desc": "Арилжаа, наймааг хөгжүүлнэ.",
        "income": 60,
        "power": 0,
        "defense": 0,
        "limit": 180,
        "emoji": "🏪",
        "build_time": 4
    },

    "temple": {
        "name": "Сүм",
        "price": 3200,
        "desc": "Эзэнт гүрний нэр хүнд, хамгаалалтыг өсгөнө.",
        "income": 25,
        "power": 10,
        "defense": 20,
        "limit": 100,
        "emoji": "🏯",
        "build_time": 6
    }
}

# ============================================================
# OLD SAVE DATA CLEANUP
# ============================================================
try:
    for uid_key, player in data.get("players", {}).items():
        if isinstance(player, dict):
            player.pop("energy", None)
            ensure_player_upgrades(player)
    save_data(data)
except Exception:
    pass

# ============================================================
# UPGRADED SHOP / WORK HELPERS
# ============================================================
def get_work_tier(level: int):
    current = WORK_TIERS[0]
    for tier in WORK_TIERS:
        if level >= tier["min_level"]:
            current = tier
    return current


def uid_hash(player: dict):
    return f"{player.get('created_at', 0)}-{player.get('name', 'player')}"


def get_dynamic_price(item_key: str, player: dict, market_type="shop"):
    if item_key not in SHOP_ITEMS:
        return 0

    ensure_player_upgrades(player)

    base = int(SHOP_ITEMS[item_key]["price"])
    trade_bonus = player["skills"].get("trade", 0) * 0.01
    charisma_bonus = player["skills"].get("charisma", 0) * 0.005
    level_bonus = min(0.10, player["level"] * 0.001)

    seed_day = datetime.utcnow().strftime("%Y%m%d")
    rng = random.Random(f"{item_key}-{seed_day}-{market_type}")
    fluctuation = rng.uniform(-0.18, 0.22)

    item_type = SHOP_ITEMS[item_key].get("type", "misc")
    if item_type == "food":
        fluctuation += rng.uniform(-0.03, 0.04)
    elif item_type == "weapon":
        fluctuation += rng.uniform(0.00, 0.08)
    elif item_type == "armor":
        fluctuation += rng.uniform(0.01, 0.10)

    if market_type == "buy":
        modifier = 1.0 + fluctuation - trade_bonus - charisma_bonus - player.get("market_discount", 0)
    elif market_type == "sell":
        modifier = 0.60 + (trade_bonus * 0.8) + (charisma_bonus * 0.6) + max(-0.08, fluctuation * 0.35)
    else:
        modifier = 1.0 + fluctuation + level_bonus * 0.2

    modifier = max(0.15, modifier)
    return max(1, int(base * modifier))


def get_blackmarket_price(item_key: str, player: dict):
    if item_key not in BLACKMARKET_ITEMS:
        return 0

    ensure_player_upgrades(player)

    base = int(BLACKMARKET_ITEMS[item_key]["price"])
    seed_hour = datetime.utcnow().strftime("%Y%m%d%H")
    rng = random.Random(f"bm-{uid_hash(player)}-{item_key}-{seed_hour}")

    fluctuation = rng.uniform(-0.10, 0.22)
    trade_bonus = player["skills"].get("trade", 0) * 0.008
    charisma_bonus = player["skills"].get("charisma", 0) * 0.004

    modifier = 1.0 + fluctuation - trade_bonus - charisma_bonus
    modifier = max(0.40, modifier)

    return max(1, int(base * modifier))


def get_blackmarket_offers(player: dict):
    ensure_player_upgrades(player)
    seed_hour = datetime.utcnow().strftime("%Y%m%d%H")
    rng = random.Random(f"blackmarket-{uid_hash(player)}-{seed_hour}")
    keys = list(BLACKMARKET_ITEMS.keys())
    rng.shuffle(keys)
    return keys[:3]


def format_shop_lines(player: dict):
    ensure_player_upgrades(player)
    grouped = {}

    for item_key, meta in SHOP_ITEMS.items():
        cat = meta.get("type", "other")
        grouped.setdefault(cat, [])
        buy_price = get_dynamic_price(item_key, player, "buy")
        sell_price = get_dynamic_price(item_key, player, "sell")

        grouped[cat].append(
            f"• **{get_item_display(item_key)}** (`{item_key}`)\n"
            f"　{EMOJIS['money']} Авах: **{buy_price}** | Буцааж зарах: **{sell_price}**"
        )

    parts = []
    for cat, lines in grouped.items():
        parts.append(f"**{SHOP_CATEGORIES.get(cat, cat)}**\n" + "\n".join(lines))
    return "\n\n".join(parts)


def get_work_cooldown(player: dict):
    ensure_player_upgrades(player)
    base = 300
    logistics_reduce = player["tech"].get("logistics", 0) * 4
    level_reduce = min(50, player["level"] // 3)
    return max(120, base - logistics_reduce - level_reduce)


def update_work_streak(player: dict):
    ensure_player_upgrades(player)
    today = datetime.utcnow().date()
    last_day_raw = player.get("last_work_day")

    try:
        last_day = datetime.strptime(last_day_raw, "%Y-%m-%d").date() if last_day_raw else None
    except Exception:
        last_day = None

    if last_day == today:
        pass
    elif last_day == (today - timedelta(days=1)):
        player["work_streak"] = min(7, player.get("work_streak", 0) + 1)
        player["last_work_day"] = today.strftime("%Y-%m-%d")
    else:
        player["work_streak"] = 1
        player["last_work_day"] = today.strftime("%Y-%m-%d")

# ============================================================
# EMBEDS
# ============================================================
def image_for(category: str) -> str:
    return IMAGES.get(category, IMAGES["default"])


def game_embed(title, description, category="default", player=None, color=0xA67C39):
    em = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.utcnow()
    )

    if player and player.get("rank") in RANK_IMAGES:
        em.set_image(url=RANK_IMAGES[player["rank"]])
    else:
        em.set_image(url=image_for(category))

    em.set_footer(text="🐎 Chingis Empire RPG • Монгол Эзэнт Гүрэн")

    if player:
        em.add_field(
            name="📌 Товч Мэдээлэл",
            value=(
                f"**{EMOJIS['rank']} Lv:** {player.get('level', 1)}\n"
                f"**{EMOJIS['money']} Мөнгө:** {player.get('money', 0)}\n"
                f"**{EMOJIS['xp']} EXP:** {player.get('xp', 0)}/{xp_to_next(player.get('level', 1))}"
            ),
            inline=True
        )
        em.add_field(
            name="🏛 Байдал",
            value=(
                f"**{EMOJIS['crown']} Цол:** {player.get('rank', 'Малчин')}\n"
                f"**{EMOJIS['clan']} Овог:** {player.get('clan') or 'Байхгүй'}\n"
                f"**{EMOJIS['city']} Хот:** {len(player.get('cities', []))}"
            ),
            inline=True
        )

    return em


async def send_embed(ctx, title, description, category="default", player=None, color=0xA67C39):
    await ctx.send(
        embed=game_embed(
            title,
            description,
            category=category,
            player=player,
            color=color,
        )
    )

# ============================================================
# ADMIN CHECK
# ============================================================
def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

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
                category="rank",
                player=player,
                color=0xE0B84D,
            )
        )

    save_data(data)
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        return await send_embed(
            ctx,
            "❌ Дутуу комманд",
            "Коммандын параметр дутуу байна.",
            "default",
            color=0xB22222
        )
    if isinstance(error, commands.BadArgument):
        return await send_embed(
            ctx,
            "❌ Буруу утга",
            "Хэрэглэгч эсвэл тоо буруу байна.",
            "default",
            color=0xB22222
        )
    if isinstance(error, commands.CheckFailure):
        return await send_embed(
            ctx,
            "⛔ Хандах эрхгүй",
            "Энэ командыг зөвхөн админ хэрэглэнэ.",
            "admin",
            color=0xB22222
        )

    print("Unhandled command error:", repr(error))
    await send_embed(
        ctx,
        "💥 Алдаа",
        f"Алдаа гарлаа:\n`{error}`",
        "default",
        color=0xB22222
    )

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
        f"**{ctx.author.display_name}**, та одоо Монголын Их Эзэнт Гүрний шинэ иргэн боллоо.\n\n"
        f"💰 **Эхлэх мөнгө:** {p['money']}\n"
        f"🎖 **Түвшин:** {p['level']}\n"
        f"👑 **Цол:** {p['rank']}\n\n"
        f"📜 Эхлэх тушаал: `{PREFIX}help`",
        "start",
        player=p
    )


@bot.command(name="help", aliases=["commands", "cmd", "menu"])
async def help_command(ctx):
    p = get_player(ctx.author)
    atk, df = army_power(p)

    em = discord.Embed(
        title="📜 CHINGIS EMPIRE • HELP",
        description=(
            f"**{ctx.author.display_name}**, доорх нь тоглоомын үндсэн тушаалууд.\n\n"
            f"🗺 Заавар: `{PREFIX}guide`\n"
            f"✨ Нэмэлт команд: `{PREFIX}extras`"
        ),
        color=0xD4AF37,
        timestamp=datetime.utcnow()
    )

    em.add_field(
        name="👤 Суурь",
        value=(
            "`start`, `profile`, `me`, `stats`, `rank`, `xp`\n"
            "`title`, `settitle`, `inventory`, `bag`, `heal`"
        ),
        inline=False
    )

    em.add_field(
        name="💰 Эдийн засаг",
        value=(
            "`balance`, `bal`, `money`, `bank`\n"
            "`deposit`, `withdraw`, `work`, `daily`, `weekly`\n"
            "`mine`, `hunt`, `farm`, `fish`, `woodcut`, `quarry`\n"
            "`resources`, `tax`, `collecttax`"
        ),
        inline=False
    )

    em.add_field(
        name="🛒 Худалдаа",
        value=(
            "`shop`, `price`, `buy`, `sell`\n"
            "`market`, `blackmarket`, `craft`"
        ),
        inline=False
    )

    em.add_field(
        name="⚔ Арми",
        value=(
            "`units`, `recruit`, `army`, `disband`\n"
            "`fortify`, `scout`, `train`, `garrison`, `patrol`"
        ),
        inline=False
    )

    em.add_field(
        name="🏙 Хот / Дайн",
        value=(
            "`cities`, `city`, `conquer`, `invade`, `raid`\n"
            "`defendcity`, `siege`, `march`, `camp`, `attack`"
        ),
        inline=False
    )

    em.add_field(
        name="🐺 Овог",
        value=(
            "`clancreate`, `claninfo`, `clanjoin`\n"
            "`clanleave`, `clandonate`, `clanvault`, `clanwar`"
        ),
        inline=False
    )

    em.add_field(
        name="🏆 Шилдгүүд",
        value=(
            "`leaderboard`, `topmoney`, `toplevel`\n"
            "`topwar`, `topcities`, `topclans`"
        ),
        inline=False
    )

    em.add_field(
        name="⚡ Түргэн эхлэх",
        value=(
            f"`{PREFIX}start` → `{PREFIX}work` → `{PREFIX}shop`\n"
            f"`{PREFIX}recruit ywgan 5` → `{PREFIX}conquer Хархорум`"
        ),
        inline=False
    )

    em.add_field(
        name="👑 Таны байдал",
        value=(
            f"**🎖 Level:** {p['level']}\n"
            f"**👑 Цол:** {p['rank']}\n"
            f"**💰 Мөнгө:** {p['money']}\n"
            f"**🏦 Банк:** {p['bank']}\n"
            f"**🏙 Хот:** {len(p['cities'])}\n"
            f"**🐺 Овог:** {p['clan'] or 'Байхгүй'}\n"
            f"**⚔ Attack:** {atk}\n"
            f"**🛡 Defense:** {df}"
        ),
        inline=False
    )

    if ctx.author.guild_permissions.administrator:
        em.add_field(
            name="🛡 Админ",
            value="`adminhelp`",
            inline=False
        )

    if p.get("rank") in RANK_IMAGES:
        em.set_image(url=RANK_IMAGES[p["rank"]])
    else:
        em.set_image(url=image_for("help"))

    em.set_thumbnail(url=ctx.author.display_avatar.url)
    em.set_footer(text="🐎 Chingis Empire RPG • Үндсэн Тушаалууд")

    await ctx.send(embed=em)


@bot.command(name="guide")
async def guide_command(ctx):
    p = get_player(ctx.author)

    em = discord.Embed(
        title="🗺 CHINGIS EMPIRE • GUIDE",
        description="Шинэ тоглогчийн эхлэх заавар",
        color=0xC89B3C,
        timestamp=datetime.utcnow()
    )

    em.add_field(
        name="1️⃣ Эхлэх",
        value=(
            f"`{PREFIX}start` ашиглаад тоглоомоо эхлүүл.\n"
            f"Дараа нь `{PREFIX}profile` ашиглаад өөрийн байдлаа шалга."
        ),
        inline=False
    )

    em.add_field(
        name="2️⃣ Мөнгө олох",
        value=(
            f"`{PREFIX}work` бол хамгийн гол орлого.\n"
            f"`{PREFIX}daily`, `{PREFIX}weekly`, `{PREFIX}mine`, `{PREFIX}hunt`, `{PREFIX}farm` ашигла."
        ),
        inline=False
    )

    em.add_field(
        name="3️⃣ Худалдаа",
        value=(
            f"`{PREFIX}shop` → бараа харах\n"
            f"`{PREFIX}buy sword 1` → зэвсэг авах\n"
            f"`{PREFIX}sell item amount` → бараа зарах"
        ),
        inline=False
    )

    em.add_field(
        name="4️⃣ Арми босгох",
        value=(
            f"`{PREFIX}units` → нэгжүүдээ харах\n"
            f"`{PREFIX}recruit ywgan 5` → анхны цэрэг элсүүлэх\n"
            f"`{PREFIX}army` → хүчээ шалгах"
        ),
        inline=False
    )

    em.add_field(
        name="5️⃣ Хот эзлэх",
        value=(
            f"`{PREFIX}cities` → хотууд харах\n"
            f"`{PREFIX}scout` → тагнах\n"
            f"`{PREFIX}conquer Хархорум` → хот эзлэх"
        ),
        inline=False
    )

    em.add_field(
        name="6️⃣ Овог",
        value=(
            f"`{PREFIX}clancreate BlueWolf` → овог байгуулах\n"
            f"`{PREFIX}clandonate 500` → сан нэмэх\n"
            f"`{PREFIX}clanwar enemyname` → овгийн дайн"
        ),
        inline=False
    )

    em.add_field(
        name="💡 Зөвлөгөө",
        value="Эхэндээ `work` + `daily` + `recruit` дээр төвлөрвөл хурдан өснө.",
        inline=False
    )

    if p.get("rank") in RANK_IMAGES:
        em.set_image(url=RANK_IMAGES[p["rank"]])
    else:
        em.set_image(url=image_for("help"))

    em.set_footer(text="🐎 Chingis Empire RPG • Эхлэх Заавар")
    await ctx.send(embed=em)


@bot.command(name="extras", aliases=["extra", "fun"])
async def extras_command(ctx):
    p = get_player(ctx.author)

    em = discord.Embed(
        title="✨ CHINGIS EMPIRE • EXTRA COMMANDS",
        description=(
            f"Эдгээр нь нэмэлт, roleplay, fun төрлийн командууд.\n"
            f"Үндсэн командуудыг харах бол `{PREFIX}help`."
        ),
        color=0x8F6BC1,
        timestamp=datetime.utcnow()
    )

    em.add_field(
        name="💰 Economy Extras",
        value="`beg`, `gift`, `bonus`, `salary`, `caravan`, `merchant`, `coin`, `treasury`",
        inline=False
    )

    em.add_field(
        name="⚔ Army Extras",
        value="`stable`, `inspect`, `banner`, `drill`, `tactics`, `supply`, `medic`, `horsearcher`, `cavalry`, `kheshig`, `horse`, `bannerup`, `horn`",
        inline=False
    )

    em.add_field(
        name="🏙 Conquest Extras",
        value="`province`, `frontier`, `border`, `expand`, `govern`, `prosperity`, `census`, `law`, `decree`, `tribute`",
        inline=False
    )

    em.add_field(
        name="🐺 Clan / RP Extras",
        value="`alliance`, `diplomacy`, `treaty`, `envoy`, `respect`, `feast`, `marry`, `heir`, `bloodline`, `oath`",
        inline=False
    )

    em.add_field(
        name="👑 Rank / Story Extras",
        value="`crown`, `throne`, `palace`, `council`, `minister`, `judge`, `scribe`, `honor`, `glory`, `bannerlord`",
        inline=False
    )

    em.add_field(
        name="🌍 World / Travel Extras",
        value="`messenger`, `road`, `campfire`, `steppe`, `weather`, `oracle`, `legend`, `story`, `empire`, `homeland`",
        inline=False
    )

    em.add_field(
        name="📘 Info",
        value="`about`, `version`, `server`, `rules`, `faq`, `news`, `event`, `season`, `ping`",
        inline=False
    )

    if p.get("rank") in RANK_IMAGES:
        em.set_image(url=RANK_IMAGES[p["rank"]])
    else:
        em.set_image(url=image_for("help"))

    em.set_footer(text="🐎 Chingis Empire RPG • Нэмэлт Тушаалууд")
    await ctx.send(embed=em)


@bot.command(name="profile", aliases=["me"])
async def profile(ctx, member: discord.Member = None):
    member = member or ctx.author
    p = get_player(member)
    atk, df = army_power(p)

    desc = (
        f"**Нэр:** {member.display_name}\n"
        f"**Title:** {p['title']}\n"
        f"**Level:** {p['level']}\n"
        f"**Rank:** {p['rank']}\n"
        f"**Money:** {p['money']}\n"
        f"**Bank:** {p['bank']}\n"
        f"**HP:** {p['hp']}\n"
        f"**Influence:** {p['influence']}\n"
        f"**Clan:** {p['clan'] or 'Байхгүй'}\n"
        f"**Cities:** {len(p['cities'])}\n"
        f"**Wins / Losses:** {p['wins']} / {p['losses']}\n"
        f"**Attack / Defense:** {atk} / {df}"
    )

    await send_embed(
        ctx,
        f"👤 {member.display_name}-ийн Профайл",
        desc,
        "profile",
        player=p
    )


@bot.command(name="stats")
async def stats(ctx):
    p = get_player(ctx.author)
    atk, df = army_power(p)
    desc = (
        f"**HP:** {p['hp']}\n"
        f"**Leadership:** {p['skills']['leadership']}\n"
        f"**Warfare:** {p['skills']['warfare']}\n"
        f"**Trade:** {p['skills']['trade']}\n"
        f"**Charisma:** {p['skills']['charisma']}\n"
        f"**Attack:** {atk}\n"
        f"**Defense:** {df}"
    )
    await send_embed(ctx, "📊 Дэлгэрэнгүй Үзүүлэлт", desc, "profile", player=p)


@bot.command(name="rank")
async def rank_cmd(ctx):
    p = get_player(ctx.author)
    await send_embed(
        ctx,
        "🎖 Цол",
        f"**Одоогийн түвшин:** {p['level']}\n**Одоогийн цол:** {p['rank']}\n**Дараагийн түвшний EXP:** {xp_to_next(p['level'])}",
        "rank",
        player=p,
    )


@bot.command(name="xp")
async def xp_cmd(ctx):
    p = get_player(ctx.author)
    await send_embed(ctx, "✨ Туршлага", f"**EXP:** {p['xp']}/{xp_to_next(p['level'])}", "rank", player=p)


@bot.command(name="title")
async def title_cmd(ctx):
    p = get_player(ctx.author)
    await send_embed(ctx, "👑 Цол Нэр", f"Одоогийн цол нэр: **{p['title']}**", "rank", player=p)


@bot.command(name="settitle")
async def settitle(ctx, *, title: str):
    p = get_player(ctx.author)
    p["title"] = title[:50]
    save_data(data)
    await send_embed(ctx, "✍ Цол Нэр Шинэчлэгдлээ", f"Шинэ нэр: **{p['title']}**", "rank", player=p)


@bot.command(name="inventory", aliases=["bag"])
async def inventory(ctx):
    p = get_player(ctx.author)
    await send_embed(ctx, "🎒 Агуулах / Цүнх", fmt_inventory(p), "shop", player=p)


@bot.command(name="heal")
async def heal(ctx):
    p = get_player(ctx.author)
    cost = 120
    if p["money"] < cost:
        return await send_embed(ctx, "❌ Мөнгө Хүрэлцэхгүй", f"Эмчилгээний үнэ: **{cost}**", "profile", player=p, color=0xB22222)
    p["money"] -= cost
    p["hp"] = min(100 + p["level"], 300)
    save_data(data)
    await send_embed(ctx, "🩹 Эмчлэгдлээ", f"HP сэргээгдэв.\n**Үлдэгдэл мөнгө:** {p['money']}", "profile", player=p)

# ============================================================
# ECONOMY
# ============================================================
@bot.command(name="balance", aliases=["bal", "money"])
async def balance(ctx, member: discord.Member = None):
    member = member or ctx.author
    p = get_player(member)
    await send_embed(ctx, "💰 Санхүү", f"**Бэлэн мөнгө:** {p['money']}\n**Банк:** {p['bank']}", "economy", player=p)


@bot.command(name="bank")
async def bank(ctx):
    p = get_player(ctx.author)
    await send_embed(ctx, "🏦 Банк", f"**Хадгаламж:** {p['bank']} мөнгө", "economy", player=p)


@bot.command(name="deposit")
async def deposit(ctx, amount: str):
    p = get_player(ctx.author)
    amt = parse_amount(amount, p["money"])
    if amt is None or amt <= 0 or p["money"] < amt:
        return await send_embed(ctx, "❌ Алдаа", "Хадгалах мөнгө буруу байна.", "economy", player=p, color=0xB22222)
    p["money"] -= amt
    p["bank"] += amt
    save_data(data)
    await send_embed(ctx, "🏦 Банканд Хийв", f"**{amt}** мөнгө хадгаллаа.", "economy", player=p)


@bot.command(name="withdraw")
async def withdraw(ctx, amount: str):
    p = get_player(ctx.author)
    amt = parse_amount(amount, p["bank"])
    if amt is None or amt <= 0 or p["bank"] < amt:
        return await send_embed(ctx, "❌ Алдаа", "Татах мөнгө буруу байна.", "economy", player=p, color=0xB22222)
    p["bank"] -= amt
    p["money"] += amt
    save_data(data)
    await send_embed(ctx, "💸 Банкаас Авлаа", f"**{amt}** мөнгө гаргаж авлаа.", "economy", player=p)


@bot.command(name="work")
async def upgraded_work(ctx):
    p = get_player(ctx.author)
    ensure_player_upgrades(p)

    cooldown = get_work_cooldown(p)
    ok, rem = cd_ready(p, "work", cooldown)
    if not ok:
        return await send_embed(
            ctx,
            "⏳ Ажил Түр Хүлээгдэж Байна",
            f"Дахин ажиллах хүртэл **{rem} сек**.\n"
            f"Одоогийн cooldown: **{cooldown} сек**",
            "economy",
            player=p,
            color=0xCC8800
        )

    tier = get_work_tier(p["level"])
    update_work_streak(p)

    job, base_money, base_xp = random.choice(tier["jobs"])

    streak_bonus = 1 + (p["work_streak"] - 1) * 0.05
    trade_bonus = 1 + p["skills"].get("trade", 0) * 0.015
    level_bonus = 1 + min(0.35, p["level"] * 0.003)
    random_bonus = random.uniform(0.92, 1.18)

    final_money = int(base_money * streak_bonus * trade_bonus * level_bonus * random_bonus)
    final_xp = int(base_xp * (1 + p["skills"].get("charisma", 0) * 0.01 + min(0.25, p["level"] * 0.002)))

    special = []
    roll = random.random()

    if roll < 0.12:
        bonus = random.randint(60, 180)
        p["money"] += bonus
        special.append(f"🎁 Тусгай шагнал: **+{bonus} мөнгө**")
    elif roll < 0.22:
        inf = random.randint(1, 3)
        p["influence"] = p.get("influence", 0) + inf
        special.append(f"👑 Нөлөө өсөв: **+{inf}**")
    elif roll < 0.30:
        item = random.choice(["airag", "mah", "guril", "mod", "aris"])
        p["inventory"][item] = p["inventory"].get(item, 0) + 1
        special.append(f"📦 Олдвор: **{get_item_display(item)} x1**")

    p["money"] += final_money
    levels = add_xp(p, final_xp)
    set_cd(p, "work")
    save_data(data)

    extra = f"\n🎖 Level up: {', '.join(map(str, levels))}" if levels else ""
    specials = ("\n" + "\n".join(special)) if special else ""

    await ctx.send(
        embed=game_embed(
            "🛠 Сайжруулсан Ажил",
            f"**Ангилал:** {tier['name']}\n"
            f"**Үйлдэл:** Та **{job}**.\n\n"
            f"💰 **+{final_money} мөнгө**\n"
            f"✨ **+{final_xp} EXP**\n"
            f"🔥 **Streak:** {p['work_streak']}/7{extra}{specials}",
            category="economy",
            player=p,
            color=0xC89B3C
        )
    )


@bot.command(name="daily")
async def daily(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "daily", 86400)
    if not ok:
        return await send_embed(ctx, "⏳ Daily Бэлэн Биш", f"Үлдсэн хугацаа: **{rem // 3600} цаг**", "economy", player=p, color=0xCC8800)
    reward = 500 + p["level"] * 12
    p["money"] += reward
    p["influence"] += 3
    add_xp(p, 30)
    set_cd(p, "daily")
    save_data(data)
    await send_embed(ctx, "🌅 Daily Шагнал", f"**+{reward} мөнгө**\n**+3 нөлөө**\n**+30 EXP**", "economy", player=p)


@bot.command(name="weekly")
async def weekly(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "weekly", 604800)
    if not ok:
        return await send_embed(ctx, "⏳ Weekly Бэлэн Биш", f"Үлдсэн хугацаа: **{rem // 3600} цаг**", "economy", player=p, color=0xCC8800)
    reward = 3000 + p["level"] * 25
    p["money"] += reward
    p["influence"] += 10
    add_xp(p, 90)
    set_cd(p, "weekly")
    save_data(data)
    await send_embed(ctx, "📦 Weekly Шагнал", f"**+{reward} мөнгө**\n**+10 нөлөө**\n**+90 EXP**", "economy", player=p)


@bot.command(name="mine")
async def mine(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "mine", 480)
    if not ok:
        return await send_embed(ctx, "⏳ Уурхай", f"Дахин олборлох хүртэл **{rem} сек**", "craft", player=p, color=0xCC8800)
    gain = random.randint(2, 6)
    iron = random.randint(1, 4)
    p["resources"]["чулуу"] += gain
    p["resources"]["төмөр"] += iron
    p["money"] += 80
    add_xp(p, 18)
    set_cd(p, "mine")
    save_data(data)
    await send_embed(ctx, "⛏ Уурхай", f"**+{gain} чулуу**\n**+{iron} төмөр**\n**+80 мөнгө**", "craft", player=p)


@bot.command(name="hunt")
async def hunt(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "hunt", 420)
    if not ok:
        return await send_embed(ctx, "⏳ Ан", f"Дахин ан хийх хүртэл **{rem} сек**", "craft", player=p, color=0xCC8800)
    meat = random.randint(1, 4)
    hide = random.randint(1, 3)
    p["resources"]["мах"] += meat
    p["resources"]["арьс"] += hide
    p["money"] += 70
    add_xp(p, 16)
    set_cd(p, "hunt")
    save_data(data)
    await send_embed(ctx, "🏹 Ан", f"**+{meat} мах**\n**+{hide} арьс**\n**+70 мөнгө**", "craft", player=p)


@bot.command(name="farm")
async def farm(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "farm", 360)
    if not ok:
        return await send_embed(ctx, "⏳ Тариалан", f"Дахин тариалах хүртэл **{rem} сек**", "craft", player=p, color=0xCC8800)
    grain = random.randint(2, 7)
    p["resources"]["тариа"] += grain
    p["money"] += 60
    add_xp(p, 14)
    set_cd(p, "farm")
    save_data(data)
    await send_embed(ctx, "🌾 Тариалан", f"**+{grain} тариа**\n**+60 мөнгө**", "craft", player=p)


@bot.command(name="fish")
async def fish(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "fish", 360)
    if not ok:
        return await send_embed(ctx, "⏳ Загасчлал", f"Дахин загасчлах хүртэл **{rem} сек**", "craft", player=p, color=0xCC8800)
    money = random.randint(60, 140)
    p["money"] += money
    add_xp(p, 12)
    set_cd(p, "fish")
    save_data(data)
    await send_embed(ctx, "🎣 Загасчлал", f"**+{money} мөнгө**\n**+12 EXP**", "craft", player=p)


@bot.command(name="woodcut")
async def woodcut(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "woodcut", 420)
    if not ok:
        return await send_embed(ctx, "⏳ Мод Бэлтгэл", f"Дахин хийх хүртэл **{rem} сек**", "craft", player=p, color=0xCC8800)

    gain = random.randint(2, 6)
    p["resources"]["мод"] += gain
    p["money"] += 55
    add_xp(p, 13)
    set_cd(p, "woodcut")
    save_data(data)
    await send_embed(ctx, "🪓 Мод Бэлтгэл", f"**+{gain} мод**\n**+55 мөнгө**", "craft", player=p)


@bot.command(name="quarry")
async def quarry(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "quarry", 450)
    if not ok:
        return await send_embed(ctx, "⏳ Чулуу Олборлолт", f"Дахин хийх хүртэл **{rem} сек**", "craft", player=p, color=0xCC8800)

    gain = random.randint(2, 5)
    p["resources"]["чулуу"] += gain
    p["money"] += 65
    add_xp(p, 14)
    set_cd(p, "quarry")
    save_data(data)
    await send_embed(ctx, "🪨 Чулуу Олборлолт", f"**+{gain} чулуу**\n**+65 мөнгө**", "craft", player=p)


@bot.command(name="resources")
async def resources_cmd(ctx):
    p = get_player(ctx.author)
    res = p.get("resources", {})

    lines = [
        f"🪙 **Алт:** {res.get('алт', 0)}",
        f"🪵 **Мод:** {res.get('мод', 0)}",
        f"🪨 **Чулуу:** {res.get('чулуу', 0)}",
        f"⛓ **Төмөр:** {res.get('төмөр', 0)}",
        f"🧥 **Арьс:** {res.get('арьс', 0)}",
        f"🐎 **Морь:** {res.get('морь', 0)}",
        f"🌾 **Тариа:** {res.get('тариа', 0)}",
        f"🍖 **Мах:** {res.get('мах', 0)}",
    ]

    await send_embed(ctx, "🪵 Түүхий Эдийн Нөөц", "\n".join(lines), "craft", player=p)


@bot.command(name="tax")
async def tax(ctx):
    p = get_player(ctx.author)
    income = sum(data["cities"][c]["tax_base"] for c in p["cities"] if c in data["cities"])
    income = math.floor(income * (p["tax_rate"] / 100))
    await send_embed(ctx, "📜 Татвар", f"Хотуудаас авах боломжит татвар: **{income}**", "economy", player=p)


@bot.command(name="collecttax")
async def collecttax(ctx):
    p = get_player(ctx.author)
    ok, rem = cd_ready(p, "collecttax", 7200)
    if not ok:
        return await send_embed(ctx, "⏳ Татвар", f"Дахин татвар авах хүртэл **{rem // 60} мин**", "economy", player=p, color=0xCC8800)
    income = sum(data["cities"][c]["tax_base"] for c in p["cities"] if c in data["cities"])
    income = math.floor(income * (p["tax_rate"] / 100))
    if income <= 0:
        return await send_embed(ctx, "🏙 Хот Алга", "Та одоогоор эзэлсэн хотгүй байна.", "economy", player=p)
    p["money"] += income
    p["influence"] += max(1, len(p["cities"]))
    set_cd(p, "collecttax")
    save_data(data)
    await send_embed(ctx, "💰 Татвар Хураалаа", f"**+{income} мөнгө**\n**+{len(p['cities'])} нөлөө**", "economy", player=p)

# ============================================================
# SHOP / MARKET
# ============================================================
@bot.command(name="shop")
async def upgraded_shop(ctx):
    p = get_player(ctx.author)
    ensure_player_upgrades(p)

    desc = format_shop_lines(p)
    desc += (
        f"\n\n**🎯 Таны худалдааны урамшуулал**\n"
        f"• Хөнгөлөлт: **{int(p.get('market_discount', 0) * 100)}%**\n"
        f"• Trade skill: **{p['skills'].get('trade', 0)}**\n\n"
        f"**Коммандууд**\n"
        f"• Авах: `{PREFIX}buy item amount`\n"
        f"• Зарах: `{PREFIX}sell item amount`\n"
        f"• Үнэ шалгах: `{PREFIX}price item`\n"
        f"• Зах тайлан: `{PREFIX}market`\n"
        f"• Хар зах: `{PREFIX}blackmarket`"
    )
    await send_embed(ctx, "🛒 Их Захын Дэлгүүр", desc, "shop", player=p)


@bot.command(name="price")
async def upgraded_price(ctx, item: str = None):
    p = get_player(ctx.author)
    ensure_player_upgrades(p)

    if not item:
        return await send_embed(
            ctx,
            "❌ Ашиглалт",
            f"`{PREFIX}price item` гэж ашиглана.",
            "shop",
            player=p,
            color=0xB22222
        )

    item = item.lower()

    if item in SHOP_ITEMS:
        buy_price = get_dynamic_price(item, p, "buy")
        sell_price = get_dynamic_price(item, p, "sell")
        await send_embed(
            ctx,
            "💲 Зах Зээлийн Үнэ",
            f"**Бараа:** {get_item_display(item)} (`{item}`)\n"
            f"**Худалдаж авах үнэ:** {buy_price}\n"
            f"**Буцаан зарах үнэ:** {sell_price}\n"
            f"**Суурь үнэ:** {SHOP_ITEMS[item]['price']}",
            "shop",
            player=p
        )
        return

    if item in BLACKMARKET_ITEMS:
        bm_price = get_blackmarket_price(item, p)
        await send_embed(
            ctx,
            "🕶 Хар Захын Үнэ",
            f"**{BLACKMARKET_ITEMS[item]['name']}**\n"
            f"**Одоогийн үнэ:** **{bm_price}**\n"
            f"**Суурь үнэ:** **{BLACKMARKET_ITEMS[item]['price']}**",
            "shop",
            player=p
        )
        return

    await send_embed(ctx, "❌ Олдсонгүй", "Тэр бараа зах дээр алга.", "shop", player=p, color=0xB22222)


@bot.command(name="buy")
async def upgraded_buy(ctx, item: str = None, amount: int = 1):
    p = get_player(ctx.author)
    ensure_player_upgrades(p)

    if not item:
        return await send_embed(
            ctx,
            "❌ Ашиглалт",
            f"`{PREFIX}buy item amount` гэж ашиглана.",
            "shop",
            player=p,
            color=0xB22222
        )

    item = item.lower()

    if amount <= 0:
        return await send_embed(ctx, "❌ Алдаа", "Тоо хэмжээ буруу байна.", "shop", player=p, color=0xB22222)

    if item in SHOP_ITEMS:
        unit_price = get_dynamic_price(item, p, "buy")
        total = unit_price * amount

        if p["money"] < total:
            return await send_embed(
                ctx,
                "❌ Мөнгө Хүрэлцэхгүй",
                f"**{get_item_display(item)} x{amount}** авахад **{total} мөнгө** хэрэгтэй.",
                "shop",
                player=p,
                color=0xB22222
            )

        p["money"] -= total
        p["inventory"][item] = p["inventory"].get(item, 0) + amount
        p["shop_stats"]["bought"] += amount

        if random.random() < 0.10:
            p["market_discount"] = min(0.15, p.get("market_discount", 0) + 0.01)

        add_xp(p, max(4, amount * 2))
        save_data(data)

        return await send_embed(
            ctx,
            "✅ Амжилттай Худалдаж Авлаа",
            f"**{get_item_display(item)} x{amount}**\n"
            f"**Нэгж үнэ:** {unit_price}\n"
            f"**Нийт:** -{total} мөнгө",
            "shop",
            player=p,
            color=0x2E8B57
        )

    if item in BLACKMARKET_ITEMS:
        if p["level"] < 25:
            return await send_embed(
                ctx,
                "⛔ Хар Зах Хаалттай",
                "Хар захаас авахын тулд дор хаяж **Level 25** хэрэгтэй.",
                "shop",
                player=p,
                color=0xB22222
            )

        offers = get_blackmarket_offers(p)
        if item not in offers:
            return await send_embed(
                ctx,
                "🚫 Хар Захад Алга",
                "Энэ цагт тэр бараа гарч ирээгүй байна.",
                "shop",
                player=p,
                color=0xB22222
            )

        unit_price = get_blackmarket_price(item, p)
        total = unit_price * amount

        if p["money"] < total:
            return await send_embed(
                ctx,
                "❌ Мөнгө Хүрэлцэхгүй",
                f"Нийт үнэ: **{total}**",
                "shop",
                player=p,
                color=0xB22222
            )

        p["money"] -= total
        p["inventory"][item] = p["inventory"].get(item, 0) + amount
        p["wanted"] = p.get("wanted", 0) + random.randint(0, amount)
        p["shop_stats"]["bought"] += amount
        add_xp(p, 10 + amount * 3)
        save_data(data)

        return await send_embed(
            ctx,
            "🕶 Хар Захын Наймаа Амжилттай",
            f"**{BLACKMARKET_ITEMS[item]['name']} x{amount}**\n"
            f"**Нэгж үнэ:** {unit_price}\n"
            f"**Нийт:** -{total} мөнгө\n"
            f"**Wanted:** {p['wanted']}",
            "shop",
            player=p,
            color=0x6B2E8F
        )

    await send_embed(ctx, "❌ Алдаа", "Ийм бараа байхгүй.", "shop", player=p, color=0xB22222)


@bot.command(name="sell")
async def upgraded_sell(ctx, item: str = None, amount: str = "1"):
    p = get_player(ctx.author)
    ensure_player_upgrades(p)

    if not item:
        return await send_embed(
            ctx,
            "❌ Ашиглалт",
            f"`{PREFIX}sell item amount` гэж ашиглана.",
            "shop",
            player=p,
            color=0xB22222
        )

    item = item.lower()

    if item not in p["inventory"] or p["inventory"].get(item, 0) <= 0:
        return await send_embed(ctx, "❌ Алдаа", "Танд энэ бараа байхгүй.", "shop", player=p, color=0xB22222)

    max_have = p["inventory"].get(item, 0)
    amt = parse_amount(amount, max_have)

    if amt is None or amt <= 0 or amt > max_have:
        return await send_embed(ctx, "❌ Алдаа", "Зарах тоо хэмжээ буруу байна.", "shop", player=p, color=0xB22222)

    if item in SHOP_ITEMS:
        unit_price = get_dynamic_price(item, p, "sell")
    elif item in BLACKMARKET_ITEMS:
        unit_price = max(1, int(get_blackmarket_price(item, p) * 0.45))
    else:
        unit_price = 10

    total = unit_price * amt
    p["inventory"][item] -= amt
    if p["inventory"][item] <= 0:
        del p["inventory"][item]

    p["money"] += total
    p["shop_stats"]["sold"] += amt

    if random.random() < 0.14:
        bonus = random.randint(1, 2)
        p["skills"]["trade"] = p["skills"].get("trade", 0) + bonus
        trade_text = f"\n📈 Trade skill **+{bonus}**"
    else:
        trade_text = ""

    save_data(data)

    await send_embed(
        ctx,
        "💸 Амжилттай Зарлаа",
        f"**{get_item_display(item)} x{amt}**\n"
        f"**Нэгж үнэ:** {unit_price}\n"
        f"**Нийт:** +{total} мөнгө{trade_text}",
        "shop",
        player=p,
        color=0x2E8B57
    )


@bot.command(name="market")
async def upgraded_market(ctx):
    p = get_player(ctx.author)
    ensure_player_upgrades(p)

    hot_items = []
    low_items = []

    for item_key in SHOP_ITEMS.keys():
        today_price = get_dynamic_price(item_key, p, "buy")
        base = max(1, SHOP_ITEMS[item_key]["price"])
        ratio = today_price / base

        if ratio >= 1.10:
            hot_items.append(f"🔥 **{get_item_display(item_key)}** — {today_price}")
        elif ratio <= 0.92:
            low_items.append(f"💚 **{get_item_display(item_key)}** — {today_price}")

    desc = (
        f"**{EMOJIS['market']} Өнөөдрийн Зах Зээл**\n\n"
        f"**💚 Хямдарсан бараа:**\n{chr(10).join(low_items[:5]) if low_items else 'Одоогоор байхгүй'}\n\n"
        f"**🔥 Өссөн бараа:**\n{chr(10).join(hot_items[:5]) if hot_items else 'Одоогоор байхгүй'}\n\n"
        f"**📊 Таны худалдааны үзүүлэлт**\n"
        f"• Авсан: **{p['shop_stats']['bought']}**\n"
        f"• Зарсан: **{p['shop_stats']['sold']}**\n"
        f"• Trade skill: **{p['skills'].get('trade', 0)}**\n"
        f"• Хөнгөлөлт: **{int(p.get('market_discount', 0) * 100)}%**"
    )
    await send_embed(ctx, "🏪 Зах Зээлийн Тайлан", desc, "shop", player=p)


@bot.command(name="blackmarket")
async def upgraded_blackmarket(ctx):
    p = get_player(ctx.author)
    ensure_player_upgrades(p)

    if p["level"] < 25:
        return await send_embed(
            ctx,
            "⛔ Хар Зах Нээгдээгүй",
            "Хар зах ашиглахын тулд **Level 25** хүрэх хэрэгтэй.",
            "shop",
            player=p,
            color=0xB22222
        )

    offers = get_blackmarket_offers(p)
    lines = []

    for key in offers:
        item = BLACKMARKET_ITEMS[key]
        dyn_price = get_blackmarket_price(key, p)
        lines.append(
            f"**{key}** — {item['name']}\n"
            f"Үнэ: **{dyn_price}** | Төрөл: **{item['type']}**"
        )

    desc = (
        "Эндхүү бараанууд цаг тутамд өөрчлөгдөнө.\n"
        f"Худалдаж авах: `{PREFIX}buy item amount`\n\n"
        + "\n\n".join(lines) +
        f"\n\n**Wanted түвшин:** {p['wanted']}"
    )
    await send_embed(ctx, "🕶 Нууц Хар Зах", desc, "shop", player=p, color=0x5B2C6F)


@bot.command(name="craft")
async def craft(ctx, recipe: str = "sword"):
    p = get_player(ctx.author)
    recipe = recipe.lower()
    if recipe == "sword":
        if p["resources"]["төмөр"] < 3 or p["resources"]["мод"] < 1:
            return await send_embed(ctx, "❌ Нөөц Дутуу", "Сэлэм хийхэд 3 төмөр, 1 мод хэрэгтэй.", "craft", player=p, color=0xB22222)
        p["resources"]["төмөр"] -= 3
        p["resources"]["мод"] -= 1
        p["inventory"]["sword"] = p["inventory"].get("sword", 0) + 1
        add_xp(p, 20)
        save_data(data)
        return await send_embed(ctx, "🗡 Урлалаа", "**sword x1** бүтээв.", "craft", player=p)
    await send_embed(ctx, "🛠 Урлал", "Одоогоор `sword` жор идэвхтэй байна.", "craft", player=p)

# ============================================================
# ARMY
# ============================================================
@bot.command(name="units")
async def units(ctx):
    p = get_player(ctx.author)
    lines = []
    for key, s in UNIT_STATS.items():
        lines.append(f"**{key}** → {s['name']} | үнэ {s['cost']} | atk {s['power']} | def {s['defense']}")
    await send_embed(ctx, "🐎 Цэргийн Нэгжүүд", "\n".join(lines), "army", player=p)


@bot.command(name="recruit")
async def recruit(ctx, unit: str, amount: int = 1):
    p = get_player(ctx.author)
    unit = unit.lower()
    if unit not in UNIT_STATS or amount <= 0:
        return await send_embed(ctx, "❌ Алдаа", "Ийм нэгж байхгүй.", "army", player=p, color=0xB22222)
    cost = UNIT_STATS[unit]["cost"] * amount
    if p["money"] < cost:
        return await send_embed(ctx, "❌ Мөнгө Хүрэхгүй", f"Шаардлагатай: **{cost}**", "army", player=p, color=0xB22222)
    p["money"] -= cost
    p["army"][unit] += amount
    add_xp(p, max(8, amount * 2))
    save_data(data)
    await send_embed(ctx, "⚔ Цэрэг Элслээ", f"**{UNIT_STATS[unit]['name']} x{amount}**\n**-{cost} мөнгө**", "army", player=p)


@bot.command(name="army")
async def army(ctx, member: discord.Member = None):
    member = member or ctx.author
    p = get_player(member)
    atk, df = army_power(p)
    desc = f"{fmt_army(p)}\n\n**Нийт Attack:** {atk}\n**Нийт Defense:** {df}"
    await send_embed(ctx, f"🛡 {member.display_name}-ийн Арми", desc, "army", player=p)


@bot.command(name="disband")
async def disband(ctx, unit: str, amount: int = 1):
    p = get_player(ctx.author)
    unit = unit.lower()
    if unit not in UNIT_STATS or amount <= 0 or p["army"][unit] < amount:
        return await send_embed(ctx, "❌ Алдаа", "Тараах цэрэг хүрэлцэхгүй.", "army", player=p, color=0xB22222)
    refund = int(UNIT_STATS[unit]["cost"] * amount * 0.35)
    p["army"][unit] -= amount
    p["money"] += refund
    save_data(data)
    await send_embed(ctx, "📉 Цэрэг Тараалаа", f"**{UNIT_STATS[unit]['name']} x{amount}**\n**+{refund} мөнгө**", "army", player=p)


@bot.command(name="fortify")
async def fortify(ctx):
    p = get_player(ctx.author)
    p["province_power"] += 15
    add_xp(p, 12)
    save_data(data)
    await send_embed(ctx, "🏰 Бэхлэлт", "Таны хамгаалалтын чадал **+15** нэмэгдлээ.", "army", player=p)


@bot.command(name="scout")
async def scout(ctx):
    p = get_player(ctx.author)
    city = random.choice(list(data["cities"].keys()))
    c = data["cities"][city]
    owner = c["owner"] or "Төвийг сахисан"
    await send_embed(ctx, "🕵 Тагнуул", f"**{city}**\nЭзэн: **{owner}**\nХамгаалалт: **{c['defense']}**\nБаялаг: **{c['tax_base']}**", "battle", player=p)


@bot.command(name="train")
async def train(ctx):
    p = get_player(ctx.author)
    cost = 200
    if p["money"] < cost:
        return await send_embed(ctx, "❌ Мөнгө Хүрэлцэхгүй", f"Сургалтын үнэ: **{cost}**", "army", player=p, color=0xB22222)
    p["money"] -= cost
    p["skills"]["warfare"] += 1
    p["skills"]["leadership"] += 1
    add_xp(p, 25)
    save_data(data)
    await send_embed(ctx, "🏇 Сургуулилт", "**Warfare +1**\n**Leadership +1**", "army", player=p)


@bot.command(name="garrison")
async def garrison(ctx, *, city: str):
    p = get_player(ctx.author)
    city = city.title()
    if city not in p["cities"]:
        return await send_embed(ctx, "❌ Алдаа", "Тэр хот таны мэдэлд алга.", "conquest", player=p, color=0xB22222)
    data["cities"][city]["defense"] += 25
    save_data(data)
    await send_embed(ctx, "🛡 Хотод Цэрэг Байршууллаа", f"**{city}** хамгаалалт **+25**", "conquest", player=p)


@bot.command(name="patrol")
async def patrol(ctx):
    p = get_player(ctx.author)
    money = random.randint(70, 150)
    p["money"] += money
    p["influence"] += 1
    add_xp(p, 14)
    save_data(data)
    await send_embed(ctx, "🚩 Эргүүл", f"Зам хянаж **+{money} мөнгө**, **+1 нөлөө** авлаа.", "army", player=p)

# ============================================================
# CONQUEST / WAR
# ============================================================
@bot.command(name="cities")
async def cities(ctx):
    p = get_player(ctx.author)
    lines = []
    for city, c in data["cities"].items():
        owner = c["owner"] or "Төвийг сахисан"
        lines.append(f"**{city}** — Эзэн: {owner} | Defense: {c['defense']} | Tax: {c['tax_base']}")
    await send_embed(ctx, "🏙 Хотууд", "\n".join(lines[:15]), "conquest", player=p)


@bot.command(name="city")
async def city(ctx, *, city_name: str):
    p = get_player(ctx.author)
    city_name = city_name.title()
    if city_name not in data["cities"]:
        return await send_embed(ctx, "❌ Олдсонгүй", "Тэр хот бүртгэлгүй байна.", "conquest", player=p, color=0xB22222)
    c = data["cities"][city_name]
    owner = c["owner"] or "Төвийг сахисан"
    await send_embed(ctx, f"🏙 {city_name}", f"**Эзэн:** {owner}\n**Defense:** {c['defense']}\n**Prosperity:** {c['prosperity']}\n**Tax Base:** {c['tax_base']}", "conquest", player=p)


@bot.command(name="conquer")
async def conquer(ctx, *, city_name: str):
    city_name = city_name.title()
    p = get_player(ctx.author)

    if city_name not in data["cities"]:
        return await send_embed(ctx, "❌ Хот Олдсонгүй", "Ийм хот байхгүй.", "conquest", player=p, color=0xB22222)

    atk, _ = army_power(p)
    city = data["cities"][city_name]
    need = city["defense"]
    bonus = p["level"] * 2 + p["province_power"]
    total = atk + bonus + random.randint(-80, 120)

    if total >= need:
        old_owner = city["owner"]
        city["owner"] = ctx.author.display_name

        if old_owner and old_owner != ctx.author.display_name:
            for _, other_player in data["players"].items():
                if other_player.get("name") == old_owner and city_name in other_player.get("cities", []):
                    other_player["cities"].remove(city_name)
                    break

        if city_name not in p["cities"]:
            p["cities"].append(city_name)

        city["defense"] = max(80, city["defense"] - random.randint(15, 40))
        p["wins"] += 1
        p["money"] += city["tax_base"]
        p["influence"] += 8
        add_xp(p, 80)
        save_data(data)

        return await send_embed(
            ctx,
            "🏴 Хот Эзлэгдлээ",
            f"Та **{city_name}** хотыг эзэллээ!\n"
            f"💰 **+{city['tax_base']} мөнгө**\n"
            f"⭐ **+8 нөлөө**",
            "conquest",
            player=p,
            color=0x2E8B57
        )

    p["losses"] += 1
    losses = {}
    for u in p["army"]:
        lost = min(p["army"][u], random.randint(0, max(0, p["army"][u] // 12)))
        p["army"][u] -= lost
        if lost:
            losses[u] = lost

    save_data(data)
    text = "\n".join(f"• {UNIT_STATS[k]['name']}: -{v}" for k, v in losses.items()) or "Хохирол бага байв."
    await send_embed(ctx, "💥 Довтолгоо Амжилтгүй", f"**{city_name}** хамгаалалтыг нэвтэлж чадсангүй.\n\n{text}", "battle", player=p, color=0xB22222)


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
        return await send_embed(ctx, "⚔ Дайралтанд Яллаа", f"**{member.display_name}** дээр ялалт байгууллаа.\n**Олз:** {loot} мөнгө", "battle", player=attacker, color=0x2E8B57)
    attacker["losses"] += 1
    defender["wins"] += 1
    save_data(data)
    await send_embed(ctx, "🩸 Дайралт Амжилтгүй", f"**{member.display_name}** таныг няцаалаа.", "battle", player=attacker, color=0xB22222)


@bot.command(name="raid")
async def raid(ctx):
    p = get_player(ctx.author)
    money = random.randint(100, 260)
    risk = random.random()
    if risk < 0.3:
        loss = random.randint(50, 120)
        p["money"] = max(0, p["money"] - loss)
        save_data(data)
        return await send_embed(ctx, "🔥 Дээрэм Бүтэлгүйтэв", f"**-{loss} мөнгө** алдав.", "battle", player=p, color=0xB22222)
    p["money"] += money
    add_xp(p, 20)
    save_data(data)
    await send_embed(ctx, "🔥 Амжилттай Дээрэм", f"**+{money} мөнгө**\n**+20 EXP**", "battle", player=p)


@bot.command(name="defendcity")
async def defendcity(ctx, *, city_name: str):
    city_name = city_name.title()
    p = get_player(ctx.author)
    if city_name not in p["cities"]:
        return await send_embed(ctx, "❌ Алдаа", "Та энэ хотыг эзэмшдэггүй.", "conquest", player=p, color=0xB22222)
    data["cities"][city_name]["defense"] += 40
    save_data(data)
    await send_embed(ctx, "🛡 Хамгаалалтыг Зузаатгав", f"**{city_name}** defense **+40**", "conquest", player=p)


@bot.command(name="siege")
async def siege(ctx, *, city_name: str):
    p = get_player(ctx.author)
    city_name = city_name.title()
    if city_name not in data["cities"]:
        return await send_embed(ctx, "❌ Олдсонгүй", "Ийм хот алга.", "conquest", player=p, color=0xB22222)
    reduce = random.randint(15, 45)
    data["cities"][city_name]["defense"] = max(40, data["cities"][city_name]["defense"] - reduce)
    save_data(data)
    await send_embed(ctx, "🏹 Бүслэлт", f"**{city_name}** хамгаалалт **-{reduce}** буурлаа.", "battle", player=p)


@bot.command(name="march")
async def march(ctx):
    p = get_player(ctx.author)
    await send_embed(ctx, "🐎 Аян", "Арми чинь тал нутгаар хөдөлж, дайнд бэлтгэж байна.", "travel", player=p)


@bot.command(name="camp")
async def camp(ctx):
    p = get_player(ctx.author)
    max_hp = min(100 + p["level"], 300)
    before = p["hp"]
    p["hp"] = min(max_hp, p["hp"] + 35)
    heal_amount = p["hp"] - before
    save_data(data)
    await send_embed(
        ctx,
        "⛺ Хээрийн Отог",
        f"Амарч хүчээ сэлбэв.\n**HP сэргэлт:** +{heal_amount}\n**Одоогийн HP:** {p['hp']}/{max_hp}",
        "travel",
        player=p
    )


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
        return await send_embed(ctx, "❌ Алдаа", "Та аль хэдийн овогт харьяалагдаж байна.", "clan", player=p, color=0xB22222)
    name = name[:30]
    if name in data["clans"]:
        return await send_embed(ctx, "❌ Давхцал", "Ийм овог аль хэдийн байна.", "clan", player=p, color=0xB22222)
    data["clans"][name] = {"leader": ctx.author.id, "members": [ctx.author.id], "vault": 0, "power": 0}
    p["clan"] = name
    save_data(data)
    await send_embed(ctx, "🐺 Овог Байгуулагдлаа", f"Шинэ овог: **{name}**", "clan", player=p)


@bot.command(name="claninfo")
async def claninfo(ctx, *, name: str = None):
    p = get_player(ctx.author)
    target = name or p["clan"]
    if not target or target not in data["clans"]:
        return await send_embed(ctx, "❌ Олдсонгүй", "Овог олдсонгүй.", "clan", player=p, color=0xB22222)
    c = data["clans"][target]
    members = len(c["members"])
    leader_member = ctx.guild.get_member(c["leader"]) if ctx.guild else None
    leader_name = leader_member.display_name if leader_member else str(c["leader"])
    await send_embed(ctx, f"🐺 {target}", f"**Ахлагч:** {leader_name}\n**Гишүүд:** {members}\n**Сан:** {c['vault']}\n**Хүч:** {c['power']}", "clan", player=p)


@bot.command(name="clanjoin")
async def clanjoin(ctx, *, name: str):
    p = get_player(ctx.author)
    if p["clan"]:
        return await send_embed(ctx, "❌ Алдаа", "Эхлээд одоогийн овгоосоо гар.", "clan", player=p, color=0xB22222)
    if name not in data["clans"]:
        return await send_embed(ctx, "❌ Олдсонгүй", "Тэр овог байхгүй.", "clan", player=p, color=0xB22222)
    if ctx.author.id not in data["clans"][name]["members"]:
        data["clans"][name]["members"].append(ctx.author.id)
    p["clan"] = name
    save_data(data)
    await send_embed(ctx, "🤝 Овогт Нэгдлээ", f"Та **{name}** овогт орлоо.", "clan", player=p)


@bot.command(name="clanleave")
async def clanleave(ctx):
    p = get_player(ctx.author)
    clan = p["clan"]
    if not clan or clan not in data["clans"]:
        return await send_embed(ctx, "❌ Алдаа", "Та овоггүй байна.", "clan", player=p, color=0xB22222)
    if ctx.author.id in data["clans"][clan]["members"]:
        data["clans"][clan]["members"].remove(ctx.author.id)
    p["clan"] = None
    save_data(data)
    await send_embed(ctx, "🚪 Овгоос Гарлаа", f"Та **{clan}** овгоос гарлаа.", "clan", player=p)


@bot.command(name="clandonate")
async def clandonate(ctx, amount: int):
    p = get_player(ctx.author)
    clan = p["clan"]
    if not clan or clan not in data["clans"]:
        return await send_embed(ctx, "❌ Овоггүй", "Овогт нэгдсэний дараа ашигла.", "clan", player=p, color=0xB22222)
    if amount <= 0 or p["money"] < amount:
        return await send_embed(ctx, "❌ Алдаа", "Хандивын хэмжээ буруу.", "clan", player=p, color=0xB22222)
    p["money"] -= amount
    data["clans"][clan]["vault"] += amount
    data["clans"][clan]["power"] += amount // 50
    save_data(data)
    await send_embed(ctx, "🏦 Овгийн Санд Хандив", f"**{clan}** санд **{amount}** өглөө.", "clan", player=p)


@bot.command(name="clanvault")
async def clanvault(ctx):
    p = get_player(ctx.author)
    clan = p["clan"]
    if not clan or clan not in data["clans"]:
        return await send_embed(ctx, "❌ Овоггүй", "Та овоггүй байна.", "clan", player=p, color=0xB22222)
    await send_embed(ctx, "🏛 Овгийн Сан", f"**{clan}** сан: **{data['clans'][clan]['vault']}**", "clan", player=p)


@bot.command(name="clanwar")
async def clanwar(ctx, *, enemy: str):
    p = get_player(ctx.author)
    clan = p["clan"]
    if not clan or clan not in data["clans"] or enemy not in data["clans"]:
        return await send_embed(ctx, "❌ Алдаа", "Хоёр овог хоёулаа бүртгэлтэй байх ёстой.", "clan", player=p, color=0xB22222)
    our = data["clans"][clan]["power"] + random.randint(0, 150)
    their = data["clans"][enemy]["power"] + random.randint(0, 150)
    if our >= their:
        data["clans"][clan]["vault"] += 500
        save_data(data)
        return await send_embed(ctx, "⚔ Овгийн Дайн", f"**{clan}** овог **{enemy}**-г яллаа!\n**+500 сан**", "clan", player=p, color=0x2E8B57)
    await send_embed(ctx, "🩸 Овгийн Дайн", f"**{enemy}** овог энэ удаад давуу байлаа.", "clan", player=p, color=0xB22222)

# ============================================================
# LEADERBOARDS
# ============================================================
async def board(ctx, key, title, category="rank", reverse=True):
    p = get_player(ctx.author)
    players = list(data["players"].items())
    players.sort(key=lambda x: x[1].get(key, 0), reverse=reverse)
    lines = []
    for i, (_, pl) in enumerate(players[:10], start=1):
        lines.append(f"**#{i}** {pl['name']} — {pl.get(key, 0)}")
    await send_embed(ctx, title, "\n".join(lines) or "Өгөгдөл алга.", category, player=p)


@bot.command(name="leaderboard")
async def leaderboard(ctx):
    await board(ctx, "level", "🏆 Level Leaderboard", "rank")


@bot.command(name="topmoney")
async def topmoney(ctx):
    p = get_player(ctx.author)
    players = list(data["players"].values())
    players.sort(key=lambda pl: pl.get("money", 0) + pl.get("bank", 0), reverse=True)
    lines = [f"**#{i}** {pl['name']} — {pl['money'] + pl['bank']}" for i, pl in enumerate(players[:10], 1)]
    await send_embed(ctx, "💰 Шилдэг Баячууд", "\n".join(lines) or "Өгөгдөл алга.", "economy", player=p)


@bot.command(name="toplevel")
async def toplevel(ctx):
    await board(ctx, "level", "🎖 Шилдэг Түвшин", "rank")


@bot.command(name="topwar")
async def topwar(ctx):
    await board(ctx, "wins", "⚔ Шилдэг Байлдан Дийлэгчид", "battle")


@bot.command(name="topcities")
async def topcities(ctx):
    p = get_player(ctx.author)
    players = list(data["players"].values())
    players.sort(key=lambda pl: len(pl.get("cities", [])), reverse=True)
    lines = [f"**#{i}** {pl['name']} — {len(pl.get('cities', []))} хот" for i, pl in enumerate(players[:10], 1)]
    await send_embed(ctx, "🏙 Хот Эзэмшигчид", "\n".join(lines) or "Өгөгдөл алга.", "conquest", player=p)


@bot.command(name="topclans")
async def topclans(ctx):
    p = get_player(ctx.author)
    clans = list(data["clans"].items())
    clans.sort(key=lambda x: x[1].get("power", 0), reverse=True)
    lines = [f"**#{i}** {name} — хүч {c['power']} | сан {c['vault']}" for i, (name, c) in enumerate(clans[:10], 1)]
    await send_embed(ctx, "🐺 Шилдэг Овгууд", "\n".join(lines) or "Өгөгдөл алга.", "clan", player=p)

# ============================================================
# ADMIN COMMANDS
# ============================================================
@bot.command(name="adminhelp")
@is_admin()
async def adminhelp(ctx):
    p = get_player(ctx.author)
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
    await send_embed(ctx, "🛡 Админ Комманд", desc, "admin", player=p)


@bot.command(name="give")
@is_admin()
async def give(ctx, member: discord.Member, amount: int):
    admin_p = get_player(ctx.author)
    p = get_player(member)
    p["money"] += max(0, amount)
    save_data(data)
    await send_embed(ctx, "✅ Мөнгө Олголоо", f"**{member.display_name}** → **+{amount}**", "admin", player=admin_p)


@bot.command(name="setmoney")
@is_admin()
async def setmoney(ctx, member: discord.Member, amount: int):
    admin_p = get_player(ctx.author)
    p = get_player(member)
    p["money"] = max(0, amount)
    save_data(data)
    await send_embed(ctx, "💰 Мөнгө Тохирууллаа", f"**{member.display_name}** = **{amount}**", "admin", player=admin_p)


@bot.command(name="setlevel")
@is_admin()
async def setlevel(ctx, member: discord.Member, level: int):
    admin_p = get_player(ctx.author)
    p = get_player(member)
    p["level"] = max(1, min(MAX_LEVEL, level))
    p["rank"] = get_rank(p["level"])
    p["xp"] = 0
    p["hp"] = min(100 + p["level"], 300)
    save_data(data)
    await send_embed(ctx, "🎖 Түвшин Тохирууллаа", f"**{member.display_name}** = Level **{p['level']}** ({p['rank']})", "admin", player=admin_p)


@bot.command(name="addxp")
@is_admin()
async def addxp_admin(ctx, member: discord.Member, amount: int):
    admin_p = get_player(ctx.author)
    p = get_player(member)
    add_xp(p, max(0, amount))
    save_data(data)
    await send_embed(ctx, "✨ EXP Нэмлээ", f"**{member.display_name}** → **+{amount} EXP**", "admin", player=admin_p)


@bot.command(name="resetplayer")
@is_admin()
async def resetplayer(ctx, member: discord.Member):
    admin_p = get_player(ctx.author)
    data["players"][uid(member.id)] = default_player(member)
    save_data(data)
    await send_embed(ctx, "♻ Тоглогч Шинэчлэгдэв", f"**{member.display_name}** бүрэн reset хийгдлээ.", "admin", player=admin_p)


@bot.command(name="wipecity")
@is_admin()
async def wipecity(ctx, *, city_name: str):
    admin_p = get_player(ctx.author)
    city_name = city_name.title()
    if city_name not in data["cities"]:
        return await send_embed(ctx, "❌ Олдсонгүй", "Ийм хот алга.", "admin", player=admin_p, color=0xB22222)
    data["cities"][city_name]["owner"] = None
    data["cities"][city_name]["defense"] = random.randint(120, 380)
    save_data(data)
    await send_embed(ctx, "🏙 Хот Чөлөөлөгдлөө", f"**{city_name}** neutral төлөвт шилжив.", "admin", player=admin_p)


@bot.command(name="announce")
@is_admin()
async def announce(ctx, *, text: str):
    admin_p = get_player(ctx.author)
    await ctx.send(
        embed=game_embed(
            "📣 Эзэнт Гүрний Зарлиг",
            text,
            category="admin",
            player=admin_p,
            color=0xD4AF37
        )
    )


@bot.command(name="settitleadmin")
@is_admin()
async def settitleadmin(ctx, member: discord.Member, *, text: str):
    admin_p = get_player(ctx.author)
    p = get_player(member)
    p["title"] = text[:50]
    save_data(data)
    await send_embed(ctx, "✍ Админ Цол Нэр", f"**{member.display_name}** → **{p['title']}**", "admin", player=admin_p)


@bot.command(name="giveunit")
@is_admin()
async def giveunit(ctx, member: discord.Member, unit: str, amount: int):
    admin_p = get_player(ctx.author)
    unit = unit.lower()
    if unit not in UNIT_STATS:
        return await send_embed(ctx, "❌ Нэгж Олдсонгүй", "Буруу нэгжийн нэр.", "admin", player=admin_p, color=0xB22222)
    p = get_player(member)
    p["army"][unit] += max(0, amount)
    save_data(data)
    await send_embed(ctx, "🐎 Цэрэг Олголоо", f"**{member.display_name}** → **{UNIT_STATS[unit]['name']} x{amount}**", "admin", player=admin_p)


@bot.command(name="takeunit")
@is_admin()
async def takeunit(ctx, member: discord.Member, unit: str, amount: int):
    admin_p = get_player(ctx.author)
    unit = unit.lower()
    if unit not in UNIT_STATS:
        return await send_embed(ctx, "❌ Нэгж Олдсонгүй", "Буруу нэгжийн нэр.", "admin", player=admin_p, color=0xB22222)
    p = get_player(member)
    p["army"][unit] = max(0, p["army"][unit] - max(0, amount))
    save_data(data)
    await send_embed(ctx, "📉 Цэрэг Хаслаа", f"**{member.display_name}** → **{UNIT_STATS[unit]['name']} -{amount}**", "admin", player=admin_p)


@bot.command(name="setcityowner")
@is_admin()
async def setcityowner(ctx, city_name: str, member: discord.Member):
    admin_p = get_player(ctx.author)
    city_name = city_name.title()

    if city_name not in data["cities"]:
        return await send_embed(ctx, "❌ Хот Алга", "Ийм хот бүртгэлгүй.", "admin", player=admin_p, color=0xB22222)

    old_owner = data["cities"][city_name]["owner"]

    if old_owner and old_owner != member.display_name:
        for _, other_player in data["players"].items():
            if other_player.get("name") == old_owner and city_name in other_player.get("cities", []):
                other_player["cities"].remove(city_name)
                break

    p = get_player(member)
    data["cities"][city_name]["owner"] = member.display_name

    if city_name not in p["cities"]:
        p["cities"].append(city_name)

    save_data(data)
    await send_embed(ctx, "👑 Хот Эзэн Тохирууллаа", f"**{city_name}** → **{member.display_name}**", "admin", player=admin_p)


@bot.command(name="reloadgame")
@is_admin()
async def reloadgame(ctx):
    global data
    admin_p = get_player(ctx.author)
    data = load_data()
    ensure_city_state()
    try:
        for uid_key, player in data.get("players", {}).items():
            if isinstance(player, dict):
                player.pop("energy", None)
                ensure_player_upgrades(player)
        save_data(data)
    except Exception:
        pass
    await send_embed(ctx, "🔄 Өгөгдөл Дахин Ачааллаа", "Файл дахь мэдээлэл дахин уншигдлаа.", "admin", player=admin_p)

# ============================================================
# EXTRA COMMAND PACK
# ============================================================
EXTRA_COMMANDS = {
    "beg": ("economy", "🙏 Өршөөл", "Та замаар өнгөрөгчдөөс багахан хандив авлаа."),
    "gift": ("economy", "🎁 Бэлэг", "Ордноос танд өчүүхэн бэлэг ирэв."),
    "bonus": ("economy", "💎 Урамшуулал", "Таны хүчинд урамшуулал олгов."),
    "salary": ("economy", "📜 Цалин", "Албаны цалингаа авлаа."),
    "warehouse": ("shop", "📦 Агуулах", "Бараа, нөөцийн төв агуулахын тойм."),
    "smelt": ("craft", "🔥 Хайлуулах", "Төмөр хайлуулах ажлыг эхлүүлэв."),
    "forge": ("craft", "⚒ Дархан", "Дархны газар зэвсэг цутгаж байна."),
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
    "ping": ("default", "🏓 Ping", "Ботын хариу хэвийн байна."),
    "about": ("default", "📖 Тухай", "Chingis Empire RPG бол Монгол эзэнт гүрний сэдэвт стратеги бот юм."),
    "version": ("default", "🧩 Version", "Starter mega build v1."),
    "server": ("default", "🏰 Сервер", "Энэ сервер дээр эзэнт гүрний дайн өрнөж байна."),
    "rules": ("default", "📘 Дүрэм", "Серверийн дүрэм, шударга тоглоомыг мөрд."),
    "faq": ("default", "❓ FAQ", "Хамгийн түгээмэл асуултын хариултууд энд байна."),
    "news": ("default", "📰 Мэдээ", "Өнөөдрийн эзэнт гүрний мэдээ ирлээ."),
    "event": ("default", "🎉 Event", "Түр хугацааны арга хэмжээ идэвхжиж болно."),
    "season": ("default", "🍂 Улирал", "Тал нутгийн улирал дайнд нөлөөлнө."),
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
        await send_embed(ctx, title, text + tail, category, player=p)

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
