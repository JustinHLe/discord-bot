import discord
from discord.ext import commands 
import youtube_dl
import os 

class User(commands.Cog):
    
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def stats(self, ctx, member : discord.Member):
        await ctx.send("Avatar:")
        await ctx.send(member.avatar_url)
        await ctx.send('\n-------------------------\n')

        await ctx.send(f'Name: {member.name}\n')     
        await ctx.send(f'Nickname: {member.nick}\n')    
        await ctx.send(f'Discriminator: {member.discriminator}\n')     
        await ctx.send(f'ID: {member.id}\n')     

        await ctx.send('\n-------------------------\n')
        await ctx.send(f'Created at {member.created_at}')
        await ctx.send(f'Joined at {member.joined_at}')

    @commands.command()
    async def ping(self, ctx):
        try:
            await ctx.send(f'Ping is {round(self.client.latency * 1000)}ms')
        except Exception as ex:
            print(ex)
    
##finish adding full audio functionality
    @commands.command()
    async def play(self, ctx, url : str):
        voice_state = ctx.author.voice
        channel = ctx.author.voice.channel
        voice_channel = discord.utils.get(ctx.guild.voice_channels, name = str(channel))

        if voice_state is None:
            return await ctx.send("Enter veecee")
        await voice_channel.connect()
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError: 
            await ctx.send("Wait for song to end")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith('.mp3'):
                os.rename(file, 'song.mp3')
        
        voice.play(discord.FFmpegPCMAudio("song.mp3"))



def setup(client):
    client.add_cog(User(client))
