import discord
from discord.ext import commands

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channels_in_shop = {} # Dictionary of channels that activates shop_env

        # List of items and info
        self.items = {
            'life' : {
                'image' : '❤',
                'name' : 'Life',
                'description' : 'A very useful life! Use this in your game to escape death.',
                'price' : 1000
            },

            'sheild' : {
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
        
    # shop command enters user into the shop by setting the channel to True in channels_in_shop
    @commands.command(description='This is the shop!')
    async def shop(self, ctx):
        self.channels_in_shop[ctx.channel] = True
        await ctx.channel.send(embed=self.shop_page)

    # shop environment, called whenever a message is sent
    @commands.Cog.listener('on_message')
    async def shop_env(self, message):
        # if the channel does not exist in the dictionary, stop the function
        try:
            self.channels_in_shop[message.channel]
        except:
            return

        # if the channel is in the shop and the author is not the bot
        if self.channels_in_shop[message.channel] and message.author is not self.bot:

            # if the message says exit, exit the shop and set channel to False in channels_in_shop
            if (message.content == 'exit'):
                await message.channel.send("Thank you for visiting the shop!") 
                self.channels_in_shop[message.channel] = False
            
            #####INCOMPLETE#####
            # If 'buy' is in the message, let the user know
            elif ('buy' in message.content):
                parts = message.content.split()

                if (len(parts) < 2):
                    await message.channel.send("Invalid item selected.")
                
                else:
                    await message.channel.send(f'Thank you for buying {parts[1]}')
    
    #####INCOMPLETE#####
    # unfinished buy function
    async def buy(self, item, wallet, quantity=1):
        return wallet - item['price']*quantity
        


# Runs on setup
def setup(bot):
    bot.add_cog(Shop(bot))