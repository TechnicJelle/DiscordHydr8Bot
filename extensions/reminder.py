import atexit
import csv
import os

from discord.ext import commands, tasks

import settings

channels_file = "channels.csv"

class Reminder(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.channels = []
		atexit.register(self.save_channels)

	def get_channels(self):
		return self.channels

	@commands.Cog.listener()
	async def on_ready(self):
		print("[Reminder Module] Ready!")
		self.load_channels()
		self.remind.start()
		self.interval_save.start()

	### COMMANDS ###
	@commands.command(settings.activation_command, brief=settings.activation_brief_description, description=settings.activation_description)
	async def here(self, ctx : commands.Context):
		if not ctx.author.guild_permissions.administrator:  # no permission
			await ctx.send(settings.no_permission_message)
		else:  # yes permission
			if ctx.channel.id in self.channels:  # already activated
				await ctx.send(settings.already_activated_message)
			else:  # activate
				self.channels.append(ctx.channel.id)
				await ctx.send(settings.activation_message)

	@commands.command(settings.stop_command, brief=settings.stop_brief_description, description=settings.stop_description)
	async def stop(self, ctx : commands.Context):
		if not ctx.author.guild_permissions.administrator:  # no permission
			await ctx.send(settings.no_permission_message)
		else:  # yes permission
			if ctx.channel.id in self.channels:  # deactivate
				self.channels.remove(ctx.channel.id)
				await ctx.send(settings.stop_message)
			else:  # not active
				await ctx.send(settings.not_active_message)

	@tasks.loop(minutes=settings.reminder_time_in_minutes)
	async def remind(self):
		for channel in self.channels:
			await self.client.get_channel(channel).send(settings.reminder_message)

	### DATA HANDLING ###
	@tasks.loop(minutes=10)
	async def interval_save(self):
		self.save_channels()

	def load_channels(self):
		if os.path.isfile(channels_file):
			print("[Data Loader] Loading data...")
			with open(channels_file, mode='r') as infile:
				reader = csv.reader(infile)
				for row in reader:
					self.channels.append(int(row[0]))
			print("[Data Loader] Done!")

	def save_channels(self):
		print("[Data Saver] Saving data to file...")
		with open(channels_file, mode='w', newline='') as outfile:
			writer = csv.writer(outfile)
			for channel in self.channels:
				writer.writerow([channel])
		print("[Data Saver] Done!")


def setup(bot):
	bot.add_cog(Reminder(bot))
	print("[Reminder Module] Starting...")
