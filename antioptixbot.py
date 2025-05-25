import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ANTIOPTIXBOTTOKEN")

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

        if "optix is bad" in content or "robotics is bad" in content:
            await message.add_reaction("👍")
        elif "santhosh" in content and "optix" in content and "good" in content:
            await message.add_reaction("👍")
        elif "optix" in content or "robotics" in content:
            await message.add_reaction("👎")


client = MyClient()

# /help command
@client.tree.command(name="help", description="Get info about what the bot does")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**Bot Help** 🤖\n"
        "- 👎 Reacts to messages mentioning 'optix' or 'robotics'\n"
        "- 👍 Reacts if someone says 'santhosh', 'optix', and 'good' in the same message\n"
        "- 👍 Reacts if message includes 'optix is bad' or 'robotics is bad'\n"
        "\nTry it out by saying something like 'optix is bad' or 'santhosh is good at optix!'"
    )

client.run(TOKEN)
