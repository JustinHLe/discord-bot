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
    current_dir = (os.getcwd())
    song_dir = path = os.path.join(current_dir,'songs')
    song_queue = []
    def __init__(self,client):
        self.client = client
    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if member.bot and before.channel is not None and after.channel is None:
            for file in os.listdir(self.song_dir):
                os.remove(os.path.join(self.song_dir, file))
            self.song_queue.clear()
    ##finish adding full audio functionality
    @commands.command()
    async def play(self, ctx, url : str):
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
            print("Bot is connected already")
        else:
            for file in os.listdir(self.song_dir):
                os.remove(os.path.join(self.song_dir, file))
            self.song_queue.clear()
            await voice_channel.connect()

        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if(parsed_url.scheme != ""):
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                ydl.cache.remove()
                ydl.download([url])
                video_id = info_dict.get('id', None)
                video_title = info_dict.get('title', None)
                song = f'{video_title}-{video_id}.mp3'
                self.song_queue.append(song)
        else: 
            print('searching!')
            search_results = search(url)
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                info_dict = ydl.extract_info(search_results, download=False)
                ydl.cache.remove()
                ydl.download([search_results])
                video_id = info_dict.get('id', None)
                video_title = info_dict.get('title', None)
                song = f'{video_title}-{video_id}.mp3'
                self.song_queue.append(song)

        if(len(self.song_queue) == 1):
            start_playing(self, voice, ctx)
        else:
            await ctx.send("Added to queue")
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def stop(self,ctx):
        if(ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send('Not in VC piemp')
    @commands.command()
    async def skip(self,ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        voice.stop()



def setup(client):
    client.add_cog(Music(client))

def start_playing(self, voice, ctx):
    first_song_before_remove = self.song_queue[0]
    voice.play(discord.FFmpegPCMAudio(os.path.join(self.song_dir, first_song_before_remove)), after=lambda e : play_next(self, voice, ctx))
def play_next(self, voice, ctx):
    print("song finished")
    remove_song = self.song_queue[0]
    self.song_queue.pop(0)
    os.remove(os.path.join(self.song_dir, remove_song))
    if(len(self.song_queue) == 0):
        print('its over')
        return
    first_song_after_remove = self.song_queue[0]
    voice.play(discord.FFmpegPCMAudio(os.path.join(self.song_dir, first_song_after_remove)), after=lambda e : play_next(self, voice, ctx))
def search(url):
    query_string = urllib.parse.urlencode({
        "search_query": url
    })
    html_content = urllib.request.urlopen(
        "http://www.youtube.com/results?" + query_string
    )
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    return f'https://www.youtube.com/watch?v=Ce5gXZDQ4x0{search_results[0]}'
