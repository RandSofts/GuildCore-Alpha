import attributes
import nextcord
import os
from nextcord.ext import commands


intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix="gc!", intents=intents)

print(attributes.LOGOASCII)

for files in os.listdir("./cogs/botCore"):
    if files.endswith(".py"):
        print(f"Loaded {files[:-3]}")
        bot.load_extension(f"cogs.botCore.{files[:-3]}")
print("Loaded [BOT CORE]")

for files in os.listdir("./cogs/botBasics"):
    if files.endswith(".py"):
        print(f"Loaded {files[:-3]}")
        bot.load_extension(f"cogs.botBasics.{files[:-3]}")
print("Loaded [BOT BASICS]")

for files in os.listdir("./cogs/botRoblox"):
    if files.endswith(".py"):
        print(f"Loaded {files[:-3]}")
        bot.load_extension(f"cogs.botRoblox.{files[:-3]}")
print("Loaded [BOT ROBLOX]")

for files in os.listdir("./cogs/botStaff"):
    if files.endswith(".py"):
        print(f"Loaded {files[:-3]}")
        bot.load_extension(f"cogs.botStaff.{files[:-3]}")
print("Loaded [BOT STAFF]")

for files in os.listdir("./cogs/botMod"):
    if files.endswith(".py"):
        print(f"Loaded {files[:-3]}")
        bot.load_extension(f"cogs.botMod.{files[:-3]}")
print("Loaded [BOT MOD]")

bot.run(attributes.TOKEN)
