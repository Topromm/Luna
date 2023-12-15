from discord.ext.commands import Bot
from discord.ext import commands
import discord
import asyncio
import time

class JoinsCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member):
  # Welcomes new users in the general channel of the chosen guild/server, new accounts that are less than a day old will be kicked out.
		general = GENERAL_CHANNEL_ID
		guild = GUILD_ID
		channel = self.bot.get_channel(general)
		server = self.bot.get_guild(guild)
		if time.time() - member.created_at.timestamp() < 86400:
			await member.send("You have been kicked out of the server because your account is under 24 hours old. \nReturn back later if you are still interested. \nPermanent invite link: INVITELINK1")
			await guild.channel.send(f'{member.name} attempted to enter, but their account was under 24 hours old.')					
			await member.kick() # kicks the member if the account is less than 24 hours old. 
		else:
			await guild.channel.send(f'{member.name} has entered the server, give them a warm welcome!') # welcomes member if the account is not too young.


def setup(bot):
    bot.add_cog(JoinsCog(bot))
