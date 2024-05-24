import os
import glob
import nextcord
from nextcord.ext import commands
from rasa.core.agent import Agent
import asyncio


# Function to find the latest Rasa model
def find_model():
    path = os.path.join('models', f'*.tar.gz')
    models = glob.glob(path)
    return models[0]

# Créer une instance de l'agent Rasa
agent = Agent.load(find_model())

# Configure the Discord bot
intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event to indicate the bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} is ready to be used!")


# Handle messages and send them to Rasa
@bot.event
async def on_message(message):
    print(message)
    print(message.content)

    # Ignore messages from the bot itself to prevent infinite loops
    if message.author == bot.user or message.channel.type != nextcord.ChannelType.text or message.channel.name != "channel-test":
        return

    # Check if message.content is not empty
    if not message.content.strip():
        return

    # Get the response from the Rasa model
    responses = await agent.handle_text(message.content)

    # Print the response for debugging
    print(f"User message: {message.content}")
    print(f"Rasa response: {responses}")

    # Send the response back to the Discord channel
    if responses and len(responses) > 0:
        for response in responses:
            await message.channel.send(response.get("text", "No response text found"))

    # Ensure other commands are processed
    await bot.process_commands(message)


# Lancer le bot
bot.run("MTI0MzYzMjAxODM4Mjc4NjU3MA.Getn8_.s7_z0vTxObqTO9h1WDxlSudpnUnaulFtr-Ne5A")