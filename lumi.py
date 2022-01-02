##########################
#Lumi-Bot v0.04          #
#Made by Diego Castro    #
##########################
import discord
import asyncio
import time
import os
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv
load_dotenv('.env')

cg = CoinGeckoAPI()
client = discord.Client()

@client.event
async def on_ready():
    t = time.localtime()
    logging_time = time.strftime('%I:%M:%S %p', t)
    print('[' + logging_time + ']: Welcome to LumiBot [v0.04]')
    print('[' + logging_time + ']: ', end= ''), print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='all the coins'))

flag = True

@client.event 
async def on_message(message):
    if(message.author == client.user):
        return

    if(message.content.startswith('!lumi')):
        await message.channel.send('Lumi has awoken!')
    
    if(message.content.startswith('!fatal')):
        await message.channel.send('you died!')
    
    if(message.content.startswith('$')):
        if(message.content == '$'):
            return
        if(message.content == '$eth'):
            price = get_token_price('ethereum')
            await message.channel.send('ETH: $' + str(price))

        elif(message.content == '$btc'):
            price = get_token_price('bitcoin')
            await message.channel.send('BTC: $' + str(price))

        else:
            token_name = message.content.replace('$', '')
            try:
                price = get_token_price(token_name)
                await message.channel.send(token_name.upper() + ': $' + str(price))

            except Exception as e:
                print('Error: ', end =''), print(e)
                await message.channel.send('Unable to fetch price, please use full token name!')

    
    if(message.content.startswith('?')):
        global task
        global flag
        if(message.content == '?'):
            return

        if(message.content == '?reset'):
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='all the coins'))
            await message.channel.send('Resetting the monitor!')
            task.cancel()
            flag = True

        else:
            token_name = message.content.replace('?', '')
            try:
                if(flag):
                    price = cg.get_price(ids=token_name.lower(), vs_currencies='usd')[token_name.lower()]['usd']
                    task =  asyncio.Task(monitor(token_name))
                    await message.channel.send('Now monitoring ' + token_name)
                    flag = False
                else:
                    await message.channel.send('Error cannot monitor two coins at once. ?reset first!')
            
            except Exception as e:
                print('Error: ', end =''), print(e)
                await message.channel.send('Unable to monitor... please use full token name!')

def get_token_price(id):
    id = id.lower()
    t = time.localtime()
    logging_time = time.strftime('%I:%M:%S %p', t)
    price = cg.get_price(ids=id, vs_currencies='usd')[id]['usd']
    print('[' + logging_time + ']: ' + str(id) + ': $' + str(price))
    return price
    
async def monitor(token_name):
    while (True):
        t = time.localtime()
        logging_time = time.strftime('%I:%M:%S %p', t)

        price = cg.get_price(ids=token_name.lower(), vs_currencies='usd')[token_name.lower()]['usd']
        print('[' + logging_time + ']: ', end= '')
        print('Monitoring ', end='')
        print(token_name + ': $' + str(price))
        await changeWatching(price)
        await asyncio.sleep(10)

async def changeWatching(price):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='$' + str(price)))

client.run(os.getenv('DISCORD_BOT_TOKEN'))