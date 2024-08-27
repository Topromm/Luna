from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from gtts import gTTS
import datetime
import discord
import asyncio
import random
import os

deletedembed = None
deletedstaffembed = None
editedembed = None
editedstaffembed= None
voice = None

class OwnerCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message_edit(self, message_before, message_after):
	# Logs edited messages, bot messages don't get logged and staff ones get logged in a separate channel.
		global editedembed
		global editedstaffembed
		msgguild = message_before.guild
		msgauthor = message_before.author
		bots = discord.utils.get(msgguild.roles, id=BOTS_ROLE)
		staff = discord.utils.get(msgguild.roles, id=STAFF_ROLE)
		logs = discord.utils.get(msgguild.channels, id=LOGS_CHANNEL)
		logs2 = discord.utils.get(msgguild.channels, id=LOGS2_CHANNEL)
		if msgauthor == self.bot.user: 
			return
		if message_before.channel.id in (LOGS_CHANNEL, LOGS2_CHANNEL):
			return
		if bots in msgauthor.roles:
			return
		if staff in msgauthor.roles:
			editedstaffembed = discord.Embed(title="", description=f"📝**Message sent by {message_before.author.mention} edited in {message_before.channel.mention}** \n**Old message** \n{message_before.content} \n\n**New message** \n{message_after.content}", color=0xfaa51b)
			editedstaffembed.set_author(name=f"{message_before.author}", icon_url=f"{message_before.author.avatar_url}")
			editedstaffembed.set_thumbnail(url=f"{message_before.author.avatar_url}")
			await logs2.send(embed=editedstaffembed)
		else:
			editedembed = discord.Embed(title="", description=f"📝**Message sent by {message_before.author.mention} edited in {message_before.channel.mention}** \n**Old message** \n{message_before.content} \n\n**New message** \n{message_after.content}", color=0xfaa51b)
			editedembed.set_author(name=f"{message_before.author}", icon_url=f"{message_before.author.avatar_url}")
			editedembed.set_thumbnail(url=f"{message_before.author.avatar_url}")
			await logs.send(embed=editedembed)

	@commands.command(aliases=['es'])
	async def editsnipe(self, ctx):
		await ctx.send(embed=editedembed)

	@commands.command(aliases=['ses'])
	@commands.has_role('Admin')
	async def staffeditsnipe(self, ctx):
		await ctx.send(embed=editedstaffembed)

	@commands.Cog.listener()
	async def on_message_delete(self, message):
	# Logs deleted messages, bot messages don't get logged and staff ones get logged in a separate channel.
		global deletedembed
		global deletedstaffembed
		msgguild = message.guild
		msgauthor = message.author
		bots = discord.utils.get(msgguild.roles, id=BOTS_ROLE)
		staff = discord.utils.get(msgguild.roles, id=STAFF_ROLE)
		logs = discord.utils.get(msgguild.channels, id=LOGS_CHANNEL)
		logs2 = discord.utils.get(msgguild.channels, id=LOGS2_CHANNEL)
		if msgauthor == self.bot.user: 
			return
		if message.channel.id in (LOGS_CHANNEL, LOGS2_CHANNEL):
			return
		if bots in msgauthor.roles:
			return
		if staff in msgauthor.roles:
			deletedstaffembed = discord.Embed(title="", description=f"🗑️**Message sent by {message.author.mention} deleted in {message.channel.mention}** \n{message.content}", color=0xf04848)
			deletedstaffembed.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}")
			deletedstaffembed.set_thumbnail(url=f"{message.author.avatar_url}")
			await logs2.send(embed=deletedstaffembed)
		else:
			deletedembed = discord.Embed(title="", description=f"🗑️**Message sent by {message.author.mention} deleted in {message.channel.mention}** \n{message.content}", color=0xf04848)
			deletedembed.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}")
			deletedembed.set_thumbnail(url=f"{message.author.avatar_url}")
			await logs.send(embed=deletedembed)

	@commands.command(aliases=['s'])
	async def snipe(self, ctx):
		await ctx.send(embed=deletedembed)

	@commands.command(aliases=['ss'])
	@commands.has_role('Admin')
	async def staffsnipe(self, ctx):
		await ctx.send(embed=deletedstaffembed)

	@commands.command()
	@commands.has_role('Admin')
	async def addrole(self, ctx, name, *, color: discord.Colour):
	# Command for creating new roles, just add a name, or even a hex color code if you want to.
		guild = ctx.guild
		await guild.create_role(name=name, color=color)
		await ctx.send("Done!")

	@commands.command()
	@commands.has_role('Admin')
	async def members(self, ctx, *args):
	# Makes a list of all server members, it's kind of spammy.
		server = ctx.message.guild
		role_name = (' '.join(args))
		role_id = server.roles[0]
		for role in server.roles:
			if role_name == role.name:
				role_id = role
				break
		else:
			await ctx.send("Role doesn't exist")
			return
		for member in server.members:
			if role_id in member.roles:
				await ctx.send(f"{member.display_name} - {member.id}")

	@commands.command(aliases=['j'])
	@commands.has_role('Admin')
	async def join(self, ctx):
	# Makes the bot join the voice channel you're in.
		global voice
		channel = ctx.message.author.voice.channel
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()
		await voice.disconnect()
		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()
		await ctx.send(f"Joined {channel}")

	@commands.command()
	@commands.has_role('Admin')
	async def tts(self, ctx, *, args):
	# Makes the bot speak a message out loud in the voice channel it's in. 
			def after_done(error):
				os.remove("gtts.mp3")
			tts = gTTS(args, lang = "en-us", slow = False)
			tts.save('gtts.mp3')
			voice.play(discord.FFmpegPCMAudio('gtts.mp3'), after=after_done)

	@commands.command(aliases=['l'])
	@commands.has_role('Admin')
	async def leave(self, ctx):
	# Makes the bot leave the voice channel you're in.
		channel = ctx.message.author.voice.channel
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if voice and voice.is_connected():
			await voice.disconnect()
			await ctx.send(f"Left {channel}")
		else:
			await ctx.send("I'm not in a voice channel")
			

	@commands.command()
	@commands.has_role('Admin')
	async def embed(self, ctx, title, *, desc):
	# Sends an embed message for you. First word will be the title, rest will be description.
			embed=discord.Embed(title=title, description=desc, color=0x000000)
			await ctx.message.delete()
			await ctx.send(embed=embed)

	@commands.command()
	@commands.has_role('Admin')
	async def embedimage(self, ctx, image):
	# Sends an image/gif in an embed for you. Just use a link after the command.
			embed=discord.Embed(title=" ", description="", color=0x000000)
			embed.set_image(url=f"{image}")
			await ctx.message.delete()
			await ctx.send(embed=embed)

	@commands.command()
	@commands.has_role('Admin')
	async def editembed(self, ctx):
	# Edits an embed message sent by the bot, update the channel and message ID's below and edit the embed part to what you want to change an existing embed to.
			channel = self.bot.get_channel(CHANNEL_ID)
			message = await channel.fetch_message(MESSAGE_ID)
			embed=discord.Embed(title="**new name**", description="new description", color=0x000000)
			await message.edit(embed=embed)


def setup(bot):
    bot.add_cog(OwnerCog(bot))
