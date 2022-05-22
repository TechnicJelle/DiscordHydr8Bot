from discord.ext import commands, tasks
import settings

class Reminder(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.channels = []

	@commands.Cog.listener()
	async def on_ready(self):
		print("Reminder is ready.")
		self.remind.start()

	@commands.command(settings.activation_command)
	async def here(self, ctx : commands.Context):
		if not ctx.author.guild_permissions.administrator:  # no permission
			await ctx.send(settings.no_permission_message)
		else:  # yes permission
			if ctx.channel.id in self.channels:  # already activated
				await ctx.send(settings.already_activated_message)
			else:  # activate
				self.channels.append(ctx.channel.id)
				print(self.channels)
				await ctx.send(settings.activation_message)

	@commands.command(settings.stop_command)
	async def stop(self, ctx : commands.Context):
		if not ctx.author.guild_permissions.administrator:  # no permission
			await ctx.send(settings.no_permission_message)
		else:  # yes permission
			if ctx.channel.id in self.channels:  # deactivate
				self.channels.remove(ctx.channel.id)
				print(self.channels)
				await ctx.send(settings.stop_message)
			else:  # not active
				await ctx.send(settings.not_active_message)

	@tasks.loop(seconds=10)
	async def remind(self):
		print(self.channels)
		for channel in self.channels:
			await self.client.get_channel(channel).send(settings.reminder_message)
