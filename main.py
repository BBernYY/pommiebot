from typing import Text
import discord
import random
from datetime import datetime
from discord.message import Attachment
import discord.utils
from discord.ext import commands
from discord import CategoryChannel
import json
import binaryCode as bc
import requests
pomsiesaves = open("pomsie.json", "r")
pomsie = json.load(pomsiesaves)
bot = commands.Bot(command_prefix='!p ')
bot.remove_command('help')
pomsies = list(pomsie["pomsies"].keys())
kleuren = pomsie["pomsies"]
targets = pomsie["plannen"]["!T"]
ideeen = pomsie["plannen"]["zinnen"]
WWden = pomsie["plannen"]["!W"]
dingen = pomsie["plannen"]["!I"]
grappen = pomsie["grappen"]
loopbool = False
def log(ctx, reply):
  if reply == 0:
    reply = ""
  else:
    reply = "\nreply: "+reply
  ms = "\ncommand.activate():\n"+ctx.message.content+reply+"\n"+str(ctx.author.display_name)+"\n"+str(datetime.now())
  print(ms)
def TSS(txt):
  returnage = str()
  for i in txt:
    returnage = returnage + " " + i
  return returnage.replace(" ", "", 1)
@bot.event
async def on_ready():
  print('system.startup\ntime: '+str(datetime.now()))
@bot.command()
async def help(ctx):
    embed=discord.Embed(title='Lijstje met woordjes', description='Zeg dit tegen Pommie voor antwoorden.', color=0xFF5733)
    embed.add_field(name="admin commands:", value="\n!p slachtoffer [roll of het slachtoffer] geeft slachtoffer voor plannen.\n\n!p slachtoffers [slachtoffer1,slachtoffer2]stel in welke slachtoffers er zijn voor !p slachtoffer roll. Alleen een komma tussen elk slachtoffer.\n\n!p wipe verwijdert alle !p lobby kanalen.")
    embed.add_field(name="normale commands:", value="\n!p plan stelt een plan voor.\n\n!p listen [iets] zegt wat de status van Pommie moet zijn.\n\n!p lobby [naam] maakt een lobby aan.\n\n!p set [pomsie] maakt je een pomsie.\n\n!p list geeft je een lijst met alle pomsies.\n\n!p say [tekst] zegt iets als pommie.\n\n!p config configureert de server.\n\n!p encrypt [sleutel] [titel] [tekst] beveilgt tekst. Is weer te openen met !p decrypt en een sleutel.\n\n!p decrypt [sleutel] [link van bestand] maakt tekst weer normaal als je de goede key hebt.\n\n!p getKey maakt een key voor je aan om mee te decrypten.")
    await ctx.channel.send(embed=embed)
    log(ctx, "<help command>")
@bot.command()
async def set(ctx, type):
  pomsi = discord.utils.get(ctx.guild.roles,name=type)
  await ctx.author.add_roles(pomsi)
  await ctx.channel.send("Je bent nu "+type)
  for raw in pomsies:
    i = discord.utils.get(ctx.guild.roles,name=raw)
    if i != discord.utils.get(ctx.guild.roles,name=type):
      await ctx.author.remove_roles(i)
  log(ctx, "changed role")
@bot.command()
async def plan(ctx):
  global target
  global targets
  if target == "roll":
    temp = random.choice(targets)
  else:
    temp = target
  message = str(random.choice(ideeen).replace("!W", random.choice(WWden)).replace("!T", temp).replace("!I", random.choice(dingen)).replace("!P", random.choice(pomsies)))
  await ctx.channel.send(message)
  log(ctx, message)
@bot.command()
@commands.has_role("Pomsie engineer")
async def slachtoffer(ctx, *dl):
  global target
  doel = TSS(dl)
  log(ctx, "set target")
  target = doel
  await ctx.channel.send("doelwit is nu: "+ target)
@bot.command()
@commands.has_role("Pomsie engineer")
async def slachtoffers(ctx, *lijst):
  global targets
  log(ctx, "set target roll")
  targets = lijst
  await ctx.channel.send("het zijn:\n"+"\n".join(targets))
@bot.command()
async def listen(ctx, *ag1):
  arg1 = TSS(ag1)
  log(ctx, "listens to "+arg1)
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=arg1))
  await ctx.channel.send("ik luister nu naar "+arg1)
