"""
Used to store and access attributes of players such as wallet, level, and lives.
"""

import discord
from discord.ext import commands

players = {}

class Player:

    def __init__(self, user : discord.User):
        self.user = user
        self.wallet = 0
        self.level = 0
        self.lives = 0
        self.name = user.name
        players[user] = self
    
    def get_players():
        return players
    
    def get_player(user):
        return players[user]