import discord
import asyncio
from pathlib import Path
import yt_dlp as youtube_dl


class AudioPlayer:
    def __init__(self):
        self.voice_client = None
        self.playing = False
        self.yt_dl_opts = {
            'format': 'bestaudio/best'
        }
        self.ytdl = youtube_dl.YoutubeDL(self.yt_dl_opts)
        self.ffmpeg_options = {
            'options': "-vn"
        }

    async def play_audio(self, voice_channel, url):
        if not self.voice_client:
            self.voice_client = await voice_channel.connect()

        if not self.playing:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))
            song = data['url']
            self.playing = True
            self.voice_client.play(discord.FFmpegPCMAudio(song, **self.ffmpeg_options, executable=str(Path(__file__).parent.absolute()) + "\\ffmpeg\\ffmpeg.exe"))

            while self.voice_client.is_playing():
                await asyncio.sleep(1)

            self.playing = False
            await self.voice_client.disconnect()

    def stop(self):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()

    def resume(self):
        if self.voice_client and not self.voice_client.is_playing():
            self.voice_client.resume()

    def skip(self):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
