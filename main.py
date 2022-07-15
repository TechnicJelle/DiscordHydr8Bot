import json
from typing import Optional, Any, Union

from discord.ext import commands
import os
import settings

CHANNELS : str = "channels"
TEMPLATE : str = "template"
TEMPLATE_DEFAULT : str = "default"
# TEMPLATE_NL : str = "nl"

print("[Bot] Starting Hydr8...")

print("[Bot] Loading data...")
with open("data.json", mode='r') as infile:
	data : dict = json.load(infile)

def getChannels(): return list(data.get(CHANNELS))

def getTemplate(channelID : int) -> str:
	channel = str(channelID)
	# check if channel is in data
	if channel in data.get(CHANNELS):
		channelData = data.get(CHANNELS).get(channel)
		# check if template is in channel data
		if TEMPLATE in channelData:
			return channelData.get(TEMPLATE)
		else:
			return TEMPLATE_DEFAULT
	else:
		raise Exception("Channel not found in data")

# print(getTemplate(6982369))
print(getTemplate(858701175251795973))

# default_prefixes = ['Hydr8', 'hydr8']
#
# def get_prefix(bot, message):
# 	return commands.when_mentioned_or(*default_prefixes)(bot, message)
#
# client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, strip_after_prefix=True, description=settings.description)
#
# extensions_dir = "extensions"
# for extension in os.listdir(extensions_dir):
# 	if extension.endswith(".py"):
# 		try:
# 			client.load_extension(extensions_dir + "." + extension[:-3])
# 		except Exception as e:
# 			print(	f"""Failed to load extension with a {type(e).__name__}
# 					\n{e}""")


# open token file
with open("token", mode='r') as infile:
	token : str = infile.read()
	# client.run(token)
