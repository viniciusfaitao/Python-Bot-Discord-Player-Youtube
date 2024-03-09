import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from pathlib import Path
from AudioPlayer import AudioPlayer
from datetime import datetime

# Discord bot Initialization
load_dotenv(str(Path(__file__).parent.absolute()) + '\\.env')

key = os.environ.get("TOKEN_DISCORD")
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)
audio_player = AudioPlayer()

voice_clients = {}

discord.utils.setup_logging()


# This event happens when the bot gets run
@client.event
async def on_ready():
    print(f"{datetime.now()}Bot logged in as {client.user}")


@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
    else:
        await ctx.send("Please Join Voice channel to run this command")


# This event happens when a message gets sent
@client.event
async def on_message(msg):
    if msg.content.startswith("?play"):
        try:
            voice_client = msg.author.voice.channel
            voice_clients[voice_client.guild.id] = voice_client

            url = msg.content.split()[1]
            if not audio_player.playing:
                await audio_player.play_audio(voice_client, url)

        except Exception as err:
            print(err)

    # This resumes the current song playing if it's been paused
    if msg.content.startswith("?resume"):
        try:
            audio_player.resume()
        except Exception as err:
            print(err)

    # This stops the current playing song
    if msg.content.startswith("?stop"):
        try:
            audio_player.stop()
        except Exception as err:
            print(err)

    if msg.content.startswith("?skip"):
        try:
            audio_player.skip()
        except Exception as err:
            print(err)


if __name__ == "__main__":
    client.run(key)
