import discord
import forex_python
from forex_python.converter import CurrencyRates
from discord.ext import commands



prefix = '$'
client = commands.Bot(command_prefix = prefix)
c = CurrencyRates()
version = '1.0.1'
TOKEN = 'Njg0ODAwNjEzNDE4MDA4NjU2.XmKYVw.sw3o0-tk6qcq2qr4d1Xns-Ac7Is'

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



moduleStatus = {'exchange' : 0}
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




print(TOKEN)
client.run(TOKEN)