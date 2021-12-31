##########################
#Lumi-Bot v0.01          #
#Made by Diego Castro    #
##########################
import discord
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
client = discord.Client()

def get_token(id):
    id = id.lower()
    print(str(id) + ": $" + str(cg.get_price(ids=id, vs_currencies='usd')[id]['usd']))
    return cg.get_price(ids=id, vs_currencies='usd')[id]['usd']
    
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='lucas sleep'))
    

@client.event
async def on_message(message):
    if(message.author == client.user):
        return

    if(message.content.startswith('!lumi')):
        await message.channel.send('Lumi has awoken!')

    # if(message.content.startswith('$diego')):
    #     await message.channel.send('diego smells good')
    #     #await changeWatching('diego')
    
    if(message.content.startswith('$')):
        token_name = message.content.replace('$', '')
        try:
            price = get_token(token_name)
            await message.channel.send(token_name.upper() + ': $' + str(price))
        except Exception as e:
            print('Error: ', end =''), print(e)
            await message.channel.send('Unable to fetch price, please use full token name!')

async def changeWatching(name):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name + ' sleep'))

client.run(DISCORD_BOT_TOKEN)