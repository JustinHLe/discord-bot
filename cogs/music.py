from typing import OrderedDict
import discord
from discord.ext import commands
import youtube_dl
import os, os.path
from pathlib import Path
import glob

class Music(commands.Cog):

    ydl_opts = {
        'outtmpl': './songs/%(title)s-%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }
    song_dir = "./songs"
    song_data = OrderedDict()
    song_queue = []
    def __init__(self,client):
        self.client = client
    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if member.bot and before.channel is not None and after.channel is None:
            print('bot leaving')
            for file in os.listdir(self.song_dir):
                print(file)
                os.remove(os.path.join(self.song_dir, file))
            self.song_data.clear()


    ##finish adding full audio functionality
    @commands.command()
    async def play(self, ctx, url : str):
        voice_state = ctx.author.voice
        text_channel = ctx.author.voice.channel
        channel = str(text_channel)
        voice_channel = discord.utils.get(ctx.guild.voice_channels, name = str(channel))

        if voice_state is None or text_channel is None:
            return await ctx.send("Enter veecee")
        
        channel_members = text_channel.members
        memid = []
        for member in channel_members:
            memid.append(member.id)
        if 879825594752327690 in memid:
            print("Bot is connected already")
        else:
            await voice_channel.connect()

        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.cache.remove()
            ydl.download([url])
        for file in os.listdir(self.song_dir):
            if os.path.getmtime(os.path.join(self.song_dir, file)) in self.song_data:
                pass
            else:
                self.song_data[os.path.getmtime(os.path.join(self.song_dir, file))] = file

        if(len(self.song_data) == 1):
            start_playing(self, voice, ctx)
        else:
            print("we have songs")
    
        
    @commands.command()
    async def sort(self,ctx):
        print('sorting')
        print(self.song_data)




    @commands.command()
    @commands.has_permissions(administrator = True)
    async def stop(self,ctx):
        if(ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send('Not in VC piemp')


def setup(client):
    client.add_cog(Music(client))

def start_playing(self, voice, ctx):
    print(voice)
    first_song_before_remove = list(self.song_data.values())[0]
    voice.play(discord.FFmpegPCMAudio(os.path.join(self.song_dir, first_song_before_remove)), after=lambda e : play_next(self, voice, ctx))
async def play_next(self, voice, ctx):
    if(len(self.song_data) == 0):
        await ctx.send("its over")
        return
    remove_key = list(self.song_data.keys())[0]
    del self.song_data[remove_key]
    first_song_after_remove = list(self.song_data.values())[0]
    voice.play(discord.FFmpegPCMAudio(os.path.join(self.song_dir, first_song_after_remove)), after=lambda e : play_next(self, voice))