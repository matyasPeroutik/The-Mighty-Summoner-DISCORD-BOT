import discord
import os
import requests
import forex_python
import asyncio
import yaml
import random
from forex_python.converter import CurrencyRates
from discord.ext import commands, tasks
from dotenv import load_dotenv











c = CurrencyRates()
version = '1.1.4 dev.version 3 - new help implementation + czech language'
load_dotenv()

prefix = os.getenv('PREFIX')
Token = os.getenv('DISCORD_TOKEN')
LOLapiKey = os.getenv('LOL_API')
client = commands.Bot(command_prefix = prefix)
client.remove_command('help')
language = os.getenv('LANGUAGE')
translatedRot = ""

currencies = {0 : 'CZK', 1 : 'EUR', 2 : 'PLN', 3 : 'HUF'}
currenciesExchange = {}








with open(r'config.yml', 'r', encoding="utf8") as ymlfile:
    cfg = yaml.load(ymlfile)


def activation(module):
    if moduleStatus[f'{module}'] == 0:
        moduleStatus[f'{module}'] = 1
        return

    else:
        moduleStatus[f'{module}'] = 0
        return





def conversionStartup():
    for i in range(4):
        currenciesExchange[i] = c.get_rate(f'{currencies[i]}', 'CZK')

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

def currencyExchange(curr, prices, rp, rate):
    for i in range(6):
        ammount = (str(pricesList[f'{curr}' + f'{i}']))
        prices[i] = round((float(ammount) * float(rate)), 2)    
    for j in range(6):
        rp[j] = str(rpList[f'{curr}' + f'{j}'])
    return 

       


def requestsRotation(region, apiKey, championDatabase):

    url = f'https://eun1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={apiKey}'
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
        'CZK'+'1' : 1020,
        'CZK'+'2' : 2020,
        'CZK'+'3' : 2960,
        'CZK'+'4' : 6000,
        'CZK'+'5' : 12460,
        'EUR'+'0' : 310,
        'EUR'+'1' : 650,
        'EUR'+'2' : 1480,
        'EUR'+'3' : 3000,
        'EUR'+'4' : 5450,
        'EUR'+'5' : 7900,
        'HUF'+'0' : 410,
        'HUF'+'1' : 940,
        'HUF'+'2' : 1760,
        'HUF'+'3' : 2630,
        'HUF'+'4' : 5440,
        'HUF'+'5' : 11060,
        'PLN'+'0' : 310,
        'PLN'+'1' : 720,
        'PLN'+'2' : 2090,
        'PLN'+'3' : 4280,
        'PLN'+'4' : 6610,
        'PLN'+'5' : 13340

        
              
              }



# TASKS

@tasks.loop(hours = 1.0)
async def renew():
    conversionStartup()
    print(requestsRotation('EUN1', LOLapiKey, cfg['CHAMPIONS']))


@client.event
async def on_ready():
    print(f'Bot is running normally. \nBot version is {version}')
    conversionStartup()

@client.command()
async def pokimane(ctx, *, member: discord.Member=None):
    imageID = random.randrange(15)
    if imageID < 5:
        try:
            if member.id == 507638492252209152:          
                url = cfg["URLs"]["pokimane"]["darkman"]
            else:
                url = cfg["URLs"]["pokimane"][imageID]
        except:
            if ctx.author.id == 507638492252209152:
                url = cfg["URLs"]["pokimane"]["darkman"]
            else:
                url = cfg["URLs"]["pokimane"][imageID]
    else :
        url = cfg["URLs"]["pokimane"][imageID]
     
    embed = discord.Embed()
    embed.set_image(url = url)
    await ctx.send(embed = embed)


@client.command(pass_context=True)
async def help(ctx):


    embed = discord.Embed(
        colour = discord.Colour.dark_red(),
        title = cfg[language]['help']['title']
    )
    
    embed.set_thumbnail(url = 'https://scontent.fprg4-1.fna.fbcdn.net/v/t1.15752-9/92830400_1095315430824506_5372434269689872384_n.png?_nc_cat=100&_nc_sid=b96e70&_nc_ohc=n8WRijel04UAX97E3Kk&_nc_ht=scontent.fprg4-1.fna&oh=ad32df8c1581cff5ac0ab6a3d7a8aa50&oe=5ED27359')

    embed.add_field(name='Exchange rates', value= cfg[language]["help"]["exrates"].replace("/comm/", f'*{prefix}exchange <country>* '), inline = False)
    embed.add_field(name='Summoner info box', value= cfg[language]["help"]["summoner"].replace("/comm/", f'{prefix}summoner <server> <summoner name>'), inline = False)
    embed.set_author(name = 'Legius Gaming', url = 'https://discord.gg/e6sBVpQ', icon_url = 'https://www.playzone.cz/sites/default/files/styles/113x113_tym/public/cheche.jpg?itok=ijaoQZHL')

    await ctx.author.send(embed = embed)
    await ctx.send(cfg[language]["help"]["message"])


