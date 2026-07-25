import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} est connecté !")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.name == "🤖・ia":
        await message.reply(
            "Salut ! 👋 Je suis ton IA. Pour l'instant je suis en cours de création, mais bientôt je pourrai répondre comme ChatGPT !"
        )

    await bot.process_commands(message)

bot.run(TOKEN)
