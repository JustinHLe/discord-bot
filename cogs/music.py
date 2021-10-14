from sys import int_info
from typing import OrderedDict
import discord
from discord.ext import commands
import youtube_dl
import os, os.path
from pathlib import Path
from urllib.parse import urlparse
import urllib
import re
class Music(commands.Cog):

    ydl_opts = {
        'outtmpl': '../songs/%(title)s-%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }
    ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    }
    song_dir = '../songs'
    song_queue = []
    song_name = []
    def __init__(self,client):
        self.client = client
    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if member.bot and before.channel is not None and after.channel is None:
            self.song_queue.clear()
    ##finish adding full audio functionality
    @commands.command()
    async def play(self, ctx, *, url):
        print(url)
        parsed_url = urlparse(url)
        voice_state = ctx.author.voice
        if voice_state is None:
            return await ctx.send("Enter veecee")
        text_channel = ctx.author.voice.channel
        channel = str(text_channel)
        voice_channel = discord.utils.get(ctx.guild.voice_channels, name = str(channel))
        
        channel_members = text_channel.members
        memid = []
        for member in channel_members:
            memid.append(member.id)
        if 879825594752327690 in memid:
            pass;
        else:
            self.song_queue.clear()
            await voice_channel.connect()

        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if(parsed_url.scheme != ""):
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                song_stream = info_dict["formats"][0]["url"]
                video_title = info_dict.get('title', None)
                ydl.cache.remove()
                self.song_queue.append(song_stream)
                self.song_name.append(video_title)
        else: 
            search_results = search(url)
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                info_dict = ydl.extract_info(search_results, download=False)
                video_title = info_dict.get('title', None)
                song_stream = info_dict["formats"][0]["url"]
                ydl.cache.remove()
                self.song_queue.append(song_stream)
                self.song_name.append(video_title)
        if(len(self.song_queue) == 1):
            start_playing(self, voice, ctx)
        else:
            print(self.song_queue)
            await ctx.send("Added to queue")
    
    @commands.command()
    async def stop(self,ctx):
        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.send("enter veecee to kick bot")
        else:
            if(ctx.voice_client):
                await ctx.guild.voice_client.disconnect()
            else:
                await ctx.send('Not in VC')
    @commands.command()
    async def skip(self,ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        voice.stop()
    @commands.command()
    async def queue(self, ctx):
        await ctx.send('QUEUE:')
        await ctx.send('------------------------------------------------')
        for song in self.song_name:
            await ctx.send(song)


def setup(client):
    client.add_cog(Music(client))

def start_playing(self, voice, ctx):
    print(self.song_queue)
    first_song_before_remove = self.song_queue[0]
    voice.play(discord.FFmpegPCMAudio(first_song_before_remove, **self.ffmpeg_options), after=lambda e : play_next(self, voice, ctx))
def play_next(self, voice, ctx):
    self.song_queue.pop(0)
    self.song_name.pop(0)
    print(self.song_queue)
    if(len(self.song_queue) == 0):
        print('its over')
        return
    first_song_after_remove = self.song_queue[0]
    voice.play(discord.FFmpegPCMAudio(first_song_after_remove, **self.ffmpeg_options), after=lambda e : play_next(self, voice, ctx))
def search(url):
    query_string = urllib.parse.urlencode({
        "search_query": url
    })
    html_content = urllib.request.urlopen(
        "http://www.youtube.com/results?" + query_string
    )
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    return f'https://www.youtube.com/watch?v={search_results[0]}'
