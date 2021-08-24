import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):
    response = ['its over', 'its over dude', 'its beyond over', 'im blackpilled bro', 
    'frustration and animosity', 'tfw no gf', 'no e-girlfriend', 'i hate my life bro', 
    'im too blackpilled to do anything', 'truecel', 'ngmi', 'over before it began', 
    'blackpilled type of night']

    if message.channel.name == 'depression':
        if message.author.bot == False:
            print("hi")
            #await message.channel.send(random.choice(response))

@client.command()
async def ping(ctx):
    await ctx.send('Ping is {0}'.format(round(client.latency * 1000)))
async def clear(ctx, amount):
    print(ctx)
    #await ctx.channel.purge(limit=amount)

client.run('ODc5ODI1NTk0NzUyMzI3Njkw.YSVXcA.4P2K1XC7RS9yA_qTu76ZdJR_QW4')