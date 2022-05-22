from discord.ext import commands
import os
import settings

print("[Bot] Starting Hydr8...")

default_prefixes = ['Hydr8', 'hydr8']

def get_prefix(bot, message):
	return commands.when_mentioned_or(*default_prefixes)(bot, message)

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, strip_after_prefix=True, description=settings.description)

extensions_dir = "extensions"
for extension in os.listdir(extensions_dir):
	if extension.endswith(".py"):
		try:
			client.load_extension(extensions_dir + "." + extension[:-3])
		except Exception as e:
			print(	f"""Failed to load extension with a {type(e).__name__}
					\n{e}""")

client.run(settings.token)
