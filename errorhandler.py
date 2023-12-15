import discord
from discord.ext import commands

class ErrorHandlerCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
  # Errorhandler lets users know if they or the bot itself are missing permissions to run a command.
		if isinstance(error, commands.CommandNotFound):
			return
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f'Missing permissions: `{", ".join(error.missing_perms)}`')
			return
		if isinstance(error, commands.BotMissingPermissions):
			if ctx.author.dm_channel is None:
				await ctx.author.create_dm()
			await ctx.author.send(f'I do not have permission to `{"` and `".join(error.missing_perms)}` in that channel.')
			return
		if isinstance(error, commands.NotOwner):
			return


def setup(bot):
	bot.add_cog(ErrorHandlerCog(bot))

 
