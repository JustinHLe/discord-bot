import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.bans = True
intents.messages = True
client = commands.Bot(command_prefix = '.', intents=intents)

from data import *

@client.command()
async def load(ctx,extension):
    client.load_extension(f'cogs.{extension}')
    print(f'cogs.{extension} loaded')

@client.command()
async def unload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')
    print(f'cogs.{extension} unloaded')

@client.command()
async def reload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'cogs.{extension} reloaded')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        

client.run(bot_token)

