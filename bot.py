import os
import discord
from discord.ext import commands
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
bot = commands.Bot("!")

# url = "https://discord.com/api/v8/applications/787821652364361748/commands"

# json = {
#     "name": "blep",
#     "description": "Send a random adorable animal photo",
#     "options": [
#         {
#             "name": "animal",
#             "description": "The type of animal",
#             "type": 3,
#             "required": True,
#             "choices": [
#                 {
#                     "name": "Dog",
#                     "value": "animal_dog"
#                 },
#                 {
#                     "name": "Cat",
#                     "value": "animal_cat"
#                 },
#                 {
#                     "name": "Penguin",
#                     "value": "animal_penguin"
#                 }
#             ]
#         },
#         {
#             "name": "only_smol",
#             "description": "Whether to show only baby animals",
#             "type": 5,
#             "required": False
#         }
#     ]
# }

# # For authorization, you can use either your bot token 
# headers = {
#     "Authorization": TOKEN
# }

# r = requests.post(url, headers=headers, json=json)

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

@bot.command()
async def play(ctx):
    await ctx.send("You are playing!")

@bot.command()
async def rickroll(ctx):
    await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLahKLy8pQdCM0SiXNn3EfGIXX19QGzUG3")

@bot.command()
async def helpme(ctx):
    await ctx.send("You asked for help?")

# runs the bot
bot.run(TOKEN)