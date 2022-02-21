import time
import os

from discord import Intents
from discord.ext import commands
from discord import ApplicationContext
from dotenv import load_dotenv

start = time.perf_counter()

bot = commands.Bot(command_prefix=".", Intents=Intents.all())

guilds=[809410416685219853, 803981117069852672]

load_dotenv()

@bot.command()
async def load(ctx: ApplicationContext, extension):
    if ctx.author.id == 330707764911276035:
        bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx: ApplicationContext, extension):
    if ctx.author.id == 330707764911276035:
        bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv('token'))
