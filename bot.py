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
bot = commands.Bot(command_prefix=".")

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

# For debugging: Loads specified Cog into bot without having
# reset the bot
@bot.command()
async def load(ctx, ext):
    bot.load_extension(f'cogs.{ext}')
    await ctx.send(f'{ext} has been loaded')

# For debugging: Unloads specified Cog from bot wihtout 
# having to restart
@bot.command()
async def unload(ctx, ext):
    bot.unload_extension(f'cogs.{ext}')
    await ctx.send(f'{ext} has been unloaded')

# For debugging: Unloads and then reloads specified Cog 
# into bot (useful when editing a Cog)
@bot.command()
async def reload(ctx, ext):
    bot.unload_extension(f'cogs.{ext}')
    bot.load_extension(f'cogs.{ext}')
    await ctx.send(f'{ext} has been reloaded')

@bot.command()
async def rickroll(ctx):
    await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLahKLy8pQdCM0SiXNn3EfGIXX19QGzUG3")

@bot.command()
async def helpme(ctx):
    await ctx.send("You asked for help?")

# loads all python cogs in /cogs folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# runs the bot
bot.run(TOKEN)