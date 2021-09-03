import discord
from discord.ext import commands 
from discord.ext.commands.errors import CommandNotFound, MemberNotFound, MissingAnyRole, MissingPermissions
import random
import emoji
from discord.enums import AuditLogAction
from responses import *
from decouple import config

class Events(commands.Cog):
    
    guild_id = config('GUILD_ID', cast = int)

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')
        await self.client.change_presence(activity = discord.Game('Counter Strike Global Offensive'))
        guild = self.client.get_guild(self.guild_id)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(ctx)
        print(error)
        if(isinstance(error, CommandNotFound)):
            await ctx.send('erm cant find command')
        if(isinstance(error, MissingPermissions)):
            await ctx.send('need mawd piemp')
        if(isinstance(error, MemberNotFound)):
            await ctx.send('member not found')

    @commands.Cog.listener()
    async def on_message(self,message):
        if(hasattr(message.channel, 'name')):
            if message.channel.name == 'depression':
                if message.author.bot == False:
                    await message.channel.send(random.choice(response))


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="general")
        welcomeDM = ['hi', emoji.emojize(f'Greetings Fapstronaut \U0001F913 \U0001F596!')]
        welcomeGeneral = ['hi', 'fed', emoji.emojize(f'Greetings Fapstronaut \U0001F913 \U0001F596!')]
        await member.send(random.choice(welcomeDM))
        role = discord.utils.get(member.guild.roles, name = 'truecels')
        try: 
            await channel.send(f'{member.mention} {random.choice(welcomeGeneral)}')
            await member.add_roles(role)
        except Exception as ex:
            print(ex)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = discord.utils.get(guild.text_channels, name="general")
        try:
            await channel.send(f'{user} is banned. Welcome to ban world piemp.')
        except Exception as ex:
            print(ex)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        async for entry in member.guild.audit_logs(limit=1):
            if entry.action == AuditLogAction.kick and entry.target == member:
                try:
                    channel = discord.utils.get(member.guild.text_channels, name="general")
                    await channel.send(f'{entry.target} has been kicked for being an imposter.')
                except Exception as ex:
                    print(ex)

            elif entry.action == AuditLogAction.ban and entry.target == member:
                pass

            elif entry.action != AuditLogAction.kick and entry.action != AuditLogAction.ban:
                try:
                    channel = discord.utils.get(member.guild.text_channels, name="general")
                    await channel.send(f'erm {entry.target} has left the server.')
                except Exception as ex:
                    print(ex)
    
def setup(client):
    client.add_cog(Events(client))