import os

import settings
import asyncio
import discord
import csv

client = discord.Client()

channels = []

@client.event
async def on_ready():
	print(f"Bot started and logged in as {client.user}")
	print("Press Ctrl+C to stop the bot")

@client.event
async def on_message(message):
	if message.author == client.user:  # ignore messages from the bot itself
		return

	if client.user.mentioned_in(message):  # if the bot is mentioned
		if not message.author.guild_permissions.administrator:
			await message.channel.send(settings.no_permission_message)
		else:
			if settings.activation_command in message.content:
				await message.channel.send(settings.activation_message)
				channels.append(message.channel.id)
			elif settings.stop_command in message.content:
				await message.channel.send(settings.stop_message)
				channels.remove(message.channel.id)


async def background_task():
	await client.wait_until_ready()
	while not client.is_closed():
		try:
			await asyncio.sleep(settings.reminder_time_in_minutes * 60)
		except:
			pass
		for bg_channel in channels:
			await client.get_channel(bg_channel).send(settings.reminder_message)

if os.path.isfile('channels.csv'):
	with open('channels.csv', mode='r') as infile:
		reader = csv.reader(infile)
		for row in reader:
			channels.append(int(row[0]))

client.loop.create_task(background_task())

print("Starting bot...")
try:
	client.run(settings.token)
except KeyboardInterrupt:
	print("Stopping...")  # Why does this not happen?
	asyncio.run(client.close())  # This happens...
print("Bot stopped")

print("Writing data to file...")
with open('channels.csv', mode='w', newline='') as outfile:
	writer = csv.writer(outfile)
	for channel in channels:
		writer.writerow([channel])
