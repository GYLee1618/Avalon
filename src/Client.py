import discord
import argparse

from Avalon import AvalonGame
from Handlers import set_handlers

class Client:
	"""Class encapsulating helper functions and data for the discord bot"""

	def __init__(self, client, token):
		""" Default Constructor 
		
		Args:
			client (discord.client): discord.client object to handle Discord API accesses
			token (str): Token that will allow this code to access the Discord API
		"""
		self._token = token
		self._client = client
		self._players = list()

	def start_game(self):
		""" Creates a new game with players in self._players"""
		self._game = AvalonGame(self._players, "../Config/game.config.json")

	def run(self):
		""" Runs bot """
		self.client.run(self.token)

	def add_player(self, player):
		"""Appends player to end of self._players list if they are not already on it
		
		Args:
			player (str): player to add
		"""
		if (player not in self._players):
			self._players.append(player)

	def remove_player(self, player):
		"""Attempts to remove player from self._players

		Args:
			player (str): player to remove
		"""
		try:
			self._players.remove(player)
		except ValueError:
			pass

	@property
	def game(self):
		""":obj:`AvalonGame`: game logic handler object"""
		return self._game

	@property
	def players(self):
		""":obj:`list` of :obj:`str`: list of players currently ready to play game"""
		return self._players
	

	@property
	def client(self):
		""""obj:`discord.client`: discord client"""
		return self._client
	
	@property
	def token(self):
		"""str: token for access to Discord API"""
		return self._token
	

parser = argparse.ArgumentParser(description="Avalon Bot Command Line")
parser.add_argument("token", action="store", help="Discord bot token string", type=str)

args = parser.parse_args()

discord_client = discord.Client()

set_handlers(discord_client)

client = Client(discord_client, args.token)

client.run()