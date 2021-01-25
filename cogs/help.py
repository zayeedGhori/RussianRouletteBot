import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # DM help
    @commands.Cog.listener()
    async def on_message(self, ctx, message):
        if not message.guild:
            await ctx.send("This is a DM for help!")

    # Regular help
    @commands.command()
    async def help(self, ctx):
        await ctx.send("This is the help command!")

# Runs on setup
def setup(bot):
    bot.add_cog(Help(bot))