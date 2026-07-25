import discord
from discord.ext import commands
import aiohttp
import os

TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("OPENROUTER_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

SYSTEM_PROMPT = """
Tu es AQR Bot.
Tu es une IA française, sympathique, intelligente et utile.
Tu réponds uniquement dans le salon nommé 🤖・ia.
Tu réponds naturellement comme ChatGPT.
"""

conversation = {}

@bot.event
async def on_ready():
    print(f"{bot.user} est connecté !")

async def ask_ai(user_id, message):

    history = conversation.get(user_id, [])

    history.append({
        "role":"user",
        "content":message
    })

    messages = [
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        }
    ] + history

    async with aiohttp.ClientSession() as session:

        async with session.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers={
                "Authorization":f"Bearer {API_KEY}",
                "Content-Type":"application/json"
            },

            json={

                "model":"mistralai/mistral-7b-instruct:free",

                "messages":messages

            }

        ) as resp:

            data = await resp.json()

    answer = data["choices"][0]["message"]["content"]

    history.append({
        "role":"assistant",
        "content":answer
    })

    conversation[user_id] = history[-10:]

    return answer

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.name != "🤖・ia":
        return

    async with message.channel.typing():

        answer = await ask_ai(
            str(message.author.id),
            message.content
        )

        if len(answer) > 1900:
            answer = answer[:1900]

        await message.reply(answer)

bot.run(TOKEN)
