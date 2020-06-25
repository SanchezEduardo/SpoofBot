import os
import requests
import discord
import time
import math
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime, timedelta

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='.', help_command=None)

# http://127.0.0.1:5000/na1/username=noodlz&champion=kindred&enemy_champion=ezreal

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!\n')

    print(f'{client.user} is connected to the following servers')
    for x, guild in enumerate(client.guilds, 1):
      print(f'{x}. {guild}, {guild.id}')

@client.command(name='help')
async def help(ctx):
  embed=discord.Embed(title="Help", description="How to use the bot...")
  embed.add_field(name="Commands", value=".help\n.lookup", inline=False)
  embed.add_field(name=".help", value="How to use the bot", inline=False)
  embed.add_field(name=".lookup", value=".lookup follows the following format\n.lookup [region] [summonerName] [champion] [enemy champion]\nsummonerName may not contain any spaces.", inline=False)
  embed.add_field(name="Regions", value="br, eun, euw, jp, kr, la1, la2, na, oc, ru, tr", inline=False)
  embed.add_field(name="Example Input", value=".lookup na noodlz kindred ezreal", inline=False)
  await ctx.send(embed=embed)

@client.command(name='lookup')
async def lookup(ctx, arg1, arg2, arg3, arg4):
  regions = {"br": "br1", "eun":"eun1", "euw":"euw1", "jp":"jp1", "kr":"kr", "la1":"la1", "la2":"la2", "na":"na1", "oc":"oc1", "ru":"ru", "tr":"tr1"}
  region = regions.get(arg1)
  username = arg2.capitalize()
  champion = arg3.capitalize()
  enemy_champion = arg4.capitalize()

  url = f'http://127.0.0.1:5000/{region}/username={username}&champion={champion}&enemy_champion={enemy_champion}'
  print('Invoked lookup() command, searching for {username} matches. Match up {champion} vs {enemyChamp}'.format(username=arg1, champion=arg2, enemyChamp=arg3))
  response = requests.get(url).json()

  for match_id in response:
    now = datetime.fromtimestamp(time.time())
    date = datetime.fromtimestamp(response[match_id]['date'])
    difference = now - date
    days = difference.days
    ago = ''

    champion_username = response[match_id][champion]['username']
    enemy_champion_username = response[match_id][enemy_champion]['username']

    champion_kda = f"{response[match_id][champion]['kills']}/{response[match_id][champion]['deaths']}/{response[match_id][champion]['assists']}"
    enemy_champion_kda = f"{response[match_id][enemy_champion]['kills']}/{response[match_id][enemy_champion]['deaths']}/{response[match_id][champion]['assists']}"

    champion_items = f"{response[match_id][champion]['item0']}, {response[match_id][champion]['item1']}, {response[match_id][champion]['item2']}, {response[match_id][champion]['item3']}, {response[match_id][champion]['item4']}, {response[match_id][champion]['item5']}, {response[match_id][champion]['item6']}"
    enemy_champion_items = f"{response[match_id][enemy_champion]['item0']}, {response[match_id][enemy_champion]['item1']}, {response[match_id][enemy_champion]['item2']}, {response[match_id][enemy_champion]['item3']}, {response[match_id][enemy_champion]['item4']}, {response[match_id][enemy_champion]['item5']}, {response[match_id][enemy_champion]['item6']}"

    champion_runes = f"{response[match_id][champion]['perk0']}, {response[match_id][champion]['perk1']}, {response[match_id][champion]['perk2']}, {response[match_id][champion]['perk3']}, {response[match_id][champion]['perk4']}, {response[match_id][champion]['perk5']}"
    enemy_champion_runes = f"{response[match_id][enemy_champion]['perk0']}, {response[match_id][enemy_champion]['perk1']}, {response[match_id][enemy_champion]['perk2']}, {response[match_id][enemy_champion]['perk3']}, {response[match_id][enemy_champion]['perk4']}, {response[match_id][enemy_champion]['perk5']}"
    
    champion_perks = f"{response[match_id][champion]['statPerk0']}, {response[match_id][champion]['statPerk1']}, {response[match_id][champion]['statPerk2']}"
    enemy_champion_perks = f"{response[match_id][enemy_champion]['statPerk0']}, {response[match_id][enemy_champion]['statPerk1']}, {response[match_id][enemy_champion]['statPerk2']}"

    champion_spells = f"{response[match_id][champion]['spell1']}, {response[match_id][champion]['spell2']}"
    enemy_champion_spells = f"{response[match_id][enemy_champion]['spell1']}, {response[match_id][enemy_champion]['spell2']}"
    
    if days / 30.4167 < 1:
      ago = str(days) + ' days ago'
    if days / 30.4167 > 1 and days / 30.4167 < 11.90:
      months = math.floor(days / 30.4167)
      ago = str(months) + ' months ago' 
    if days / 30.4167 > 11.90:
      years = math.floor((days / 30.4167) / 12)
      ago = str(years) + ' year(s) ago'

    embed = discord.Embed (
    title = ago,
    description = f'Match details... {champion} ({champion_username}) vs {enemy_champion} ({enemy_champion_username})',
    colour = discord.Colour.blue() if response[match_id][champion]['win'] == True else discord.Colour.red()
    )

    embed.add_field(name="Champion", value=champion, inline=True)
    embed.add_field(name="K/D/A", value=champion_kda, inline=True)
    embed.add_field(name="Summoner Spells", value=champion_spells, inline=True)
    embed.add_field(name="Items", value=champion_items, inline=True)
    embed.add_field(name="Runes", value=champion_runes, inline=True)
    embed.add_field(name="Rune Perks", value=champion_perks, inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="Champion", value=enemy_champion, inline=True)
    embed.add_field(name="K/D/A", value=enemy_champion_kda, inline=True)
    embed.add_field(name="Summoner Spells", value=enemy_champion_spells, inline=True)
    embed.add_field(name="Items", value=enemy_champion_items, inline=True)
    embed.add_field(name="Runes", value=enemy_champion_runes, inline=True)
    embed.add_field(name="Rune Perks", value=enemy_champion_perks, inline=True)

    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please pass in all required arguments. Example: .na')
client.run(TOKEN)
