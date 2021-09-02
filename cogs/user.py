import discord
from discord.ext import commands 


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

def setup(client):
    client.add_cog(User(client))