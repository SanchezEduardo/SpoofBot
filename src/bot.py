#!/usr/bin/env python3


import os
import requests
import discord
import time
import math
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime, timedelta
from discord.utils import get


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = commands.Bot(command_prefix='.', help_command=None)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!\n')

    print(f'{client.user} is connected to the following servers')
    for x, guild in enumerate(client.guilds, 1):
      print(f'{x}. {guild}, {guild.id}')


@client.command(name='help')
async def help(ctx):
  """
  .help command that shows how to use the bot and available commands
  """
  embed=discord.Embed(title="Help", description="How to use the bot...")
  embed.add_field(name="Commands", value=".help\n.lookup", inline=False)
  embed.add_field(name=".help", value="How to use the bot", inline=False)
  embed.add_field(name=".lookup", value=".lookup follows the following format\n.lookup [region] [summonerName] [champion] [enemy champion]\nsummonerName may not contain any spaces.", inline=False)
  embed.add_field(name="Regions", value="br, eun, euw, jp, kr, la1, la2, na, oc, ru, tr", inline=False)
  embed.add_field(name="Example Input", value=".lookup na noodlz kindred ezreal", inline=False)
  await ctx.send(embed=embed)


@client.command(pass_context=True)
async def lookup(ctx, arg1, arg2, arg3, arg4):
  """
  Attributes
  regions : dict
    valid regions that user may input, using simpler terms to grab actual key value 
  region : str
    storing argument 1 into region to make request to url 
  username : str
    storing argument 2 into username to make request to url 
  champion : str
    storing argument 3 into champion to make request to url 
  enemy_champion : string
    storing argument 4 into champion to make request to url 
  url : str
    a formatted string containing the arguments to make a request to the proxy rest api containing matches info returned from SpoofHelper
  response : json
    returns the json response from the rest api url
  difference : int
    calculating how long ago between now and the time the match was created
  days : int
    storing the difference into days
  ago : str
    formatted string saying how long ago the game was created, rounds to days/months/years
  """
  regions = {"br": "br1", "eun":"eun1", "euw":"euw1", "jp":"jp1", "kr":"kr", "la1":"la1", "la2":"la2", "na":"na1", "oce":"oc1", "ru":"ru", "tr":"tr1"}
  servers = {"br1": "br", "eun1": "eune", "euw1": "euw", "la1": "lan", "la2": "las", "na1": "na", "oce1": "oce", "ru": "ru", "jp1": "jp", "kr": "kr", "tr1": "tr"}

  region = regions.get(arg1)
  username = arg2.capitalize()
  champion = arg3.capitalize()
  enemy_champion = arg4.capitalize()

  url = f'http://127.0.0.1:5000/{region}/username={username}&champion={champion}&enemy_champion={enemy_champion}'
  print(url)
  print('Invoked lookup() command, searching for {username} matches. Match up {champion} vs {enemyChamp}'.format(username=arg1, champion=arg2, enemyChamp=arg3))
  response = requests.get(url).json()

  # creating list of embed objects containing the matches
  for page, match_id in enumerate(response, 1):
    now = datetime.fromtimestamp(time.time())
    date_time = datetime.fromtimestamp(response[match_id]['date']).strftime('%Y-%m-%d')
    date = datetime.fromtimestamp(response[match_id]['date'])
    server = servers.get(region)
    game_id = response[match_id]['gameId']
    game_version = response[match_id]['gameVersion']
    # formatted url link that will be used to redirect users to Riot's match history page
    url2 = f'https://matchhistory.{server}.leagueoflegends.com/en/#match-details/{region.upper()}/{game_id}?tab=overview'

    difference = now - date
    days = difference.days
    ago = ''

    # storing responses for matchid -> champion in another variable to shorten length of lines
    response_champion = response[match_id][champion]
    response_enemy_champion = response[match_id][enemy_champion]

    # storing responses for username in another variable to shorten length of lines
    username = response_champion['username']
    enemy_username = response_enemy_champion['username']

    # storing json response values into a formatted string to use later in the embed message
    champion_kda = f"{response_champion['kills']}/{response_champion['deaths']}/{response_champion['assists']}"
    enemy_champion_kda = f"{response_enemy_champion['kills']}/{response_enemy_champion['deaths']}/{response_champion['assists']}"

    champion_items = f"{response_champion['item0']}, {response_champion['item1']}, {response_champion['item2']}, {response_champion['item3']}, {response_champion['item4']}, {response_champion['item5']}, {response_champion['item6']}"
    enemy_champion_items = f"{response_enemy_champion['item0']}, {response_enemy_champion['item1']}, {response_enemy_champion['item2']}, {response_enemy_champion['item3']}, {response_enemy_champion['item4']}, {response_enemy_champion['item5']}, {response_enemy_champion['item6']}"

    champion_runes = f"{response_champion['perk0']}, {response_champion['perk1']}, {response_champion['perk2']}, {response_champion['perk3']}, {response_champion['perk4']}, {response_champion['perk5']}"
    enemy_champion_runes = f"{response_enemy_champion['perk0']}, {response_enemy_champion['perk1']}, {response_enemy_champion['perk2']}, {response_enemy_champion['perk3']}, {response_enemy_champion['perk4']}, {response_enemy_champion['perk5']}"
    
    champion_perks = f"{response_champion['statPerk0'] or 'None'}, {response_champion['statPerk1'] or 'None'}, {response_champion['statPerk2'] or 'None'}"
    enemy_champion_perks = f"{response_enemy_champion['statPerk0'] or 'None'}, {response_enemy_champion['statPerk1'] or 'None'}, {response_enemy_champion['statPerk2'] or 'None'}"

    champion_spells = f"{response_champion['spell1']}, {response_champion['spell2']}"
    enemy_champion_spells = f"{response_enemy_champion['spell1']}, {response_enemy_champion['spell2']}"
    
    # splitting gameVersion to make it more use friendly and dispaying as patch with major.minor
    game_version_split = game_version.split('.')
    patch = f'{game_version_split[0]}.{game_version_split[1]}'

    # formatting ago string which displays how long ago the game was played
    if days / 30.4167 < 1:
      ago = str(days) + ' days ago'
    if days / 30.4167 > 1 and days / 30.4167 < 11.90:
      months = math.floor(days / 30.4167)
      ago = str(months) + ' months ago' 
    if days / 30.4167 > 11.90:
      years = math.floor((days / 30.4167) / 12)
      ago = str(years) + ' year(s) ago'
    
    # creating discord embed message with the details for the game
    embed = discord.Embed (
    title = ago,
    url=url2,
    description = f'Patch: {patch}\nDate: {date_time}\nMatch Up: {champion} ({username}) vs {enemy_champion} ({enemy_username})',
    colour = discord.Colour.blue() if response_champion['win'] == True else discord.Colour.red()
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
  """
  checking error handling
  - Missing Required Argument
  """
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please pass in all required arguments. Example: .na')
client.run(TOKEN)
