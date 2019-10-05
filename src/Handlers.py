import discord

def set_handlers(client):
	@client.event
	async def on_message(message):
		print("test")