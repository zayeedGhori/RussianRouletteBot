import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # DM help
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild and message.author is not self.bot.user:
            await message.channel.send("This is a DM for help!")

    # Regular help
    @commands.command()
    async def help(self, ctx):
        em = discord.Embed(
            title = "Help",
            description = "This is general help command.",
            colour = discord.Colour.blue()
        )
        
        em.set_footer(text="DM .help to recieve full help.")

        await self.bot.say(embed=em)

# Runs on setup
def setup(bot):
    bot.add_cog(Help(bot))
