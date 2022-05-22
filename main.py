from discord.ext import commands
import reminder
import settings

def get_prefix(bot, message):
	return commands.when_mentioned_or(['!', '?', '.'])(bot, message)

client = commands.Bot(command_prefix=get_prefix)
client.add_cog(reminder.Reminder(client))

client.run(settings.token)
