import discord
from discord.enums import AuditLogAction
from discord.errors import NotFound
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, MemberNotFound, MissingAnyRole, MissingPermissions

from data import *
import random
import emoji

intents = discord.Intents.default()
intents.members = True
intents.bans = True
intents.messages = True
client = commands.Bot(command_prefix = '.', intents=intents)

@client.event
async def on_ready():
    print('Bot is ready.')
    guild = client.get_guild(guild_id)
    roles = await guild.fetch_roles()
    print(roles)

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

    await client.process_commands(message)

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

@client.event
async def on_command_error(ctx, error):
    print(ctx)
    print(error)
    if(isinstance(error, CommandNotFound)):
        await ctx.send('erm cant find command')
    if(isinstance(error, MissingPermissions)):
        await ctx.send('need mawd piemp')
    if(isinstance(error, MemberNotFound)):
        await ctx.send('member not found')


@client.command()
async def ping(ctx):
    try:
        await ctx.send(f'Ping is {round(client.latency * 1000)}ms')
    except Exception as ex:
        print(ex)


@client.command()
@commands.has_permissions(administrator = True)
async def clear(ctx, amount=None):
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


@client.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, member : discord.Member, *, reason=None):
    try:
        await member.send('Hi imposter')
        await member.kick(reason=reason)
    except Exception as e:
        print("Kick Error" + e)


@client.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member : discord.Member, *, reason=None):
    try:
        await member.send('Welcome to ban world piemp')
        await member.ban(reason=reason)
    except Exception as e:
        print("Ban Error" + e)

@client.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member_id):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users: 
        user = ban_entry.user
        if (user.id) == int(member_id):
            await ctx.send(f'{user} unbanned')
            await ctx.guild.unban(user)
            return

@client.command()
async def stats(ctx, member : discord.Member):
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

        

client.run(bot_token)

