# Importing libraries
import discord
import os
import asyncio
import youtube_dl
import time
import yt_dlp as youtube_dl
import requests
from discord.ui import button, view
from discord.ext import commands

# Discord bot Initialization

key = "TOKEN_DISCORD_BOT_HERE"

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

voice_clients = {}

discord.utils.setup_logging()

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

# This event happens when the bot gets run
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        await ctx.author.voice.channel.connect()
    else:
        await ctx.send("Please Join Voice channel to run this command")
        
# This event happens when a message gets sent
@client.event
async def on_message(msg):
    if msg.content.startswith("?play"):
        try:
            print(f"2222")
            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("error")

        print(f"3333")

        try:
            url = msg.content.split()[1]
            print(f"4444", url)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            print(f"5555")
            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\\ffmpeg\\ffmpeg.exe")
            
            voice_clients[msg.guild.id].play(player)

        except Exception as err:
            print(err)


    if msg.content.startswith("?pause"):
        try:
            voice_clients[msg.guild.id].pause()
        except Exception as err:
            print(err)

    # This resumes the current song playing if it's been paused
    if msg.content.startswith("?resume"):
        try:
            voice_clients[msg.guild.id].resume()
        except Exception as err:
            print(err)

    # This stops the current playing song
    if msg.content.startswith("?stop"):
        try:
            voice_clients[msg.guild.id].stop()
            await voice_clients[msg.guild.id].disconnect()
        except Exception as err:
            print(err)


client.run(key)
