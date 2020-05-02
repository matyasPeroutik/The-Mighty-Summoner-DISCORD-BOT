import discord
import os
import requests
import forex_python
import asyncio
from forex_python.converter import CurrencyRates
from discord.ext import commands
from dotenv import load_dotenv




c = CurrencyRates()
version = '1.1.3 dev.version 2 - Embed creation'
load_dotenv()

prefix = os.getenv('PREFIX')
Token = os.getenv('DISCORD_TOKEN')
LOLapiKey = os.getenv('LOL_API')
client = commands.Bot(command_prefix = prefix)



def activation(module):
    if moduleStatus[f'{module}'] == 0:
        moduleStatus[f'{module}'] = 1
        return

    else:
        moduleStatus[f'{module}'] = 0
        return

def conversion(ammount, currency):
    converted = c.get_rate(f'{currency}', 'CZK')* float(ammount)
    return converted

def requestSummonerData(region, summonerName, apiKey):

    url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + apiKey
    print(url)

    response = requests.get(url)
    return response.json()

def requestSummonerRank(region, summonerID, apiKey):

    url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerID}?api_key={apiKey}"
    print(url)

    response1 = requests.get(url)
    return response1.json()



moduleStatus = {'exchange' : 0,
                'summoner' : 0}
pricesList = {'CZK'+'0' : 100, 
        'CZK'+'1' : 200,
        'CZK'+'2' : 350,
        'CZK'+'3' : 500,
        'CZK'+'4' : 1000,
        'CZK'+'5' : 2000,
        'EUR'+'0' : 2.5,
        'EUR'+'1' : 5,
        'EUR'+'2' : 10,
        'EUR'+'3' : 20,
        'EUR'+'4' : 35,
        'EUR'+'5' : 50,
        'PLN'+'0' : 10,
        'PLN'+'1' : 20,
        'PLN'+'2' : 50,
        'PLN'+'3' : 100,
        'PLN'+'4' : 150,
        'PLN'+'5' : 300,
        'HUF'+'0' : 1000,
        'HUF'+'1' : 2000,
        'HUF'+'2' : 3500,
        'HUF'+'3' : 5000,
        'HUF'+'4' : 10000,
        'HUF'+'5' : 20000
              
              }

rpList = {'CZK'+'0' : 480, 
        'CZK'+'1' : 990,
        'CZK'+'2' : 1850,
        'CZK'+'3' : 2680,
        'CZK'+'4' : 5400,
        'CZK'+'5' : 11030,
        'EUR'+'0' : 310,
        'EUR'+'1' : 650,
        'EUR'+'2' : 1380,
        'EUR'+'3' : 2800,
        'EUR'+'4' : 5000,
        'EUR'+'5' : 7200,
        'HUF'+'0' : 410,
        'HUF'+'1' : 880,
        'HUF'+'2' : 1600,
        'HUF'+'3' : 2340,
        'HUF'+'4' : 4770,
        'HUF'+'5' : 9630,
        'PLN'+'0' : 310,
        'PLN'+'1' : 670,
        'PLN'+'2' : 1820,
        'PLN'+'3' : 3690,
        'PLN'+'4' : 5630,
        'PLN'+'5' : 11320

        
              
              }


@client.event
async def on_ready():
    print(f'Bot is running normally. \nBot version is {version}')

@client.command()
@commands.has_permissions(administrator=True)
async def mod(ctx, action):
    activation(action)
    if moduleStatus[str(action)] == 1:
        await ctx.send(f'Module {action} has been activated')
    else:
        await ctx.send(f'Module {action} has been deactivated')

@client.command()
async def exchange(ctx, curr = 'CZK'):
    if moduleStatus['exchange'] == 1: 
        prices = [0, 1, 2, 3, 4, 5]
        rp = [0, 1, 2, 3, 4, 5]
        for i in range(6):
            ammount = (str(pricesList[f'{curr}' + f'{i}']))
            prices[i] = round(conversion(ammount, curr), 2)    
        for j in range(6):
            rp[j] = str(rpList[f'{curr}' + f'{j}'])

        await ctx.send(f""">>> ```cs\nToto jsou ceny rp, pokud budete platit v {curr}
                            \n {rp[0]}RP za {prices[0]}CZK
                            \n {rp[1]}RP za {prices[1]}CZK
                            \n {rp[2]}RP za {prices[2]}CZK
                            \n {rp[3]}RP za {prices[3]}CZK
                            \n {rp[4]}RP za {prices[4]}CZK
                            \n {rp[5]}RP za {prices[5]}CZK ```""")
    else:
        await ctx.send('Syntax error: this command is not activated')


@client.command()
async def summoner(ctx, region = None, *, summonerID = None):
    if moduleStatus['summoner'] == 0:
        responseJSON = requestSummonerData(region, summonerID, LOLapiKey)
        player = {}
        player['info'] = {}
        player['flex'] = {}
        player['sd'] = {}
        player['flexJSON'] = {}
        player['sdJSON'] = {}
        output = {}
        player['info']["Lvl"] = responseJSON["summonerLevel"]
        player['info']["Name"] = responseJSON["name"]
        player['info']["Icon"] = responseJSON["profileIconId"]
        player['info']["ID"] = responseJSON["id"]
        rankJSON = requestSummonerRank(region, player['info']["ID"], LOLapiKey)

        i=0
        for i in range(len(rankJSON)):
            temp = rankJSON[i]
            if temp["queueType"] == "RANKED_FLEX_SR":
                player['flexJSON'] = temp
            elif temp["queueType"] == "RANKED_SOLO_5x5":
                player['sdJSON'] = temp
            
        j=0
        for j in range(2):
            if j == 0:
                temp = 'flex'
                json = 'flexJSON'
            else:
                temp = 'sd'
                json = 'sdJSON'

                
            try:
                player[temp]['division'] = player[json]["tier"]
                player[temp]['rank']= player[json]["rank"]
                player[temp]['wins'] = player[json]["wins"]
                player[temp]['losses'] = player[json]["losses"]
                player[temp]['wr'] = round(100*player[temp]['wins']/(player[temp]['wins']+player[temp]['losses']), 2)
                player[temp]['LP'] = player[json]["leaguePoints"]

                output[temp] = f""" -  Rank: **{player[temp]['division']} {player[temp]['rank']}** ({player[temp]['LP']}LP)
                                    -  Winrate: **{player[temp]['wr']}%** ({player[temp]['wins']} wins, {player[temp]['losses']} losses.)"""
            except:
                output[temp] = '*Unranked*'

        summRespondMGS = discord.Embed(
            title = f"{player['info']['Name']}'s profile",
            description = f"""**Level:** {player['info']['Lvl']}""",
            colour = discord.Color.blue()
        )
        summRespondMGS.add_field(name = 'Ranked Solo/Duo', value = output['sd'], inline = False)
        summRespondMGS.add_field(name = 'Ranked Flex', value = output['flex'], inline = False)
        summRespondMGS.set_footer(text='Legius Gaming bot')
        summRespondMGS.set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/10.9.1/img/profileicon/{player["info"]["Icon"]}.png')
        await ctx.send(embed = summRespondMGS)

client.run(Token)