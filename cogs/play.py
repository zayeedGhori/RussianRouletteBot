import discord, random, asyncio
from discord.ext import commands

# Constants, can be modified if needed
FILLER = "[FILLER]"
NUMBER_OF_ROUNDS = 6
REQUIRED_NUM_PLAYERS = 2
CONGRATS_MESSAGE = "Congratulations! You earned {} coins! 💰"
NEXT_PLAYER_MESSAGES = {
    "You're up",
    "Next up",
    "You got this",
    "Don't blow it",
    "Let's go",
    "Come on",
    "Take a chance"
}
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

def createEmbed(title="", desc="test", fields=[], colour=discord.Color.dark_blue()):
    title, desc = str(title), str(desc)
    embed = discord.Embed(title = title, description = desc, colour = colour)

    for field in fields:
        embed.add_field(name = ("name" in field.keys()) and field["name"] or "", value = field["value"], inline = field["inline"])

    return embed

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
                await ctx.send(embed=createEmbed(title = "Can't join!", desc="User {} is currently in a game! They have been omitted.".format(member.display_name), colour = discord.Color.dark_gray()))

        # Create revolver with bullet (the location being the index of the True value)
        if len(members) < REQUIRED_NUM_PLAYERS:
            await ctx.send(embed=createEmbed(title = "Not enough players!", desc="You do not have enough players! {} more players needed.".format(REQUIRED_NUM_PLAYERS-len(members)), colour = discord.Color.red())) 
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
        await ctx.send(embed=createEmbed(desc="{} are playing regular mode!".format(", ".join(member.display_name for member in members))))

        ### Short game of automated imperfect russian roulette ###
        Round = 0
        while len(members) > 1:
            # Increment and display round
            Round += 1 
            roundEmbed = createEmbed(title="Round {}:".format(Round), desc="")

            isFirst = True
            # for every member playing, make them shoot
            for member in members:
                if isFirst:
                    isFirst = False
                    roundEmbed.add_field(name = "{}...".format(NEXT_PLAYER_MESSAGES[random.randint(1, len(NEXT_PLAYER_MESSAGES))-1]), value="Your turn {}!".format(member.display_name), inline=False)
                    await ctx.send(embed=roundEmbed)
                else:
                    await ctx.send(embed=createEmbed(desc="Your turn {}!".format(member.display_name)))
                print(self.Games[game_id]["CurrentPlayer"])
                self.Games[game_id]["CurrentPlayer"] = member

                """
                While loop implementation - not in use.
                @commands.group(invoke_without_command=True, aliases=["shoot", "fire"])
                async def hit(self, ctx):
                    self.Games[game_id]["CurrentPlayer"] = 0
                    self.bot.remove_command("hit")

                while True:
                    if time.time()-benchmark > TIME_TO_RESPOND:
                        await ctx.send(f'{member.display_name} failed to respond in time!')
                        break
                    elif not self.Games[game_id]["CurrentPlayer"]:
                        break
                """

                hit_commands = [
                    "hit",
                    "shoot",
                    "fire",
                    "hit me"
                ]

                def verify(message):
                    return message.content.lower().strip() in hit_commands and message.author == member

                shotEmbed = discord.Embed
                try:
                    await self.bot.wait_for("message", check=verify, timeout=60.0)
                except asyncio.TimeoutError:
                    await ctx.send(embed=createEmbed(desc="{} failed to respond in time!".format(member.display_name)))
                    members.remove(member) 
                else:
                    shotEmbed = createEmbed(desc="{} shot, and ...".format(member.display_name))
                    
                    # If safe, then no bullet+
                    safe = cylinder.pop(random.randint(0, len(cylinder)-1))
                    if safe:                           
                        safe_message = FUNNY_MESSAGES["Survived"][random.randint(0, len(FUNNY_MESSAGES["Survived"])-1)]

                        shotEmbed.colour = discord.Colour.green()
                        shotEmbed.add_field(name = "is safe!", value=safe_message, inline=False)
                    
                    # if not safe, member is dead
                    else:
                        died_message = FUNNY_MESSAGES["Died"][random.randint(0, len(FUNNY_MESSAGES["Died"])-1)]

                        shotEmbed.colour = discord.Colour.red()
                        shotEmbed.add_field(name = "is dead!", value=died_message, inline=False)
                        members.remove(member) # remove member from members list

                    await ctx.send(embed = shotEmbed)

        # Win message
        await ctx.send(embed=createEmbed(title="{} wins!".format(members[0].display_name), desc = CONGRATS_MESSAGE, colour=discord.Color.gold()))
        
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