from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
import datetime
import discord
import asyncio
import random
import os

start_time = datetime.datetime.utcnow() # Timestamp of when the bot came online.

responses = [
"It is certain.",
"It is decidedly so.",
"Without a doubt.",
"Definitely.",
"You may rely on it.",
"As I see it, yes.",
"Most likely.",
"Signs point to yes.",
"Ask again later.",
"Better not tell you now.",
"Cannot predict now.",
"Concentrate and ask again.",
"Don't count on it.",
"My reply is no.",
"My sources say no.",
"Outlook not so good.",
"Very doubtful.",
"Nope",
"Yes, now.",
"No",
"Yes",
"No, unless?",
"Yes, unless?"]

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
    # Logs all direct messages sent to the bot and dumps them in the chosen channel.
        msg_dump_channel = DUMP_CHANNEL_HERE
        channel = self.bot.get_channel(msg_dump_channel)
        if message.guild is None and not message.author.bot:
            if (len(message.attachments)>0):
                await channel.send(f"Author: {message.author}\nAuthor ID: {message.author.id}\nAttachment: {message.attachments[0].url} \nContent: {message.content}")
            else:
                if message.guild is None and not message.author.bot:
                    await channel.send(f"Author: {message.author}\nAuthor ID: {message.author.id}\nContent: {message.content}")

    @commands.command()
    @commands.has_role('Admin')
    async def dm(self, ctx, user: discord.Member, *, content):
    # The bot will direct message the chosen user with the wanted content.
        if ctx.message.author.id in (MEMBER1, MEMBER2):
            await user.send(content)

    @commands.command()
    @commands.has_role('Admin')
    async def send(self, ctx, channel: discord.TextChannel, *, content):
    # The bot will send a message in the chosen channel with the wanted content.
        if ctx.message.author.id in (MEMBER1, MEMBER2):
            await channel.send(content)

    @commands.command()
    @commands.has_role('Admin')
    async def sendhere(self, ctx, *, content):
    # The bot will send a message in the current channel with the wanted content.
        if ctx.message.author.id in (MEMBER1, MEMBER2):
            await ctx.message.delete()
            await ctx.send(content)

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def uptime(self, ctx: commands.Context):
    # The bot checks and tells you how long it's been online.
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            now = datetime.datetime.utcnow() # Timestamp of when uptime function is run.
            delta = now - start_time
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            if days:
                time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
            else:
                time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
            uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
            await ctx.send("I have been up for {}".format(uptime_stamp))

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def invlink(self, ctx):
    # The bot will send an invite link for the chosen server.
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            await ctx.send("https://discord.gg/YOUR_SERVER_LINK")
          
    @commands.command(aliases=['8ball'])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def _8ball(self, ctx):
    # Ask a question and let the magic 8ball define your fate.
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            await ctx.send(f"{random.choice(responses)}")

    @commands.command(aliases=['flip', 'coin', 'cf'])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def coinflip(self, ctx):
    # Flips a coin for you by picking either heads or tails.
        coinsides = ['Heads', 'Tails']
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            await ctx.send(f"{ctx.author.name} flipped a coin and got {random.choice(coinsides)}!")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def rate(self, ctx, *, user: discord.Member = None):
    # The bot will rate the user from 1 to 10.
        role = discord.utils.get(ctx.guild.roles, id=ROLE1) # Anyone with this role will get a rigged result.
        role2 = discord.utils.get(ctx.guild.roles, id=ROLE2) # Anyone with this role will get a rigged result.
        user = user or ctx.author
        random.seed(user.id)
        rate_amount = random.uniform(0.0, 10.0)
        riggedrate_amount = 10.0
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            if role in user.roles:
                await ctx.send(f"I'd rate {user.name} a **{int(round(riggedrate_amount, 4))} / 10**")
            else:
                if role2 in user.roles:
                    await ctx.send(f"I'd rate {user.name} a **{int(round(riggedrate_amount, 4))} / 10**")
                else:
                    await ctx.send(f"I'd rate {user.name} a **{int(round(rate_amount, 4))} / 10**")

    @commands.command(aliases=['slots'])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def slot(self, ctx):
    # The bot will roll a slot machine for you, don't get addicted.
        role = discord.utils.get(ctx.guild.roles, id=ROLE1) # Anyone with this role will get a rigged result.
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"[ {a} {b} {c} ]\n"
        riggedslotmachine = f"[ {a} {a} {a} ]\n"
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            if role in ctx.author.roles:
                await ctx.send(f"{riggedslotmachine} All matching, you won! 🎉")
            else:
                if (a == b == c):
                    await ctx.send(f"{slotmachine} All matching, you won! 🎉")
                elif (a == b) or (a == c) or (b == c):
                    await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
                else:
                    await ctx.send(f"{slotmachine} No match, you lost 😢")

    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
    async def typing(self, ctx):
    # The bot will start typing for 60 seconds, just to throw people off in anticipation.
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            await ctx.message.delete()
            async with ctx.typing():
                await asyncio.sleep(60)
            await ctx.send(":)")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def ping(self, ctx):
    # The bot will return you it's ping in milliseconds so you know if there is any latency.
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            await ctx.send('Latency: {0}ms'.format(round(self.bot.latency, 1)))

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def emote(self, ctx, emoji :discord.Emoji):
    # The bot will show you the chosen emote in larger view (the bot must be in the server where the emote is from).
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            await ctx.message.delete()
            embed = discord.Embed(colour=0x1f0000)
            embed.set_image(url=emoji.url)
            embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=embed)
                

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def avatar(self, ctx, *, user: discord.Member = None):
    # The bot will show you the chosen user's avatar in larger view.
        user = user or ctx.author
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            await ctx.message.delete()
            if user is None:
                user = ctx.message.author
            embed = discord.Embed(title=f"**{user.name}**'s avatar", colour=0x1f0000)
            embed.set_image(url=user.avatar_url)
            embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(aliases=['cd'])
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def countdown(self, ctx):
    # The bot will count down from 5 for you.
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            countdown = ['five', 'four', 'three', 'two', 'one']
            for num in countdown:
                await ctx.send('**:{0}:**'.format(num))
                await asyncio.sleep(1)
            await ctx.send('**:ok:**')

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    @commands.has_role('Admin')
    async def extensions(self, ctx):
    # The bot will list all of it's extensions, update this when needed as it is just a bunch of text.
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            embed=discord.Embed(title="**Luna Extensions**", description="`Roles` \nContains reaction roles. \n`music` \nContains music commands. \n`Commands` \nContains all other commands. \n`Owner` \nContains tests and owner only commands. \n`Errorhandler` \nContains error messages for most common issues and errors. \n`Joins` \nContains certain actions that are triggered when new users join the server.", color=0x000000)
            await ctx.send(embed=embed)

    @commands.command(aliases=['h'])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def help(self, ctx):
    # Replaces the standard help command and shows helpful info about the bot and it's commands.
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            embed=discord.Embed(title="**Need help?**", description="You can do `?[command]` to run a command. \nSome commands require additional information after the initial command. \n\nYou can see a list of commands and categories below.\nYou can read more about a certain category by mentioning it after the `?` prefix. \n\n**Fun • 12** \n`coinflip`, `typing`, `countdown`, `emote`, `avatar`, `8ball`, `slot`, `rate`, `snipe`, `editsnipe`, `staffsnipe`, `staffeditsnipe` \n\n**Other • 5** \n`help`, `ping`, `info`, `uptime`, `invlink`", color=0x000000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def fun(self, ctx):
    # Shows you all the fun commands the bot can use.
    	if ctx.message.channel.id in (CHANNEL1, CHANNEL2) or ctx.message.author.id in (MEMBER1, MEMBER2):
            embed=discord.Embed(title="**Luna Fun Commands**", description="Here's a list of fun commands:", color=0x000000)
            embed.add_field(name=":coin: coinflip", value="Flip a coin!", inline=False)
            embed.add_field(name="💬 typing", value="The bot will start typing.", inline=False)
            embed.add_field(name="🔢 countdown", value="Starts counting down from five.", inline=False)
            embed.add_field(name="😀 emote [emote]", value="Luna views chosen server emote.", inline=False)
            embed.add_field(name=":frame_photo: avatar [user]", value="Luna views chosen Discord avatar.", inline=False)
            embed.add_field(name="choose [1] [2] ([3])", value="Let Luna help you decide something.", inline=False)
            embed.add_field(name="🎱 8ball [question]", value="Let the magic 8ball decide your fate.", inline=False)
            embed.add_field(name="🎰 slot", value="Roll the slot machine, don't get addicted!", inline=False)
            embed.add_field(name="🔟 rate [user]", value="Bot will rate the chosen user.", inline=False)
            embed.add_field(name="⏮ snipe", value="Snipes the last deleted message.", inline=False)
            embed.add_field(name="⏪ editsnipe", value="Snipes the last edited message.", inline=False)
            embed.add_field(name="⏮ staffsnipe", value="Snipes the last deleted staff message.", inline=False)
            embed.add_field(name="⏪ staffeditsnipe", value="Snipes the last edited staff message.", inline=False)
            await ctx.send(embed=embed)

    @commands.command(aliases=['i'])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def info(self, ctx):
    # Shows you a bunch of useful information about the bot.
        if ctx.message.channel.id in (CHANNEL1, CHANNEL2, CHANNEL3) or ctx.message.author.id in (MEMBER1, MEMBER2):
            embed=discord.Embed(title="**Luna Info**", color=0x000000)
            embed.set_thumbnail(url="https://i.imgur.com/BeMc3Hf.gif")
            embed.add_field(name="What is Luna?", value="I'm a useful utility and enterntainment bot. \nI help with lots of server related tasks and provide users with fun games and features.", inline=False)
            embed.add_field(name="Can I add it on my server?", value="The bot is currently not available to the public. \nIt is open source so you can follow the development [here](https://github.com/Wanrell/Lunabot).", inline=False)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CommandsCog(bot))

    
