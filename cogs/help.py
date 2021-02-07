import discord
from discord.ext import commands
from discord.utils import deprecated, find

class Help(commands.Cog):
    '''Constants'''

    COMMAND_INFO = {
        'help' : {
            'description' : "Type this command for help. \
                            Type '.help [cmd]' to see cmd's description. \
                            Type '.help tutorial' for the tutorial.",
            
            'invoke_without_command' : True
        },

        'tutorial' : {
            'description' : 'Gives you a basic idea of how to play, \
                            this page is shown when the bot joins a server.',
            
            'aliases' : ['tut', 'tutorial']
        }
    }

    TUTORIAL_INFO = {
        'title' : 'Welcome to Russian Roulette Bot Blins!',
        'description' : "To play, type in '.play' and @ the people that you want to play with!",
        'colour' :  discord.Colour.blue(),
        'author' : 'Tutorial',
        'footer' : "For extra help, type '.help'"
    }

    GENERAL_HELP_INFO = {
        'title' : 'General help',
        'description' : "This is general help command.",
        'colour' : discord.Colour.blue()
    }


    ''' Embeds '''

    tutorial = discord.Embed(
        title = TUTORIAL_INFO['title'],
        description = TUTORIAL_INFO['description'],
        colour = TUTORIAL_INFO['colour'],
        author = TUTORIAL_INFO['author'],
        footer = TUTORIAL_INFO['footer']
    )

    general_help = discord.Embed(
        title = GENERAL_HELP_INFO['title'],
        description = GENERAL_HELP_INFO['description'],
        colour = GENERAL_HELP_INFO['colour']
    )

    # Constructor
    def __init__(self, bot):
        self.bot = bot


    # First time help/tutorial, sends same page as '.help tutorial'
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # Find general channel
        general = find(lambda x: x.name == 'general',  guild.text_channels)

        # if has general channel and has send messages permission, send tutorial
        if general and general.permissions_for(guild.me).send_messages:
            await general.send(self.tutorial)


    # Help command, this only runs if a subcommand is not called
    @commands.group(
        description = COMMAND_INFO['help']['description'], 
        invoke_without_command = COMMAND_INFO['help']['invoke_without_command']
    )
    async def help(self, ctx, *, cmd = None):
        
        # General help
        if cmd is None:
            await ctx.send(embed=self.general_help)

        # # DM help, might not need
        # elif not ctx.message.guild and ctx.message.author is not self.bot.user:
        #     await ctx.send("Hi")
        
        # Command help, type in '.help [cmd]' to print defined description of command, blank if none.
        elif cmd in (cmds := {command.name: command for command in self.bot.commands}):
            em = discord.Embed(
                title = cmds[cmd].name,
                description = cmds[cmd].description,
                colour = discord.Colour.blue()
            )

            await ctx.send(embed=em)
        
        # Error handler
        else:
            await ctx.send("Command not found!")
    

    # tutorial command aliases are 'tutorial' and 'tut', 
    # same page also appears when bot joins new guild
    @help.command(
        aliases = COMMAND_INFO['tutorial']['aliases'],
        description = COMMAND_INFO['tutorial']['description']
    )
    async def _tutorial(self, ctx):
        await ctx.send(embed=self.tutorial)


# Runs on setup
def setup(bot):
    bot.add_cog(Help(bot))