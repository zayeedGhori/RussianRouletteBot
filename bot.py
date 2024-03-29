import os, time
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
from player import Player

# imports items from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Gives permission to look at member names
intents = discord.Intents.default()
intents.members = True

# Creates bot
bot = commands.Bot(command_prefix=".", intents=intents)

# Checks if the GUILD in .env is listed is in the guilds of the bot and if it has connected to discord
@bot.event
async def on_ready():
    for guild in bot.guilds:
        for member in guild.members:
            Player(member)
        
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

# Command group setprefix changes the bot's default prefix based on a passed value,
# if the Member invoking the command is a channel admin.
# If a space is desired in the prefix (inluding a space between prefix and command),
# quotations should be used like '.setprefix "[prefix] "'.
# Aliases: 'sp'
@bot.group(
    aliases=['sp'], 
    description='Used to change the bot\'s prefix. \
                If you want a space between the commands and the prefix, \
                use quotations: `"[prefix] "`. Default prefix: `.`, \
                use `.setprefix default` to set to default',
    invoke_without_command=True
)
async def setprefix(ctx, new_prefix):

    # if the user who used the command is an admin in the channel
    if (ctx.author.permissions_in(ctx.channel).administrator):
        bot.command_prefix = new_prefix
        await ctx.send(f'Prefix sucessfully changed to: `{new_prefix}`!')
    
    else:
        await ctx.send(f'You, {ctx.author}, are not an admin!\nPlease contact a channel admin to change the prefix!')

# Subcommand of setprefix, sets the prefix to default: '.'. Aliases: 'd'
@setprefix.command(
    aliases=['d'], 
    description='Set command prefix to default: `.`.'
)
async def default(ctx):
    bot.command_prefix = '.'

    await ctx.send(f'Prefix sucessfully changed to default: `.`!')

# Removes default help command
bot.remove_command('help')

# loads all python cogs in /cogs folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_guild_join(guild : discord.Guild):
    for s in guild.members:
        Player(s)

if __name__ == '__main__':
    # runs the bot
    bot.run(TOKEN)