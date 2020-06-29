# SpoofBot
Simplistic Discord bot that filters a League of Legends player's games based on a champion match up. 
This bot was built on [SpoofHelper](https://github.com/SanchezEduardo/SpoofHelper).

![Example Run](https://i.imgur.com/9GT23sE.png)

# Game Details
* How long ago and Date
* Champion Name
* K/D/A
* Summoner Spells
* Items
* Runes Reforged
* Rune Perks

# Features
* Rate Limiter for Riot API
* Caching for quicker and more efficient response times

# Usage
```
pip3 install -r requirements.txt
# then run the rest api and discord bot alongside each other in seperate terminals...
```
then
```
./bot.py
./rest-server.py
# runs webserver on http://127.0.0.1:5000/ or http://localhost:5000/
```
or
```
python3 bot.py 
python3 rest-server.py 
# runs webserver on http://127.0.0.1:5000/ or http://localhost:5000/
```
# Implemenation
SpoofBot is an easy to use discord bot built upon endpoints to the Riot Api and creating a REST Api for the formatted data. The Riot Api allows you to retrieve up to 100 games max for a given summoner as well as filtering by champion. By having the user input a certain enemy champion, the program will go through those 100 games to check where the champions exist in the same match and will return a list of these matches. We send a formatted json response to the newly build REST Api with the details we want from the match.\

When looking up a summoner for the first time, it may take roughly 30-40 seconds before displaying the information. Caching is helpful for saving the past 100 games for a certain champion because then the program only has to check for where the champions exist in the same match. Response times are almost instant when the cache for a certain lookup already exists. 
