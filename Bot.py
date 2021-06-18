import discord
import youtube_dl
import os
import random
from discord import client
from discord.ext import commands
from discord import Intents
from discord import FFmpegPCMAudio

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '.',help_command=None, intents=intents) #The prefix of this bot is '.'
key = ("") #Enter bot key in between quotation marks
channelID = ("") #Enter channel ID in between quotation marks

#Events
@client.event
async def on_ready():
    await client.change_presence()
    print('Bot Status: Active')

@client.event   #Sends welcome message when new member joins
async def on_member_join(member):
    server = client.get_channel(channelID)
    
    welcomeEmbed = discord.Embed(
        title = "Welcome " + str(member)[0:-5],
        description = 'If you have any questions about the bot just type : .help',
        colour = discord.Colour.red()
    )
    await server.send(embed=welcomeEmbed)

@client.event   #Sends good bye message when new member leaves
async def on_member_remove(member):
    server = client.get_channel(channelID)
    
    goodbyeEmbed = discord.Embed(
        title = "Bye bye " + str(member)[0:-5],
        colour = discord.Colour.red()
    )
    await server.send(embed=goodbyeEmbed)

#Commands
@client.command(pass_context=True) # Shows all available commands
async def help(ctx):
    embed = discord.Embed(
        title = 'Help',
        description = 'Available commands:',
        colour = discord.Colour.red()     
    )
    prefix = '.'
    embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/852520198317539378/5cd0ca40a2d45799a8fe0a944f420a8b.png?size=256')
    embed.add_field(name=(prefix + 'help'), value='Shows all available commands.')
    embed.add_field(name=(prefix + 'introduce'), value='Bot introduction.')
    embed.add_field(name=(prefix + 'ping'), value='Response time of bot.')
    embed.add_field(name=(prefix + 'clear + [Amount to clear]'), value='Clears messages from channel.')
    embed.add_field(name=(prefix + '8ball + [Question'), value='Makes a prediction.')
    embed.add_field(name=(prefix + 'play + [Youtube URL]'), value='Starts playing music.')
    embed.add_field(name=(prefix + 'join'), value='Makes music bot join voice channel')
    embed.add_field(name=(prefix + 'leave '), value='Makes music bot leave voice channel')
    embed.add_field(name=(prefix + 'pause'), value='#Pauses music')
    embed.add_field(name=(prefix + 'resume'), value='Resumes music')
    embed.add_field(name=(prefix + 'stop'), value='Stops playing music')
    embed.set_footer(text=('Requested by: ' + ctx.message.author.name))

    await ctx.send(embed=embed)

@client.command(aliases=['Introduce']) #Bot introduction
async def introduce(ctx):
    await ctx.send("Hey, i'm your music bot!")

@client.command(aliases=['Ping']) #Response time of bot
async def ping(ctx):
    await ctx.send("Pong! " + str(round(client.latency * 1000))+ "ms")

@client.command(aliases=['Clear']) #Clears messages from channel
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit = amount)

@client.command(aliases=['8ball']) #Makes a prediction
async def _8ball(ctx, *, question):
    responses = ['zeker niet','zeker wel','nee','jazeker','ja','kleine kans','dat gaat zeker gebeuren']
    await ctx.send(f'question: {question}\nAnswer: {random.choice(responses)}')

#Music bot commands

@client.command(pass_content = True, aliases=['Play']) #Starts playing music
async def play(ctx, url:str):
    channel = ctx.message.author.voice.channel

    if not (ctx.author.voice):
        await ctx.send("You must be in a voice channel to use this command")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("There is still an other song playing, wait for song to end or use the 'stop' command")
        return

    if not (ctx.voice_client):
        await channel.connect()
    await ctx.message.add_reaction('🎶')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': 
        [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            nowPlaying = str(file)[0:-16]
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

    songEmbed = discord.Embed(
        title = 'Music Time!',
        description = 'Now playing: ' + nowPlaying,
        colour = discord.Colour.red()
    )

    songEmbed.set_footer(text='Author: ' + ctx.message.author.name)
    songEmbed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/852520198317539378/5cd0ca40a2d45799a8fe0a944f420a8b.png?size=256')
    songEmbed.add_field(name='Url: ', value=url, inline=True)
    await ctx.send(embed=songEmbed)

@client.command(aliases=['Join']) #Makes music bot join voice channel
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.message.add_reaction('✅')
    else:
        await ctx.send("You have to be in a voice channel to execute this command.")

@client.command(pass_context = True, aliases=['dc', 'Leave']) #Makes music bot leave voice channel
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.message.add_reaction('❌')
    else:
        await ctx.send("Bot is not in a voice channel.")

@client.command(pass_context = True) #Pauses music
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.message.add_reaction('⏸️')
    else:
        await ctx.send("There is no audio playing right now.")

@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.message.add_reaction('▶️')
    else:
        await ctx.send("There is no audio paused right now.")

@client.command(pass_context = True) #Stops playing music
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.message.add_reaction('🛑')

client.run(key)