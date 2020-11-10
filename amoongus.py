import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
from discord import FFmpegPCMAudio
import asyncio
import datetime

from gtts import gTTS
import os

from urllib import parse, request
import re
import time
from random import randint

import keyboard
import string
from datetime import datetime
from discord.ext.commands import has_permissions, MissingPermissions

PREFIX = '!'

OWNER = 280411662333247499

bot = commands.Bot(command_prefix=PREFIX, description="Amoongus")
bot.remove_command('help')

ttsMode = False
ttsUsers = []

def createMp3(message):
    tts = gTTS(message)
    tts.save('message.mp3')

#Commands:
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne + numTwo)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Lorem Ipsum asdasd", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

    await ctx.send(embed=embed)

@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    # print(html_content.read().decode())
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', html_content.read().decode())
    print(search_results)
    # I will put just the first result, you can loop the response to show more results
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

@bot.command(pass_context=True)
async def leave(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect()

@bot.command()
async def ttson(ctx):
    global ttsMode
    global ttsUsers

    ttsMode = True
    await ctx.send("text to speech mode on")
    await ctx.send(ttsUsers)

@bot.command()
async def ttsoff(ctx):
    global ttsMode
    global ttsUsers

    ttsMode = False
    #ttsUsers.remove(ctx.message.author)
    await ctx.send("text to speech mode off")

@bot.command(pass_context=True)
async def coboclient(ctx):
    channel = ctx.message.channel
    await channel.send("Coboclient unreleased v4.0.0")
    await channel.send("https://www.mediafire.com/file/wz6ex1vrajxk5gs/CoboClientEXPERIMENTAL.zip/file")

@bot.command()
async def invite(ctx):
    link = await ctx.channel.create_invite()
    await ctx.send(link)

@bot.command()
async def inviteme(ctx):
    await ctx.send("https://discord.com/oauth2/authorize?client_id=753220949372960778&scope=bot")

@bot.command()
async def docs(ctx):
    await ctx.send(file=discord.File(r'DataCollection/documentation.txt'))

@bot.command()
async def help(ctx):
    await ctx.send("```Normal Commands: \n!ping - pong \n!join - Gets the bot to join the voice channel of the user who called the command. \n!leave - Gets the bot to disconnect from whichever voice channel the bot resides in. \n!invite - The bot will send out an invite to the current server.\n!inviteme - The bot will send out the bot's invite link. \n!docs - The bot sends a .txt file of the documentation \n!help - gives this. \n!d20 {int number} - The bot will roll a d20 die (number) amount of times \n \nAdmin Commands: \n!create_role {string name} - You will be asked for a color, followed by if you want the role to be hoisted, and the 53 permissions of the role. \n!mute {@user} - The bot will mute the user if there is a 'Muted' role in the server. \n!unmute {@user} - The bot will unmute the user if there is a 'Muted' role in the server.```")

@bot.command(aliases=['play', 'queue', 'que'])
async def tts(ctx, phrase: str):
    await ctx.send('step 1')
    createMp3(phrase)
    await ctx.send('step 2')
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    audio_source = discord.FFmpegPCMAudio('message.mp3')
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)
    os.remove('message.mp3')
    await ctx.send('it worked dipshit')

@bot.command()
async def dm(ctx, member: discord.Member, *, content):
    if content == None:
        await ctx.send("Message must inclue content")
        return
    channel = await member.create_dm()
    await channel.send(f"{ctx.message.author} said '{content}'")

@bot.command()
async def roll(ctx, d: str, num: int):
    moreThan = False
    numbers = []
    if num < 1:
        await ctx.send("Cannot roll less than 1 times")
        return
    if num > 50:
        moreThan = True
        num = 50
    d = int(d[1:])
    for number in range(num):
        numbers.append(randint(1, d))
    if moreThan == True:
        await ctx.send(f'```The number you entered was greater than 50. It was automatically set to 50. \n{numbers} ```')
        return
    await ctx.send(f'```{numbers} ```')

@bot.command()
async def whereegg(ctx):
    channel = ctx.message.channel
    await channel.send(file=discord.File(r'images\whereegg.jpg'))

@bot.command()
async def tit(ctx):
    channel = ctx.message.channel
    await ctx.send("Here is a tit for your viewing")
    await channel.send(file=discord.File(r'images\tit.jpg'))

