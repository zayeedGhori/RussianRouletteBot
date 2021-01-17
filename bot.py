import os
import discord
from dotenv import load_dotenv
import requests

# imports items from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Gives permission to look at member names
intents = discord.Intents.default()
intents.members = True

# Creates bot
bot = discord.Client(intents=intents)

url = "https://discord.com/api/v8/applications/<my_application_id>/commands"

json = {
    "name": "blep",
    "description": "Send a random adorable animal photo",
    "options": [
        {
            "name": "animal",
            "description": "The type of animal",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "Dog",
                    "value": "animal_dog"
                },
                {
                    "name": "Cat",
                    "value": "animal_cat"
                },
                {
                    "name": "Penguin",
                    "value": "animal_penguin"
                }
            ]
        },
        {
            "name": "only_smol",
            "description": "Whether to show only baby animals",
            "type": 5,
            "required": False
        }
    ]
}

# For authorization, you can use either your bot token 
headers = {
    "Authorization": "Bot 123456"
}

r = requests.post(url, headers=headers, json=json)

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