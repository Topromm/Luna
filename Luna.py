from discord.ext.commands import Bot
from discord.ext import commands
import discord
import random
import os

intents = discord.Intents.default()
intents.members = True 

bot = commands.Bot(command_prefix="?", intents=intents)
bot.remove_command("help")
initial_extensions = [ "errorhandler", "roles", "joins", "owner", "commands"]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you | ?help"), status=discord.Status.idle)
    print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
    print('┃Logged in as: Luna              ┃')
    print('┃Lunabot', 'ID:', bot.user.id, ' ┃')
    print('┕━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')

@bot.command()
@commands.has_role("Admin")
async def load(ctx, extension_name : str):
    # Loads an extension/cog, requires Admin role.
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))

@bot.command()
@commands.has_role("Admin")
async def unload(ctx, extension_name : str):
    # Unloads an extension/cog, requires Admin role.
    bot.unload_extension(extension_name)
    await ctx.message.delete()
    await ctx.send("{} unloaded.".format(extension_name))

if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

@bot.command()
@commands.has_role("Admin")
async def reload(ctx, extension_name : str):
    # Reloads an extension/cog, requires Admin role.
    bot.reload_extension(extension_name)
    await ctx.message.delete()
    await ctx.send("{} reloaded.".format(extension_name))

@bot.command()
@commands.has_role("Admin")
async def turnoffhostpc(ctx):
    # Shuts down host PC remotely through the Discord app, requires Admin role.
    await ctx.send("Shutting down host")
    await os.system("shutdown /s /t 1")

@bot.command()
@commands.has_role("Admin")
async def shutdown(ctx):
    # Shuts the bot down remotely through the Discord app, requires Admin role.
    await ctx.send("Shutting down")
    await bot.close()


bot.run("TOKEN")
