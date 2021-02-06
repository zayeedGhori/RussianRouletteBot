import discord, random, asyncio
from discord.ext import commands

# Constants, can be modified if needed
NUMBER_OF_ROUNDS = 6
REQUIRED_NUM_PLAYERS = 2
FUNNY_MESSAGES = {
    "Survived": [
        "Lucky you. 🍀",
        "How did you do that, seriously? 🤯",
        "What a legend. ✊",
        "In it to win it I see. 👀"
    ],

    "Died": [
        "That's tough. 😔",
        "RIP.⚰️",
        "Really bro? 😑"
    ]
}

RESPONSE_COMMANDS = [
    ".hit",
    ".shoot",
    ".fire"
]


class Play(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # The group of russian roulette commands, default is played when there are no subcommands 
    @commands.group(invoke_without_command=True, aliases=["roulette"])
    async def play(self, ctx):

        ''' Default Command '''

        # makes list for every member in the message that invoked this command
        members = [member for member in ctx.message.mentions]

        # Create revolver with bullet (the location being the index of the True value)
        if len(members) < REQUIRED_NUM_PLAYERS:
            await ctx.send(f'You do not have enough players! {REQUIRED_NUM_PLAYERS-len(members)} more players needed.') 
            return

        cylinder = [True for _ in range(NUMBER_OF_ROUNDS)]
        cylinder[random.randint(0, NUMBER_OF_ROUNDS-1)] = False
        # Let members know what mode they are using
        await ctx.send(f'{" ".join(member.mention for member in members)} are playing regular mode!')

        ### Short game of automated imperfect russian roulette ###
        Round = 0

        # while more than one member is standing, play the game
        while (len(members) > 1):
            # Increment and display round
            Round += 1 
            await ctx.send(f'Round {Round}:')

            # for every member playing, make them shoot
            for member in members:

                await ctx.send(f'Your turn {member.display_name}!')
                

                def verify(msg):
                    return msg.author.mention == member.mention and msg.channel == ctx.channel and msg.content in RESPONSE_COMMANDS

                try:
                    await self.bot.wait_for("message", timeout=60.0, check=verify)
                except asyncio.TimeoutError:
                    await ctx.send(f'{member.display_name} failed to respond in time!')
                    members.remove(member)
                    continue


                await ctx.send(f'{member.display_name} shot, and ...')
                
                # If safe, then no bullet+
                safe = cylinder.pop(random.randint(0, len(cylinder)-1))
                if safe:   
                    safe_message = FUNNY_MESSAGES["Survived"][random.randint(0, len(FUNNY_MESSAGES["Survived"])-1)]
                    await ctx.send(f'is safe! {safe_message}')
                
                # if not safe, member is dead
                else:
                    died_message = FUNNY_MESSAGES["Died"][random.randint(0, len(FUNNY_MESSAGES["Died"])-1)]
                    await ctx.send(f'is dead! {died_message}')
                    members.remove(member) # remove member from members list
        
        # Win message
        await ctx.send(f'{members[0].mention} wins!')
        

    
    # Sudden death mode subcommand, alias is 'sd'
    @play.command(aliases=['sd'])
    async def sudden_death(self, ctx, *members : discord.Member):
        await ctx.send(f"{' '.join(member.mention for member in members)} are playing sudden death!")

    
# Runs on setup
def setup(bot):
    bot.self_bot = False
    bot.add_cog(Play(bot))