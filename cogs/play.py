import discord, random, asyncio, time
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
TIME_TO_RESPOND = 60

class Play(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GAMES_PLAYED = -1
        self.Games = {}


    def user_is_in_game(self, user):
        for game in self.Games:
            if user in game:
                return True
        
        return False

    # The group of russian roulette commands, default is played when there are no subcommands 
    @commands.group(invoke_without_command=True, aliases=["roulette"])
    async def play(self, ctx):
        ''' Default Command '''
        members = []
        # makes list for every member in the message that invoked this command
        for member in ctx.message.mentions:
            if not self.user_is_in_game(member):
                members.append(member)
            else:
                await ctx.send(f'User {member.display_name} is currently in a game! They have been omitted.')

        # Create revolver with bullet (the location being the index of the True value)
        if len(members) < REQUIRED_NUM_PLAYERS:
            await ctx.send(f'You do not have enough players! {REQUIRED_NUM_PLAYERS-len(members)} more players needed.') 
            return

        self.GAMES_PLAYED += 1

        game_id = self.GAMES_PLAYED

        self.Games[game_id] = {
            "Players" : members,
            "CurrentPlayer" : 0,
        }

        cylinder = [True for _ in range(NUMBER_OF_ROUNDS)]
        cylinder[random.randint(0, NUMBER_OF_ROUNDS-1)] = False
        # Let members know what mode they are using
        await ctx.send(f'{" ".join(member.mention for member in members)} are playing regular mode!')

        ### Short game of automated imperfect russian roulette ###
        Round = 0
        while len(members) > 1:
            # Increment and display round
            Round += 1 
            await ctx.send(f'Round {Round}:')

            # for every member playing, make them shoot
            for member in members:

                await ctx.send(f'Your turn {member.display_name}!')
                print(self.Games[game_id]["CurrentPlayer"])
                self.Games[game_id]["CurrentPlayer"] = member

                @commands.group(invoke_without_command=True, aliases=["shoot", "fire"])
                async def hit(self, ctx):
                    self.Games[game_id]["CurrentPlayer"] = 0
                    self.bot.remove_command("hit")


                benchmark = time.time()

                while True:
                    if time.time()-benchmark > TIME_TO_RESPOND:
                        await ctx.send(f'{member.display_name} failed to respond in time!')
                        break
                    elif not self.Games[game_id]["CurrentPlayer"]:
                        break


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
        
        self.Games.pop(game_id, None)
        # award points here
        
        

    
    # Sudden death mode subcommand, alias is 'sd'
    @play.command(aliases=['sd'])
    async def sudden_death(self, ctx, *members : discord.Member):
        await ctx.send(f"{' '.join(member.mention for member in members)} are playing sudden death!")

    
# Runs on setup
def setup(bot):
    bot.self_bot = False
    bot.add_cog(Play(bot))