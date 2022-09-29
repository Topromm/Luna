from discord.ext.commands import Bot
from discord.ext import commands
from asyncio import TimeoutError
import discord
import asyncio 

class RolesCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
        # If one of the messages in payload.message_id gets a reaction the system checks for a role with the same name and gives it to the user.
		if payload.message_id in (MESSAGE1, MESSAGE2, MESSAGE3, MESSAGE4, MESSAGE5, MESSAGE6, MESSAGE7, MESSAGE8):
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
			role = discord.utils.find(lambda r : r.name == payload.emoji.name, guild.roles)
			member = member = payload.member 

			if role is not None:
				await member.add_roles(role)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
        # If one of the messages in payload.message_id gets a reaction the system checks for a role with the same name and removes it from the user.
		if payload.message_id in (MESSAGE1, MESSAGE2, MESSAGE3, MESSAGE4, MESSAGE5, MESSAGE6, MESSAGE7, MESSAGE8):
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
			role = discord.utils.find(lambda r : r.name == payload.emoji.name, guild.roles)
			member = guild.get_member(payload.user_id)

			if role is not None:
				await member.remove_roles(role)


def setup(bot):
	bot.add_cog(RolesCog(bot))