@client.command()
@commands.has_permissions(administrator=True)
async def mod(ctx, action):
    activation(action)
    if moduleStatus[str(action)] == 1:
        await ctx.send(cfg[language]["commands"]["mod"]["activation"].replace("/module/", action))
    else:
        await ctx.send(cfg[language]["commands"]["mod"]["deactivation"].replace("/module/", action))


@client.command()
async def exchange(ctx, curr = 'CZK'):
    if moduleStatus['exchange'] == 1: 
        currEmbed = discord.Embed(
            title = cfg[language]["commands"]["exchange"]["title"],
            colour = discord.Colour.gold()
        )
        

        for i in range(4):
            status = False
            prices = [0, 1, 2, 3, 4, 5]
            rp = [0, 1, 2, 3, 4, 5]
            currencyExchange(currencies[i], prices, rp, currenciesExchange[i])
            currEmbed.add_field(name =cfg[language]["commands"]["exchange"]["output"].replace("/curr/", currencies[i]),
                value = f"""```  {rp[0]}RP / {prices[0]}CZK ({round(float(rp[0]) / float(prices[0]),2)} RP/CZK)
  {rp[1]}RP / {prices[1]}CZK ({round(float(rp[1]) / float(prices[1]),2)} RP/CZK)
  {rp[2]}RP / {prices[2]}CZK ({round(float(rp[2]) / float(prices[2]),2)} RP/CZK)
  {rp[3]}RP / {prices[3]}CZK ({round(float(rp[3]) / float(prices[3]),2)} RP/CZK)
  {rp[4]}RP / {prices[4]}CZK ({round(float(rp[4]) / float(prices[4]),2)} RP/CZK)
  {rp[5]}RP / {prices[5]}CZK ({round(float(rp[5]) / float(prices[5]),2)} RP/CZK)```""",
                                 inline=status)

        currEmbed.set_thumbnail(url = 'https://pointsprizes-blog.s3-accelerate.amazonaws.com/18.png')
        currEmbed.set_footer(text = 'Legius Gaming')
        await ctx.send(embed = currEmbed)



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

                if language != "ENGLISH":
                    player[temp]['division'] = cfg[language]["ranks"][player[temp]['division']]

                output[temp] = f""" -  Rank: **{player[temp]['division']} {player[temp]['rank']}** ({player[temp]['LP']}LP)
                                    -  Winrate: **{player[temp]['wr']}%** ({player[temp]['wins']} wins, {player[temp]['losses']} losses.)"""
            except:
                output[temp] = '*Unranked*'

        summRespondMGS = discord.Embed(
            title = cfg[language]["commands"]["summoner"]["title"].replace("/player/", player['info']['Name']),
            description = f"""**Level:** {player['info']['Lvl']}""",
            colour = discord.Color.blue()
        )
        summRespondMGS.add_field(name = 'Ranked Solo/Duo', value = output['sd'], inline = False)
        summRespondMGS.add_field(name = 'Ranked Flex', value = output['flex'], inline = False)
        summRespondMGS.set_footer(text='Legius Gaming bot')
        summRespondMGS.set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/10.9.1/img/profileicon/{player["info"]["Icon"]}.png')
        await ctx.send(embed = summRespondMGS)

@client.command()
async def rotation(ctx):
    rotation = (requestsRotation('EUN1', LOLapiKey, cfg['CHAMPIONS']))
    champions = {}
    championstring = ""
    for i in range(len(rotation["freeChampionIds"])):
        champions[i] = cfg["CHAMPIONS"][int(rotation["freeChampionIds"][i])]
        championstring = championstring + f'\n-{champions[i]}'

    
    rotationEmbed = discord.Embed(
        title = cfg[language]["commands"]["rotation"]["title"]        
    )
    rotationEmbed.add_field(name = cfg[language]["commands"]["rotation"]["value"],  
        value = championstring        
    )
    


    await ctx.send(embed = rotationEmbed)

client.run(Token)
