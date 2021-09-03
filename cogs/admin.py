import discord
from discord import voice_client 
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self,client):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        try:
            await member.send('Hi imposter')
            await member.kick(reason=reason)
        except Exception as e:
            print("Kick Error" + e)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        try:
            await member.send('Welcome to ban world piemp')
            await member.ban(reason=reason)
        except Exception as e:
            print("Ban Error" + e)
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx, *, member_id):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users: 
            user = ban_entry.user
            if (user.id) == int(member_id):
                await ctx.send(f'{user} unbanned')
                await ctx.guild.unban(user)
                return

    @commands.command() 
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount=None):
        if amount is None:
            await ctx.send("Enter amount of messages you want to clear")
            return
        else:
            try:    
                if ctx.channel.name == 'cool-images':
                    pass
                else:
                    await ctx.channel.purge(limit = int(amount) + 1)
            except ValueError:
                await ctx.send("Enter a number")

##Finish this and add error handling
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick_bot(self,ctx):
        voice_client = ctx.bot.voice_clients
        if voice_client and voice_client.is_connected():
            await ctx.voice_client.disconnect()
            return
        await ctx.send('not in vc piemp')

def setup(client):
    client.add_cog(Admin(client))