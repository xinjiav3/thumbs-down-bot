import discord

intents = discord.Intents.default()
intents.messages = True  # Enables message-related events
intents.message_content = True  # Required to read message content

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore messages from bots

    # Check for keywords in the message content
    if "optix" in message.content.lower() or "robotics" in message.content.lower():
        try:
            # React with thumbs down emoji
            await message.add_reaction("👎")
        except discord.HTTPException as e:
            print(f"Failed to react: {e}")

# Replace with your bot token
bot.run("YMTM2MTg1NzY2NjIwNDQzNDU3Mw.GT1837.O8W8W2-AI0208aV5AGeqXvOfirShYBPY5XqC0E")
