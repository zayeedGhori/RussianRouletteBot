import discord
from discord import user
from discord.ext import commands
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from player import Player

class Shop(commands.Cog):
    def __init__(self, bot : discord.Client):
        self.bot = bot
        self.players_in_shop = {} # Dictionary of players that activates shop_env in a channel

        # List of items and info
        self.items = {
            'life' : {
                'image' : '❤',
                'name' : 'Life',
                'description' : 'A very useful life! Use this in your game to escape death.',
                'price' : 1000
            },

            'shield' : {
                'image' : '🛡',
                'name' : 'Shield',
                'description' : 'A shield has a 1/100 chance for blocking your opponent\'s bullet. Good luck blyat.',
                'price' : 100
            }
        }

        # embed with shop formatting
        self.shop_page = discord.Embed(
            title = "__**Welcome to the shop!**__", # __ = underline, ** = bold
            description =
                '**Items:**\n\n' +

                # Creates a string with all the items seperated by two '\n's
                '\n\n'.join(
                        # Creates list of each item line
                        [
                            # Formats each item line, ** for bold words
                            # formatted like: 'image' 'name' - $'price'\n'description'
                            f"**{info['image']}** **{info['name']}** - **${info['price']}**\n{info['description']}"
                            
                            # For each element in dictionary of info for every item
                            for info in [
                                pair[1] for pair in self.items.items()
                            ]
                        ]
                )
        ).set_footer(
            text = 'Type `buy *item*` or `buy *item* *quantity*`to buy somthing or `exit` to exit the shop.'
        )
        
    # shop command enters user into the shop by setting the channel to True in players_in_shop
    @commands.command(description='This is the shop!')
    async def shop(self, ctx):
        self.players_in_shop[ctx.channel] = True
        
        await ctx.channel.send(embed=self.shop_page)

    # shop environment, called whenever a message is sent
    @commands.Cog.listener('on_message')
    async def shop_env(self, message : discord.Message):
        # if the channel does not exist in the dictionary, stop the function
        try:
            self.players_in_shop[message.channel]
        except:
            return

        # if the channel is in the shop and the author is not the bot
        if self.players_in_shop[message.channel] and message.author != self.bot.user:

            # if the message says exit, exit the shop and set channel to False in players_in_shop
            if (message.content == 'exit'):
                await message.channel.send("Thank you for visiting the shop!") 
                self.players_in_shop[message.channel] = False
            
            #####INCOMPLETE#####
            # If 'buy' is in the message, let the user know
            elif ('buy' in message.content):
                parts = message.content.split()
                player = Player.get_player(message.author)

                if (len(parts) < 2 or len(parts) > 3):
                    await message.channel.send("Invalid item selected.")
                
                elif (len(parts) < 3):
                    item = parts[1]

                    await self.buy(player, item)

                    await message.channel.send(f'Thank you for buying {item}\nYou have ${player.wallet} remaining.')
                
                else:
                    item = parts[1]

                    await self.buy(message.author, item)

                    await message.channel.send(f'Thank you for buying {item}\nYou have ${player.wallet} remaining.')

                
    #####INCOMPLETE#####
    # unfinished buy function
    async def buy(self, player : Player, item, numItems = 1):
        player.wallet -= self.items[item]['price']

        if (self.item[item]['name'] == 'Life'):
            player.lives += numItems



# Runs on setup
def setup(bot):
    bot.add_cog(Shop(bot))