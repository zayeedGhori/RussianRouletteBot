import os
import discord
from dotenv import load_dotenv

# imports items from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Gives permission to look at member names
intents = discord.Intents.default()
intents.members = True

# Creates bot
bot = discord.Client(intents=intents)

# Initializes keyword that the bot will respond to
keyword = '!roulette'

# Checks if the GUILD in .env is listed is in the guilds of the bot and if it has connected to discord
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            print(f'Found {guild.name} guild!')
            break

    print(
        f'{bot.user} has connected to Discord!\n'
    )

# Runs when a message is sent, prints 'hello [member names]'
@bot.event
async def on_message(message):
    message_breakdown = message.content.strip().lower().split()
    main, extra = message_breakdown[0], message_breakdown[1:len(message_breakdown)]
    # prints message if keyword is in the start of message
    if main == keyword:
        extra = (" / ").join(extra)
        members = (', ').join([member.name for member in bot.guilds[0].members])
        await message.channel.send("Hello! You have activated the Russian Roulette Bot. You have added the following sub-commands: [{}]. Current members are: '{}'".format(extra, members))
    

# runs the bot
bot.run(TOKEN)