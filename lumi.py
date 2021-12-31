##########################
#Lumi-Bot v0.02          #
#Made by Diego Castro    #
##########################
import discord
import asyncio
from time import sleep
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
client = discord.Client()

def get_token_price(id):
    id = id.lower()
    print(str(id) + ": $" + str(cg.get_price(ids=id, vs_currencies='usd')[id]['usd']))
    #return small numbers too
    return cg.get_price(ids=id, vs_currencies='usd')[id]['usd']

# async def monitor(token_name):
#     while(True):

        

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='all the coins'))
    

@client.event
async def on_message(message):
    if(message.author == client.user):
        return

    if(message.content.startswith('!lumi')):
        await message.channel.send('Lumi has awoken!')
    
    if(message.content.startswith('!fatal')):
        await message.channel.send('you died!')
    # if(message.content.startswith('$diego')):
    #     await message.channel.send('diego smells good')
    #     #await changeWatching('diego')
    
    if(message.content.startswith('$')):
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

        if(message.content == '?reset'):
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='all the coins'))
            await message.channel.send('Resetting the monitor!')
            task.cancel()
        else:
            token_name = message.content.replace('?', '')
            
            try:
                price = cg.get_price(ids=token_name.lower(), vs_currencies='usd')[token_name.lower()]['usd']
                task =  asyncio.Task(monitor(token_name))
                await message.channel.send('Now monitoring ' + token_name)
            
            except Exception as e:
                print('Error: ', end =''), print(e)
                await message.channel.send('Unable to monitor... please use full token name!')
        

async def monitor(token_name):
    while (True):
        print("monitoring ", end='')
        price = cg.get_price(ids=token_name.lower(), vs_currencies='usd')[token_name.lower()]['usd']
        print(token_name + ": $" + str(price))
        await changeWatching(price, token_name)
        await asyncio.sleep(10)

async def changeWatching(price):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='$' + str(price)))

client.run('OTI2NTQxOTkyMjE1ODM4NzUw.Yc9LeQ.88ws1B2yMeeT59AIRyOyZ3OM0Dk')