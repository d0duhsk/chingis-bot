import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="S ", intents=intents)

@bot.event
async def on_ready():
    print("Bot online!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)
