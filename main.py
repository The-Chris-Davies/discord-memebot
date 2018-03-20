import sys
import random
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands

def get_settings(fn = 'settings.txt'):
	data = {'fn':fn, 'tunnel':{}}
	try:
		f=open(fn)

	except FileNotFoundError as e:
		print("No file by name {} found! Please input info manually:".format(fn))
		data['token'] = raw_input("What is the bot token?\n>|")
		data['prefix'] = raw_input("what is the prefix the bot uses?\n>|")
		return data
		
	for ln in f:
		if ln[0] == '#': continue
		sln = ln.split('=', 1)
		if sln[0] == 'token':
			data['token'] = sln[1].strip()
		if sln[0] == 'prefix':
			data['prefix'] = sln[1].strip()
		'''
		if sln[0] == 'tunnel':
			data['tunnel'][sln[1].split()[0].strip()] = sln[1].split()[1].strip()
			data['tunnel'][sln[1].split()[1].strip()] = sln[1].split()[0].strip()
		'''
	f.close()
	return data

random.seed()
bot_data = get_settings(sys.argv[1] if len(sys.argv)>1 else 'settings.txt')
pendingConnection = ''
client = Bot(description="Who has any idea what they are doing here?", command_prefix=bot_data['prefix'], pm_help = True)

@client.event
async def on_ready():
	print(
	"""logged in as {}\nservers:\n\t{}\nusers:\n\t{}\nDiscord version: {}
	""".format( client.user.name, 
			"\n\t".join(map(lambda x:x.name, client.servers)), 
			"\n\t".join(set(map(lambda x:x.name,client.get_all_members()))), 
			discord.__version__, ))

@client.command()
async def hi(*args):
	'''A test command. Serves no function.'''
	global client
	await client.say("hey there!")

@client.command()
async def test(*args):
	'''A test command. Serves no function.'''
	await client.say("I'm alive?")
	await asyncio.sleep(1)
	await client.say("I'm ALIVE?!")
	await asyncio.sleep(2)
	await client.say("AAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHH")

@client.command(pass_context=True)
async def say(op, *args):
	'''say <message>
	makes the bot say whatever the <message> is. Your comment will be deleted.'''
	if(len(args)):
		await client.say(' '.join(args))
	await client.delete_message(op.message)

@client.command()
async def die(*args):
	'''shuts down the bot.'''
	global client
	await client.say(random.choice((":point_right::sunglasses::point_right: zoop", ":joy::gun:")))
	await client.logout()

@client.command(pass_context = True)
async def openportal(op, *args):
	'''opens a portal in this channel to a random other channel. Can span servers, as long as the bot is in the server.'''
	global bot_data, pendingConnection
	
	if op.message.channel in bot_data['tunnel']:
		await client.say("You fool! A portal is already opened here!")
	elif pendingConnection:
		if pendingConnection == op.message.channel:
			await client.say("You fool! You can't open two ends of a portal in the same place!")
		else:
			bot_data['tunnel'][pendingConnection] = op.message.channel
			bot_data['tunnel'][op.message.channel] = pendingConnection
			pendingConnection = ""
			await client.say("The portal has been opened!")
			await client.send_message(bot_data['tunnel'][op.message.channel], "The portal has been opened!")
			'''
			f = open(bot_data['fn'], 'a')
			f.write("tunnel={} {}".format(op.message.channel, bot_data['tunnel'][op.message.channel]))
			f.close()
			'''
	else:
		pendingConnection = op.message.channel
		await client.say("Portal activated! Waiting for the other end to open...")

@client.command(pass_context = True)
async def closeportal(op, *args):
	'''Closes an already open portal. WIP'''
	if op.message.channel in bot_data['tunnel']:
		endpoint = bot_data['tunnel'][op.message.channel]
		del(bot_data['tunnel'][endpoint])
		del(bot_data['tunnel'][op.message.channel])
		await client.say("The portal is closed!")
		await client.send_message(endpoint, "The portal has been closed at the other end!")
	elif op.message.channel == pendingConnection:
		pendingConnection == ""
	else:
		await client.say("You cannot close a portal that has not been opened!")

@client.command(pass_context = True)
async def migrate(op, *args):
	'''copies all of the posts in one channel to another. WIP'''

@client.event
async def on_message(message):
	await client.process_commands(message)
	
	#print('message from {} in channel {}, {}:\n\t{}'.format(message.author.name, message.channel.name, message.server.name, message.content))
	
	if message.content[0] != bot_data['prefix'] and message.author != client.user:
		
		#"chat portal"
		if message.channel in bot_data['tunnel']:
			await client.send_message(bot_data['tunnel'][message.channel], "{}:\n{}".format(message.author.name, message.content))

client.run(bot_data['token'])
