import discord
from discord.enums import AuditLogAction
from discord.ext import commands
import random
import emoji

from data import *

intents = discord.Intents.default()
intents.members = True
intents.bans = True
intents.messages = True
client = commands.Bot(command_prefix = '.', intents=intents)

@client.event
async def on_ready():
    print('Bot is ready.')
    guild = client.get_guild(guild_id)


@client.event
async def on_message(message):
    response = ['its over', 'its over dude', 'its beyond over', 'im blackpilled bro', 
    'frustration and animosity', 'tfw no gf', 'no e-girlfriend', 'i hate my life bro', 
    'im too blackpilled to do anything', 'truecel', 'ngmi', 'over before it began', 
    'blackpilled type of night']

    if(hasattr(message.channel, 'name')):
        if message.channel.name == 'depression':
            if message.author.bot == False:
                await message.channel.send(random.choice(response))
    else:
        pass

@client.event
async def on_member_join(member):
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

@client.event
async def on_member_ban(guild, user):
    channel = discord.utils.get(guild.text_channels, name="general")
    try:
        await channel.send(f'{user} is banned. Welcome to ban world piemp.')
    except Exception as ex:
        print(ex)
        
@client.event
async def on_member_remove(member):
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





# @client.command()
# async def ping(ctx):
#     await ctx.send('Ping is {0}'.format(round(client.latency * 1000)))
# async def clear(ctx, amount):
#     print(ctx)
#     await ctx.channel.purge(limit=amount)

client.run(bot_token)