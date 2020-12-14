import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = discord.Client()

keyword = '!roulette'

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} has connected to Discord!\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_message(message):
    message_text = message.content.strip().lower()

    if keyword in message_text:
        await message.channel.send('hi')

bot.run(TOKEN)