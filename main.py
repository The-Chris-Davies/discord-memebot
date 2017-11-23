import sys
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands

class KillMeError(Exception):
	pass

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


@client.command()
async def test(*args):
	await client.say("I'm alive?")
	await asyncio.sleep(1)
	await client.say("I'm ALIVE?!")
	await asyncio.sleep(2)
	await client.say("AAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHH")

@client.command()
async def say(*args):
	if(len(args)):
		await client.say(' '.join(args))
	else:
		await client.say('no')

@client.command()
async def die(*args):
	global client
	await client.say(":joy::gun:")
	await client.logout()

client.run(bot_data['token'])
