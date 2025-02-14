#Importing necessary libraries.

import discord
from discord.ext import commands
import random
import praw
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import wolframalpha


#Initializing wolfram client and setting token.

wolfClient = str(os.getenv('WOLF'))
client2 = wolframalpha.Client(wolfClient)
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Cool").sheet1
token = os.getenv('TOKEN')
client = commands.Bot(command_prefix = '_')
client.remove_command('help')
reddit = praw.Reddit("bot1", user_agent="Cyan's program 1.0 by /u/RosogollaBot")


#List of features

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('with Zyen'))
    print('bot is ready')


@client.command(aliases=['Ping'])
async def ping(ctx):
        embed = discord.Embed(
        colour = discord.Colour(int("F8F8F8", 16))
        )

        embed.add_field(name='Ping', value=(f'```{round(client.latency * 1000)}ms```'), inline='False')
        await ctx.send(embed=embed)


@client.command(aliases=['8ball'])
async def eightoborru(ctx,* question):
    solved = ("")
    for x in question:
     solved += x
     solved += " "
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes – definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 "Don't count on it.",
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']

    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16))
    )

    embed.add_field(name='Question', value=(f'```{solved}```'), inline='False')
    embed.add_field(name='Answer', value=(f'```{random.choice(responses)}```'), inline='True')
    await ctx.send(embed=embed)


@client.command(aliases=['Clear'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    amount += 1
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16))
    )

    embed.add_field(name='Kicked Successfully', value=(f'Kicked {member.mention}'), inline='False')
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)


    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16))
    )

    embed.add_field(name='Banned Successfully', value=(f'Banned {member.mention}'), inline='False')
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user=None):

    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
    except:
        await ctx.send("Error: user could not be found!")
        return

    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason="Responsible moderator: "+ str(ctx.author))
        else:
            await ctx.send("User not banned!")
            return

    except discord.Forbidden:
        await ctx.send("I do not have permission to unban!")
        return

    except:
        await ctx.send("Unbanning failed!")
        return

    await ctx.send(f"Successfully unbanned {user.mention}!")


@client.command(aliases=['red', 'Red', 'reddit'])
async def Reddit(ctx, sub: str):
    submision = reddit.subreddit(sub).hot()
    pick = random.randint(1,25)
    embed = discord.Embed(colour = discord.Colour(int("F8F8F8", 16)), description = f'{ctx.message.author.mention}')

    for i in range(0,pick):
        submission = next(x for x in submision if not x.stickied)

    if submission.over_18 == True:
        embed.add_field(name="Error", value="Post is too lewd ><")
        await ctx.send(embed=embed)
    else:
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, message):
    embed = discord.Embed(
    colour= discord.Colour(int("F8F8F8", 16))
    )

    embed.add_field(name="Error", value=f'```{message}```')
    await ctx.send(embed=embed)


@client.command(aliases=['Say', 's', 'S'])
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)


@client.command()
async def hug(ctx, member : discord.Member):
    huggifs = [
     'https://66.media.tumblr.com/33c8d3b0b83514b16fc5fb06589ceb11/tumblr_nlrld1pXss1tros9go1_500.gif',
     'https://media1.tenor.com/images/ce9dc4b7e715cea12604f8dbdb49141b/tenor.gif?itemid=4451998',
     'https://i.kym-cdn.com/photos/images/newsfeed/001/230/145/957.gif',
     'https://media1.tenor.com/images/7ed465434ba3c9b969944f2e341c86e8/tenor.gif?itemid=7876658',
     'https://media1.tenor.com/images/1c692b486c6a43a35a5f32e91b1e6a5f/tenor.gif?itemid=9309062'
     'https://media.tenor.com/images/853bb442dd8eae619c4a524ffad4261c/tenor.gif'
     'https://media.tenor.com/images/3a9d2bd1bde9ed8ea02b2222988be6da/tenor.gif'
     'https://media.tenor.com/images/71ae3fe37388e0d4ce1575090bf6cbdc/tenor.gif']


    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16)),
    description = f'{ctx.message.author.mention} hugs <@{member.id}>'
    )

    embed.set_image(url = random.choice(huggifs))
    await ctx.send(embed=embed)


@client.command()
async def pat(ctx, member : discord.Member):
    patgifs = [
    'https://i.pinimg.com/originals/cd/7a/7e/cd7a7ea15b05b065bc59962cc288f5d8.gif'
    'https://media.tenor.com/images/69fb17b3eafe27df334f9f873473d531/tenor.gif'
    'https://media.tenor.com/images/27e35e2e393576d98a574d2dd75ca1b1/tenor.gif'
    'https://media.tenor.com/images/c74e55214ecad0c056a372a9eabc5743/tenor.gif']


    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16)),
    description = f'{ctx.message.author.mention} pats <@{member.id}>'
    )

    embed.set_image(url = random.choice(patgifs))
    await ctx.send(embed=embed)


@client.command()
async def commands(ctx):
    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16))
    )

    embed.set_author(name='Commands')
    embed.add_field(name='Administration', value='`kick, ban, unban, clear`', inline = True)
    embed.add_field(name='Fun', value='`8ball, ping, say`', inline = True)
    embed.add_field(name='Imagery', value='`Reddit`', inline = True)
    embed.add_field(name='Misc', value='`WolframAlpha, Schedule`')

    await ctx.send(embed=embed)


@client.command(aliases = ["scd"])
async def Schedule(ctx, amt: int):
    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16))
    )

    embed.set_author(name='2v2 Schedule')
    embed.add_field(name='ID', value=f'`{sheet.row_values(amt+1)[0]}`')
    embed.add_field(name='Team 1', value=f'`{sheet.row_values(amt+1)[3]}`')
    embed.add_field(name='Team 2', value=f'`{sheet.row_values(amt+1)[4]}`')
    embed.add_field(name='Date', value=f'`{sheet.row_values(amt+1)[1]}`')
    embed.add_field(name='Time', value=f'`{sheet.row_values(amt+1)[2]}`')



    await ctx.send(embed=embed)

@client.command(aliases=['cyan'])
async def cyan(ctx):
        embed = discord.Embed(
        colour = discord.Colour(int("F8F8F8", 16))
        )

        embed.add_field(name='Ping', value=('god'), inline='False')
        await ctx.send(embed=embed)


@client.command(aliases = ['wa'])
async def WolframAlpha(ctx, query: str):
    res = client2.query(query)

    embed = discord.Embed(
        colour = discord.Colour(int("F8F8F8", 16))
        )

    try:
        output = next(res.results).text
        embed.add_field(name='WolframAlpha', value=f'```{output}```')
        await ctx.send(embed=embed)

    except:
        embed.add_field(name='Error', value='Invalid Query')
        await ctx.send(embed=embed)


client.run(token)
