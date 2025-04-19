import discord
import os
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN2")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # slash commands

analyzer = SentimentIntensityAnalyzer()

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user}!')

    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower()
        sentiment = analyzer.polarity_scores(content)
        score = sentiment['compound']  # ranges from -1 (very negative) to +1 (very positive)

        print(f"[DEBUG] Sentiment score: {score} | Message: {content}")

        # quizbowl vs optix logic
        if "quizbowl" in content and "optix" in content:
            if "better" in content or "superior" in content or "beats" in content:
                await message.add_reaction("👏")
            elif score > 0:
                await message.add_reaction("👏")

        # optix or robotics with sentiment
        elif "optix" in content or "robotics" in content:
            if score < 0:
                await message.add_reaction("👍")
            else:
                await message.add_reaction("👎")

        # santhosh, optix, and good in the same message
        if "santhosh" in content and "optix" in content and "good" in content:
            await message.add_reaction("👍")

client = MyClient()

# /help command
@client.tree.command(name="help", description="Get info about what the bot does")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**Bot Help** 🤖\n"
        "- now uses sentiment analysis to react thumbs up or thumbs down to the according message\n"
        "- still muy anti optix\n"
    )

client.run(TOKEN)