@bot.command()
async def lobby(ctx, *nam):
  name = TSS(nam)
  log(ctx, "set lobby to "+name)
  category = discord.utils.get(ctx.guild.categories, name="Pommies Lobby's")
  await ctx.guild.create_voice_channel(name, category=category)
  await ctx.channel.send(await discord.utils.get(ctx.guild.channels, name=name).create_invite(max_age = 300))
@bot.command()
@commands.has_role("Pomsie engineer")
async def wipe(ctx):
  log(ctx, "wiped all lobbies")
  for i in discord.utils.get(ctx.guild.categories, name="Pommies Lobby's").channels:
    await i.delete()
  await ctx.message.channel.send("Wiped!")
@bot.command()
async def list(ctx):
  log(ctx, "showed pomsie list")
  await ctx.channel.send(file=discord.File("PomsiePic.png"))
@bot.command()
async def say(ctx, *txt):
  global loopbool
  text = TSS(txt)
  if loopbool:
    text = text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text + text
    loopbool = False
  log(ctx, text+", message deletion")
  message = await ctx.channel.fetch_message(ctx.channel.last_message_id)
  await message.delete()
  await ctx.channel.send(text)
@bot.command(pass_context=True)
async def config(ctx):
  log(ctx, "configged "+ctx.guild.name)
  guild = ctx.guild
  if guild.has_role(name="Pomsie engineer"):
    return
  else:
    await guild.create_category("Pommies Lobby's")
    for a in pomsies:
      await guild.create_role(name=a, color=discord.Colour(int(kleuren[a], 16)))
    await guild.create_role(name="Pomsie engineer")
@bot.command()
async def troll(ctx):
  log(ctx, "spammed lobbies")
  for i in range(20):
    channel = await ctx.guild.create_text_channel("troll")
    await channel.send(random.choice(grappen))
@bot.command()
async def roll(ctx, chances, *q):
  await ctx.channel.send(str(random.randint(0, int(chances))))
  log(ctx, "random int")
@bot.command()
async def untroll(ctx):
  for t in ctx.message.guild.text_channels:
    if t.name == "troll":
      await t.delete()
@bot.command()
async def wijsheid(ctx):
  await ctx.channel.send("Anime is cool")
@bot.command()
async def target(ctx, *args):
  await ctx.channel.send("NEE HET IS !P SLACHTOFFER JIJ DOMPOK!!!!! TYP !P HELP VOOR HULP DOMMIE :ROLLING_EYES:")
@bot.command()
async def geef(ctx, thing):
  if thing == "klap":
    ans = "WEEEEEEEEEEEEEEEEEEH"
  elif thing == "knuffel":
    ans = "dankjewel!"
  elif thing == "straf":
    ans = "You underestimate my powe- **dies**"
  elif thing == "secks":
    ans = "eww!"
  else:
    ans = "probeer iets anders."
  await ctx.channel.send(ans)
@bot.command()
async def spel(ctx):
  await ctx.channel.send(r"https://bbernyy-90.itch.io/fish")
@bot.command()
async def loop(ctx):
  global loopbool
  log(ctx, "loopbooled")
  loopbool = True
  await ctx.channel.send(r"ok")
@bot.command()
async def encrypt(ctx, key, title, *msg):
  msg = TSS(msg)
  if "http" in msg:
    f = requests.get(msg, allow_redirects=True)
    open("temp.bin", "wb").write(f.content)
    msg = open("temp.bin", "r").read()
  log(ctx, "encrypted " + msg)
  code = bc.encode(msg, key)
  with open("temp.bin", "wb") as f:
    f.write(code)
  await ctx.channel.send("hier is het bericht:", file=discord.File("temp.bin"))
@bot.command()
async def decrypt(ctx, key, url):
  log(ctx, "decrypted")
  f = requests.get(url, allow_redirects=True)
  fileee = open("temp.bin", "wb")
  fileee.write(f.content)
  fileee.close()
  await ctx.channel.send(bc.decode(key, "temp.bin"))
@bot.command()
async def getKey(ctx):
  log(ctx, "made key")
  chanel = await ctx.author.create_dm()
  await chanel.send("\"" + bc.generateKey(False) + "\"")
# connect token
bot.run(os.getenv("TOKEN"))
