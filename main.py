import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from discord.ui import Button, View
from cogs import economy
import os
import csv
from directional import enterdungeon
from misc import getcharacter, getvalue
from creators import createclass, createenemy, createdungeon, makecharacter, quickdungeon, quickenemy, quickclass, quickitem
from shop import generateshop
from Playerstats import Player

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)


@client.event
async def on_ready():
    await client.wait_until_ready()
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name=f"Powered by Nite Life Software"))

async def whohasaccess():
    try:
        with open("util/access.txt") as access:
            data = access.read()
            datalist = data.split("\n")
        return datalist
    except:
        print("error getting access ids.")
@client.command(name="reloadcogs", description="command to reload cogs")
async def reload(ctx) -> None:
    if str(ctx.message.author.id) in await whohasaccess():
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await ctx.send(f"reloading cog: {filename[:-3]}")
                await client.reload_extension(f"cogs.{filename[:-3]}")
        await ctx.send(f"Syncing commands")
        await client.tree.sync()
        await ctx.send(f"Commands synced")
    else:
        await ctx.send(f"You can't run this command.")
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            print(f"Loading cog: {filename[:-3]}")
            await client.load_extension(f"cogs.{filename[:-3]}")

# Main function to load extensions and then load bot.
async def main():
    async with client:
        try:
            with open('token/token.txt', 'r') as token:
                token = token.read()
            await load_extensions()
            await client.start(token)
        except KeyboardInterrupt:
            pass
asyncio.run(main())

# @bot.slash_command(guild_ids=Support, description="Command to sell items.")
# async def sell(ctx):
#     await ctx.respond("Selling module opened.")
#     if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/character.txt"):
#         player = Player(str(ctx.user.id), getcharacter(str(ctx.user.id)))
#     else:
#         makecharacter(ctx, "default")
#         player = Player(str(ctx.user.id), getcharacter(str(ctx.user.id)))
#
#     def is_auth(m):
#         return m.author == ctx.author
#
#     character = getcharacter(str(ctx.user.id))
#     items = os.listdir(f"{dirr}/Players/{str(ctx.user.id)}/{character}/inventory")
#     unn = []
#     num = []
#     if len(items) != 0:
#         for a, b in enumerate(items):
#             unn.append(f"{a + 1}. {b.replace('.txt', '')}")
#             num.append(f"{a + 1}")
#         await ctx.send(f"** {getcharacter(str(ctx.user.id))} Items:** \n" + '\n'.join(unn))
#         await ctx.send(f"Please select the item you want to sell. Type 0 to end this command.")
#         unitmsg = await bot.wait_for('message', check=is_auth, timeout=300)
#         if not unitmsg.content.isdigit():
#             await ctx.respond(f"{unitmsg.content} is not a valid entry, please re-run the command to try again.")
#         else:
#             try:
#                 if int(unitmsg.content) == 0:
#                     await ctx.send("Command ended.")
#                 else:
#                     ind = num.index(unitmsg.content)
#                     itemval = getvalue(items[ind].replace(".txt", ""))
#                     player.writewallet(itemval / 2)
#                     player.remfrominv(items[ind].replace(".txt", ""))
#                     await ctx.send(f"{items[ind].replace('.txt', '')} has been sold! Money gained: {itemval / 2}")
#             except:
#                 await ctx.respond(
#                     f"{unitmsg.content} is not a valid choice, please re-run the command to try again.")
#     else:
#         await ctx.respond("No items available to sell.")