@bot.command(pass_context=True)
async def song(ctx):
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    voice.play(discord.FFmpegPCMAudio(executable=r"ffmpegF/bin/ffmpeg.exe", source=r"songs/go hard.mp3"))
    voice.source = discord.PCMVolumeTransformer(vc.source)
    voice.source.volume = 0.5

@bot.command(pass_context=True)
async def pURL(ctx, url: str):
    channel = ctx.message.author.voice.channel

@bot.command()
async def suggest(ctx):
    with open(r"DataCollection/suggestions.txt", "r+") as f:
        old = f.read()
        f.seek(0)
        f.write(f"{ctx.message.author.name}: {ctx.message.content} : at {datetime.now()} \n{old}")

#admin control
@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def mute(ctx, member: discord.Member):
    guild = ctx.guild
    for role in guild.roles:
        if role.name.lower() == "muted":
            for memberRoles in member.roles:
                if memberRoles.name.lower() == "muted":
                    await ctx.send("{} is already muted".format(member.mention))
                    return
            await member.add_roles(role)
            await ctx.send("{} has been muted".format(member.mention))
            return
    await ctx.send("No role named 'muted'. Please create the role, then try again")
@mute.error
async def mute_error(error, ctx):
    ctx.send("You do not have the required permissions to do that")


@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    for role in guild.roles:
        if role.name.lower() == "muted":
            for memberRoles in member.roles:
                if memberRoles.name.lower() == "muted":
                    await member.remove_roles(role)
                    await ctx.send("{} has been unmuted".format(member.mention))
                    return
            await ctx.send("{} is not muted".format(member.mention))
            return
    await ctx.send("No role named 'muted'. Please create the role, then try again")
@unmute.error
async def unmute_error(error, ctx):
    ctx.send("You do not have the required permissions to do that")

@bot.command()
async def amongping(ctx):
    await ctx.send('would you like to ping people?')
    @bot.listen()
    async def on_message(message):
        if message.content == 'yes':
            await ctx.send('@everyone')
            return

@bot.command()
async def roles(ctx, member: discord.Member):
    roles = []
    for role in member.roles:
        roles.append(role.name)
    roles.remove("@everyone")
    await ctx.send(f"{member.mention}'s roles: {roles}")

@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def smute(ctx, member: discord.Member):
    await member.edit(mute=True)
    
@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def unsmute(ctx, member: discord.Member):
    await member.edit(mute=False)

@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def kick(ctx, member: discord.User):
    guild = ctx.message.guild
    await guild.kick(member)
    await ctx.send(f"{member.name} has been kicked")
    return
@kick.error
async def kick_error(ctx, error):
    await ctx.send("You do not have the required permissions to do that")


#Events:
@bot.event
async def on_ready():
    #await bot.change_presence(activity=discord.Streaming(name="Help", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLahKLy8pQdCM0SiXNn3EfGIXX19QGzUG3"))
    activity = discord.Game(name="▼simp▼", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

    """
    channel = bot.get_channel(741822285157236869)
    await channel.send('!unmute <@741822285157236869>')
    """
    print('My Ready is Body')

@bot.event
async def on_disconnect():
    print("good night buckaroo")
    for guild in bot.guilds:
        voice = get(bot.voice_clients, guild=guild)
        if voice.is_connected():
            await voice.disconnect()

@bot.event
async def on_member_join(member):
    pass
@bot.event
async def on_member_update(before, after):
    pass

@bot.listen()
async def on_message(message):
    if message.author != "Amoongus#2551":
        channel = message.channel
        if "tutorial" in message.content.lower():
            pass
    if message.content.startswith('tts'):
        content = message.content[3:]
        tts = gTTS(content)
        tts.save('message.mp3')
    if message.content.startswith('!d'):
        pass
    emoji = '\N{THUMBS UP SIGN}'
    msg_content = message.content
    if "among us" in msg_content:
        await message.add_reaction(emoji)
    if 'pog' in msg_content.lower():
        try:
            await message.add_reaction('🇵')
            await message.add_reaction('🇴')
            await message.add_reaction('🇬')
        except:
            await channel.send('React error')
    
    """
    with open("data.txt","r+") as f:
        old = f.read()
        f.seek(0)
        f.write(str(message.guild.id) + '\n' + old)
    """

currentChannel= ''

#Owner only commands

@bot.command()
async def broadcast(ctx, channelID: int, *, content):
    if ctx.message.author.id == OWNER:
        channel = bot.get_channel(channelID)
        await channel.send(content)
    else:
        await ctx.send("You are not authorized to use that command")    

bot.run('TOKEN')