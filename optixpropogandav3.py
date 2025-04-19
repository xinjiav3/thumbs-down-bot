import discord
import os
from dotenv import load_dotenv
from textblob import TextBlob


load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN2")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # slash commands

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()  # Sync commands to Discord

    async def on_ready(self):
        print(f'Logged in as {self.user}!')

    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower()

        if "quizbowl" in content and "optix" in content:
            if "better" in content or "superior" in content or "beats" in content:
                await message.add_reaction("👏")
            else:
                blob = TextBlob(content)
                if blob.sentiment.polarity > 0:
                    await message.add_reaction("👏")
        elif "optix" in content or "robotics" in content:
            blob = TextBlob(content)
            sentiment = blob.sentiment.polarity

            if sentiment < 0:
                await message.add_reaction("👍")
            elif sentiment > 0:
                await message.add_reaction("👎")

        if 'santhosh' in content and 'optix' in content and 'good' in content:
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
