import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("MTM2MTg1NzY2NjIwNDQzNDU3Mw.GclKbv.AQ9dfEFiSG5t9q3TlM-Bw54yVpbsrDcem1OmsE")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required to read message content

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    if "optix is bad" in content or "robotics is bad" in content:
        await message.add_reaction("👍")
    elif "optix" in content or "robotics" in content:
        await message.add_reaction("👎")

bot.run(TOKEN)
