import discord, random
from discord.ext import commands

class Play(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # The group of russian roulette commands, default is played when there are no subcommands 
    @commands.group(invoke_without_command=True)
    async def play(self, ctx):

        ''' Default Command '''

        # makes list for every member in the message that invoked this command
        members = [member for member in ctx.message.mentions]

        # Create revolver with bullet (the location being the index of the True value)
        cylinder = [False for i in range(6)]
        cylinder[random.randint(0, 5)] = True

        # Let members know what mode they are using
        await ctx.send(f'{" ".join(member.mention for member in members)} are playing regular mode!')



        ### Short game of automated imperfect russian roulette ###
        round = 0

        # while more than one member is standing, play the game
        while (len(members) > 1):
            # Increment and display round
            round += 1 
            await ctx.send(f'Round {round}:')

            # for every member playing, make them shoot
            for member in members:
                await ctx.send(f'{member.mention} shot.')
                
                # If False, then no bullet, so member is safe
                if (not cylinder[random.randint(0, 5)]):
                    await ctx.send(f'{member.mention} is safe.')
                
                # if True, member is dead
                else:
                    await ctx.send(f'{member.mention} is dead.')
                    members.remove(member) # remove member from members list
        
        # Win message
        await ctx.send(f'{members[0].mention} wins!')
        

    
    # Sudden death mode subcommand, alias is 'sd'
    @play.command(aliases=['sd'])
    async def sudden_death(self, ctx, *members : discord.Member):
        await ctx.send(f"{' '.join(member.mention for member in members)} are playing sudden death!")

    
# Runs on setup
def setup(bot):
    bot.add_cog(Play(bot))