# @bot.slash_command(guild_ids=Support, description="Command to buy items from the shop.")
# async def shop(ctx):
#     await ctx.respond("Shop has been opened.")
#     if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/character.txt"):
#         player = Player(str(ctx.user.id), getcharacter(str(ctx.user.id)))
#     else:
#         makecharacter(ctx, "default")
#         player = Player(str(ctx.user.id), getcharacter(str(ctx.user.id)))
#
#     def is_auth(m):
#         return m.author == ctx.author
#
#     character = getcharacter(str(ctx.user.id))
#     with open(f"{dirr}/Players/{str(ctx.user.id)}/{character}/wallet.txt", "r") as mon:
#         money = int(mon.readline())
#     shopitems = os.listdir(f"{dirr}/globals/shop")
#     unn = []
#     num = []
#     if len(shopitems) != 0:
#         for a, b in enumerate(shopitems):
#             unn.append(f"{a + 1}. {b}")
#             num.append(f"{a + 1}")
#         await ctx.send(f"**Shop Items:** \n" + '\n'.join(unn))
#         await ctx.send(f"Please select the item you want to purchase. Type 0 to close the shop.")
#         unitmsg = await bot.wait_for('message', check=is_auth, timeout=300)
#         if not unitmsg.content.isdigit():
#             await ctx.respond(f"{unitmsg.content} is not a valid entry, please re-run the command to try again.")
#         else:
#             try:
#                 if int(unitmsg.content) == 0:
#                     await ctx.send("Shop closed, command ended.")
#                 else:
#                     ind = num.index(unitmsg.content)
#                     if player.readwallet() - getvalue(shopitems[ind].replace(".txt", "")) >= 0:
#                         player.addtoinv(shopitems[ind].replace(".txt", ""))
#                         player.writewallet(-getvalue(shopitems[ind].replace(".txt", "")))
#                         await ctx.send(f"Item {shopitems[ind].replace('.txt', '')} has been purchased!")
#                         await generateshop()
#                     else:
#                         await ctx.send("You cannot afford that item.")
#             except IndexError as e:
#                 await ctx.respond(f"{unitmsg.content} is not a valid choice, please re-run the command to try again.")
#
#
# @bot.slash_command(guild_ids=Support, description="Admin command to create Items.")
# async def createitem(ctx):
#     role = discord.utils.get(ctx.guild.roles, name="Design Lead")
#     if role in ctx.user.roles:
#         itemname = ""
#         itemvalue = ""
#         itemtype = ""
#
#         def is_auth(m):
#             return m.author == ctx.author
#
#         resname = Button(label="Item name", style=discord.ButtonStyle.primary)
#         value = Button(label="Item value", style=discord.ButtonStyle.primary)
#         category = Button(label="Type", style=discord.ButtonStyle.primary)
#         write = Button(label="Finish", style=discord.ButtonStyle.green)
#         view = View()
#         view.add_item(resname)
#         view.add_item(value)
#         view.add_item(category)
#         view.add_item(write)
#         await ctx.respond("Welcome to the Item creator.", view=view)
#
#         async def resourcenamecallback(interaction):
#             nonlocal itemname
#             if interaction.user == ctx.author:
#                 await interaction.response.edit_message(view=None)
#                 await interaction.followup.send("Type the name of the Item.")
#                 rname = await bot.wait_for('message', check=is_auth, timeout=300)
#                 itemname = f"{rname.content}"
#                 await interaction.followup.send(f"Your Item's name is {itemname}", view=view)
#
#         async def valuecallback(interaction):
#             nonlocal itemvalue
#             if interaction.user == ctx.author:
#                 await interaction.response.edit_message(view=None)
#                 await interaction.followup.send("Type the value of one of this Item.")
#                 rval = await bot.wait_for('message', check=is_auth, timeout=300)
#                 itemvalue = f"Value: {rval.content}"
#                 await interaction.followup.send(f"Your Item's value is {itemvalue}", view=view)
#
#         async def categorycallback(interaction):
#             nonlocal itemtype
#             if interaction.user == ctx.author:
#                 await interaction.response.edit_message(view=None)
#                 await interaction.followup.send(
#                     "Enter the type you want this item to have. ie weapon, shield, armor, or none")
#                 cate = await bot.wait_for('message', check=is_auth, timeout=300)
#                 itemtype = f"type: {cate.content}"
#                 await interaction.followup.send(f"Your Item's type(s) is {itemtype}", view=view)
#
#         async def writecallback(interaction):
#             nonlocal itemname
#             nonlocal itemvalue
#             nonlocal itemtype
#             if interaction.user == ctx.author:
#                 await interaction.response.edit_message(view=None)
#                 if os.path.exists(f"{dirr}/globals/items"):
#                     os.chdir(f"{dirr}/globals/items")
#                     try:
#                         f = open(f"{itemname}.txt", 'w+')
#                         f.write(f"{itemvalue} \n")
#                         f.write(f"{itemtype} \n")
#                         if "weapon" in itemtype:
#                             await interaction.followup.send(
#                                 f"How much damage will this item do? (this is a multiplier, usually over 1.0)")
#                             dam = await bot.wait_for('message', check=is_auth, timeout=300)
#                             damage = str(dam.content)
#                             damage = "damage: " + damage
#                             f.write(f"{damage}")
#                         if "shield" in itemtype:
#                             await interaction.followup.send(
#                                 f"How much defense does this item have? (this is a multiplier, usually over 1.0)")
#                             defe = await bot.wait_for('message', check=is_auth, timeout=300)
#                             defense = str(defe.content)
#                             defense = "defense: " + defense
#                             f.write(f"{defense}")
#                         if "armor" in itemtype:
#                             await interaction.followup.send(
#                                 f"How much defense does this item have? (this is a multiplier, usually over 1.0)")
#                             defe = await bot.wait_for('message', check=is_auth, timeout=300)
#                             defense = str(defe.content)
#                             defense = "defense: " + defense
#                             f.write(f"{defense}")
#
#                         f.close()
#                         await interaction.followup.send(
#                             f"Item {itemname} has been created!")
#                         await generateshop()
#                     except:
#                         await interaction.response.edit_message(view=None)
#                         await interaction.followup.send(
#                             f"Something went wrong creating the item {itemname}.")
#
#         resname.callback = resourcenamecallback
#         value.callback = valuecallback
#         write.callback = writecallback
#         category.callback = categorycallback
#     else:
#         await ctx.respond(
#             "You do not have the required permissions to run this command. Role needed: **Design Lead**")
#
#
# @bot.slash_command(description="Command to display player data.")
# async def player(ctx):
#     if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/character.txt"):
#         charactername = getcharacter(str(ctx.user.id))
#         servstats = []
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/wallet.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/wallet.txt", "r") as money:
#                 servstats.append(f"Money: {money.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/class.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/class.txt", "r") as clas:
#                 servstats.append(f"Class: {clas.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/damage.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/damage.txt", "r") as damage:
#                 servstats.append(f"Damage: {damage.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/defense.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/defense.txt", "r") as defense:
#                 servstats.append(f"Defense: {defense.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/health.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/health.txt", "r") as health:
#                 servstats.append(f"Health: {health.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/level.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/level.txt", "r") as level:
#                 servstats.append(f"Level: {level.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/mana.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/mana.txt", "r") as mana:
#                 servstats.append(f"Mana: {mana.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/xp.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/xp.txt", "r") as xp:
#                 servstats.append(f"XP: {xp.readline()}")
#         await ctx.respond(f"**Player information for {charactername}:** \n \n" + "\n".join(servstats))
#     else:
#         makecharacter(ctx, "default")
#         servstats = []
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/class.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/class.txt", "r") as clas:
#                 servstats.append(f"Class: {clas.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/damage.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/damage.txt", "r") as damage:
#                 servstats.append(f"Damage: {damage.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/defense.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/defense.txt", "r") as defense:
#                 servstats.append(f"Defense: {defense.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/health.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/health.txt", "r") as health:
#                 servstats.append(f"Health: {health.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/level.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/level.txt", "r") as level:
#                 servstats.append(f"Level: {level.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/mana.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/mana.txt", "r") as mana:
#                 servstats.append(f"Mana: {mana.readline()}")
#         if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/xp.txt"):
#             with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/xp.txt", "r") as xp:
#                 servstats.append(f"XP: {xp.readline()}")
#         await ctx.respond(f"**Player information for {'default'}:** \n \n" + "\n".join(servstats))
#
#
# @bot.slash_command(guild_ids=Support, description="Dungeon Crawler start command.")
# async def dc(ctx):
#     if not os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}"):
#         charactername = "default"
#         os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}")
#         os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}")
#         os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/inventory")
#         makecharacter(ctx, charactername)
#     else:
#         charactername = getcharacter(ctx.user.id)
#         makecharacter(ctx, charactername)
#
#     await enterdungeon(ctx, bot, ctx.author, ctx.user.id, charactername)
#
#
# @bot.slash_command(guild_ids=Support, description="Command to set your current character.")
# async def setcharacter(ctx):
#     def is_auth(m):
#         return m.author == ctx.author
#
#     await ctx.respond("Character set tool started.")
#     isfolder = []
#     if not os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}"):
#         os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}")
#         makecharacter(ctx, "default")
#         characters = os.listdir(f"{dirr}/Players/{str(ctx.user.id)}")
#     else:
#         characters = os.listdir(f"{dirr}/Players/{str(ctx.user.id)}")
#     for a in characters:
#         if not a.endswith(".txt"):
#             isfolder.append(a)
#     unn = []
#     num = []
#     if len(isfolder) != 0:
#         for a, b in enumerate(isfolder):
#             unn.append(f"{a + 1}. {b}")
#             num.append(f"{a + 1}")
#         await ctx.send(f"**{ctx.user.name}'s Characters:** \n" + '\n'.join(unn))
#         await ctx.send(f"Please select the character you want to choose.")
#         unitmsg = await bot.wait_for('message', check=is_auth, timeout=300)
#         if not unitmsg.content.isdigit():
#             await ctx.respond(f"{unitmsg.content} is not a valid entry, please re-run the command to try again.")
#         else:
#             try:
#                 ind = num.index(unitmsg.content)
#                 with open(f"{dirr}/Players/{str(ctx.user.id)}/character.txt", "w+") as character:
#                     character.write(isfolder[ind])
#                 await ctx.send("Character set!")
#             except:
#                 await ctx.respond(f"{unitmsg.content} is not a valid choice, please re-run the command to try again.")
#
#
# @bot.slash_command(guild_ids=Support, description="Command to create new character.")
# async def createcharacter(ctx):
#     def is_auth(m):
#         return m.author == ctx.author
#
#     await ctx.respond("What do you want the character's name to be?")
#     character = await bot.wait_for('message', check=is_auth, timeout=300)
#     if not os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}"):
#         os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}")
#     os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}/{character.content}")
#     os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}/{character.content}/inventory")
#     try:
#         makecharacter(ctx, character.content)
#         await ctx.respond("Character created!")
#     except:
#         await ctx.respond("Character not created!")
#
#
# @bot.slash_command(guild_ids=Support)
# async def classcreator(ctx):
#     role = discord.utils.get(ctx.guild.roles, name="Design Lead")
#     if role in ctx.user.roles:
#         await createclass(ctx, bot)
#     else:
#         await ctx.respond("You do not have the required permissions to run this command. Role needed: **Design Lead**")
#
#
# @bot.slash_command(guild_ids=Support)
# async def enemycreator(ctx):
#     role = discord.utils.get(ctx.guild.roles, name="Design Lead")
#     if role in ctx.user.roles:
#         await createenemy(ctx, bot)
#     else:
#         await ctx.respond("You do not have the required permissions to run this command. Role needed: **Design Lead**")
#
#
# @bot.slash_command(guild_ids=Support)
# async def dungeoncreator(ctx):
#     role = discord.utils.get(ctx.guild.roles, name="Design Lead")
#     if role in ctx.user.roles:
#         await createdungeon(ctx, bot)
#     else:
#         await ctx.respond("You do not have the required permissions to run this command. Role needed: **Design Lead**")
#
#
# @bot.slash_command(guild_ids=Support)
# async def masscreate(ctx):
#     def is_auth(m):
#         return m.author == ctx.author
#
#     role = discord.utils.get(ctx.guild.roles, name="Design Lead")
#     if role in ctx.user.roles:
#         await ctx.respond("Which creator do you want to access? (dungeon, enemy, class or item.)")
#         choice = await bot.wait_for('message', check=is_auth, timeout=300)
#         if choice.content == "dungeon": # Dungeon Mode
#             await ctx.send("(Dungeon Mode) Please upload your file now, it should be in the format '.csv'")
#             file = await bot.wait_for('message', check=is_auth, timeout=300)
#             await file.attachments[0].save(fp=f"{dirr}/saved/dungeons.csv")
#             with open(f"{dirr}/saved/dungeons.csv", "r") as f:
#                 reader = csv.reader(f)
#                 next(reader)
#                 try:
#                     for row in reader:
#                         quickdungeon(row)
#                 except:
#                     await ctx.send("A problem occurred while creating your dungeons.")
#                 finally:
#                     await ctx.send("Dungeons have been created!")
#         elif choice.content == "enemy": # Enemy Mode
#             await ctx.send("(Enemy mode) Please upload your file now, it should be in the format '.csv'")
#             file = await bot.wait_for('message', check=is_auth, timeout=300)
#             await file.attachments[0].save(fp=f"{dirr}/saved/enemies.csv")
#             with open(f"{dirr}/saved/enemies.csv", "r") as f:
#                 reader = csv.reader(f)
#                 next(reader)
#                 try:
#                     for row in reader:
#                         quickenemy(row)
#                 except:
#                     await ctx.send("A problem occurred while creating your enemies.")
#                 finally:
#                     await ctx.send("Enemies have been created!")
#         elif choice.content == "class": # Class Mode
#             await ctx.send("(Class mode) Please upload your file now, it should be in the format '.csv'")
#             file = await bot.wait_for('message', check=is_auth, timeout=300)
#             await file.attachments[0].save(fp=f"{dirr}/saved/classes.csv")
#             with open(f"{dirr}/saved/classes.csv", "r") as f:
#                 reader = csv.reader(f)
#                 next(reader)
#                 try:
#                     for row in reader:
#                         quickclass(row)
#                 except:
#                     await ctx.send("A problem occurred while creating your classes.")
#                 finally:
#                     await ctx.send("Classes have been created!")
#         elif choice.content == "item":
#             await ctx.send("(Item mode) Please upload your file now, it should be in the format '.csv'")
#             file = await bot.wait_for('message', check=is_auth, timeout=300)
#             await file.attachments[0].save(fp=f"{dirr}/saved/items.csv")
#             with open(f"{dirr}/saved/items.csv", "r") as f:
#                 reader = csv.reader(f)
#                 next(reader)
#                 try:
#                     for row in reader:
#                         quickitem(row)
#                 except:
#                     await ctx.send("A problem occurred while creating your items.")
#                 finally:
#                     await ctx.send("Items have been created!")
#         else:
#             await ctx.respond("Your choice is not valid.")
#     else:
#         await ctx.respond("You do not have the required permissions to run this command. Role needed: **Design Lead**")

