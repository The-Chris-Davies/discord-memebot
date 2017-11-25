import sys
import random
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands

def get_settings(fn = 'settings.txt'):
	f=open(fn)
	data = {}
	for ln in f:
		if ln[0] == '#': continue
		sln = ln.split('=', 1)
		if sln[0] == 'token':
			data['token'] = sln[1].strip()
		if sln[0] == 'prefix':
			data['prefix'] = sln[1].strip()
	return data

if(len(sys.argv)>1):
	bot_data = get_settings(sys.argv[1])
else:
	bot_data = get_settings()

client = Bot(description="Make memes make sense \n Chris for president 2020", command_prefix=bot_data['prefix'], pm_help = True)

@client.event
async def on_ready():
	print(
	"""logged in as {}\nservers:\n\t{}\nusers:\n\t{}\nDiscord version: {}
	""".format( client.user.name, 
			"\n\t".join(map(lambda x:x.name, client.servers)), 
			"\n\t".join(set(map(lambda x:x.name,client.get_all_members()))), 
			discord.__version__, ))

@client.event
async def on_message(message):
	print('message from {} in channel {}, {}:\n\t{}'.format(message.author.name, message.channel.name, message.server.name, message.content))
	if message.author != client.user:
		
		#say command
		if message.content.split()[0].lower() == 'say':
			await client.send_message(message.channel, message.content[3:])
			await client.delete_message(message)
		
		#die command
		elif message.content.lower() == 'die':
			await client.send_message(message.channel, random.choice((":point_right::sunglasses::point_right: zoop", ":joy::gun:")))
			await client.logout()
		
		#test command
		elif message.content.lower() == 'test':
				await client.send_message(message.channel, "I'm alive?")
				await asyncio.sleep(1)
				await client.send_message(message.channel, "I'm ALIVE?!")
				await asyncio.sleep(2)
				await client.send_message(message.channel, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHH")

client.run(bot_data['token'])
