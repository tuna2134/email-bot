from discord.ext import commands
from json import load

bot = commands.Bot(command_prefix = "e!")
with open("./config.json", "r") as f:
    bot.data = load(f)

@bot.event
async def on_ready():
    print("starting...")
    bot.load_extension("cogs.send")
    bot.load_extension("cogs.getemail")
    print("ready")
    bot.dispatch("full_ready")

bot.run(bot.data["token"])