import discord
from discord.ext import commands
from discord.ui import Button, View
import os
import sys
from directional import enterdungeon
from misc import readwallet, writewallet, getcharacter
from creators import createclass, createenemy, createdungeon, makecharacter
from shop import generateshop, purchaseitem

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
dirr = sys.path[0]


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    print(f"Py-Cord version: {discord.__version__}")
    await bot.change_presence(activity=discord.Game('Powered by NLS: https://www.nitelifesoftware.com'))
    try:
        print("Starting Shop")
        await generateshop()
    except:
        print("There was an issue starting the shop")
    finally:
        print("Initial shop generation has completed!")


testing = [904120920862519396]
Support = [904120920862519396]


@bot.slash_command(guild_ids=Support, description="Command to buy items from the shop.")
async def shop(ctx):
    character = getcharacter(str(ctx.user.id))
    with open(f"{dirr}/Players/{str(ctx.user.id)}/{character}/wallet.txt", "r") as mon:
        money = int(mon.readline())
    shopitems = os.listdir(f"{dirr}/globals/shop")
    # Same code as the character selection code goes here.


@bot.slash_command(guild_ids=Support, description="Admin command to create Items.")
async def itemcreator(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Design Lead")
    if role in ctx.user.roles:
        itemname = ""
        itemvalue = ""
        itemtype = ""

        def is_auth(m):
            return m.author == ctx.author

        resname = Button(label="Item name", style=discord.ButtonStyle.primary)
        value = Button(label="Item value", style=discord.ButtonStyle.primary)
        category = Button(label="Type", style=discord.ButtonStyle.primary)
        write = Button(label="Finish", style=discord.ButtonStyle.green)
        view = View()
        view.add_item(resname)
        view.add_item(value)
        view.add_item(category)
        view.add_item(write)
        await ctx.respond("Welcome to the Item creator.", view=view)

        async def resourcenamecallback(interaction):
            nonlocal itemname
            if interaction.user == ctx.author:
                await interaction.response.edit_message(view=None)
                await interaction.followup.send("Type the name of the Item.")
                rname = await bot.wait_for('message', check=is_auth, timeout=300)
                itemname = f"{rname.content}"
                await interaction.followup.send(f"Your Item's name is {itemname}", view=view)

        async def valuecallback(interaction):
            nonlocal itemvalue
            if interaction.user == ctx.author:
                await interaction.response.edit_message(view=None)
                await interaction.followup.send("Type the value of one of this Item.")
                rval = await bot.wait_for('message', check=is_auth, timeout=300)
                itemvalue = f"Value: {rval.content}"
                await interaction.followup.send(f"Your Item's value is {itemvalue}", view=view)

        async def categorycallback(interaction):
            nonlocal itemtype
            if interaction.user == ctx.author:
                await interaction.response.edit_message(view=None)
                await interaction.followup.send(
                    "Enter the type you want this item to have. ie weapon, shield, armor, or none")
                cate = await bot.wait_for('message', check=is_auth, timeout=300)
                itemtype = f"type: {cate.content}"
                await interaction.followup.send(f"Your Item's type(s) is {itemtype}", view=view)

        async def writecallback(interaction):
            nonlocal itemname
            nonlocal itemvalue
            nonlocal itemtype
            if interaction.user == ctx.author:
                await interaction.response.edit_message(view=None)
                if os.path.exists(f"{dirr}/globals/items"):
                    os.chdir(f"{dirr}/globals/items")
                    try:
                        f = open(f"{itemname}.txt", 'w+')
                        f.write(f"{itemvalue} \n")
                        f.write(f"{itemtype} \n")
                        await interaction.followup.send(f"Is this item craftable? (y/n)")
                        iscraftable = await bot.wait_for('message', check=is_auth, timeout=300)
                        if iscraftable.content == "y":
                            await interaction.followup.send(f"What is the recipe? (Cloth,Iron,Stone) < Must match the "
                                                            f"case of the resource, Usually uppercase as shown.")
                            recipe = await bot.wait_for('message', check=is_auth, timeout=300)
                            recipe = recipe.content.replace(" ", "").lower()
                            recipe = "recipe: " + recipe
                            f.write(f"{recipe} \n")
                        if "weapon" in itemtype:
                            await interaction.followup.send(
                                f"How much damage will this item do? (this is a multiplier, usually over 1.0)")
                            dam = await bot.wait_for('message', check=is_auth, timeout=300)
                            damage = str(dam.content)
                            damage = "damage: " + damage
                            f.write(f"{damage}")
                            await interaction.followup.send(
                                f"Does this weapon have any special damage types? (poison, fire, freezing, explosive)")
                            eff = await bot.wait_for('message', check=is_auth, timeout=300)
                            effect = str(eff.content)
                            effect = "effect: " + effect
                            f.write(f"{effect}")
                        if "shield" in itemtype:
                            await interaction.followup.send(
                                f"How much defense does this item have? (this is a multiplier, usually over 1.0)")
                            defe = await bot.wait_for('message', check=is_auth, timeout=300)
                            defense = str(defe.content)
                            defense = "defense: " + defense
                            f.write(f"{defense}")
                        if "armor" in itemtype:
                            await interaction.followup.send(
                                f"How much defense does this item have? (this is a multiplier, usually over 1.0)")
                            defe = await bot.wait_for('message', check=is_auth, timeout=300)
                            defense = str(defe.content)
                            defense = "defense: " + defense
                            f.write(f"{defense}")

                        f.close()
                        await interaction.followup.send(
                            f"Item {itemname} has been created!")
                    except:
                        await interaction.response.edit_message(view=None)
                        await interaction.followup.send(
                            f"Something went wrong creating the item {itemname}.")

        resname.callback = resourcenamecallback
        value.callback = valuecallback
        write.callback = writecallback
        category.callback = categorycallback
    else:
        await ctx.respond(
            "You do not have the required permissions to run this command. Role needed: **Design Lead**")


@bot.slash_command(description="Command to display player data.")
async def player(ctx):
    if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/character.txt"):
        charactername = getcharacter(str(ctx.user.id))
        servstats = []
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/class.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/class.txt", "r") as clas:
                servstats.append(f"Class: {clas.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/damage.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/damage.txt", "r") as damage:
                servstats.append(f"Damage: {damage.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/defense.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/defense.txt", "r") as defense:
                servstats.append(f"Defense: {defense.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/health.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/health.txt", "r") as health:
                servstats.append(f"Health: {health.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/level.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/level.txt", "r") as level:
                servstats.append(f"Level: {level.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/mana.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/mana.txt", "r") as mana:
                servstats.append(f"Mana: {mana.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/xp.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/xp.txt", "r") as xp:
                servstats.append(f"XP: {xp.readline()}")
        await ctx.respond(f"**Player information for {charactername}:** \n \n" + "\n".join(servstats))
    else:
        makecharacter(ctx, "default")
        servstats = []
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/class.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/class.txt", "r") as clas:
                servstats.append(f"Class: {clas.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/damage.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/damage.txt", "r") as damage:
                servstats.append(f"Damage: {damage.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/defense.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/defense.txt", "r") as defense:
                servstats.append(f"Defense: {defense.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/health.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/health.txt", "r") as health:
                servstats.append(f"Health: {health.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/level.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/level.txt", "r") as level:
                servstats.append(f"Level: {level.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/mana.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/mana.txt", "r") as mana:
                servstats.append(f"Mana: {mana.readline()}")
        if os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/xp.txt"):
            with open(f"{dirr}/Players/{str(ctx.user.id)}/{'default'}/xp.txt", "r") as xp:
                servstats.append(f"XP: {xp.readline()}")
        await ctx.respond(f"**Player information for {'default'}:** \n \n" + "\n".join(servstats))


@bot.slash_command(guild_ids=Support, description="Dungeon Crawler start command.")
async def dc(ctx):
    if not os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}"):
        charactername = "default"
        os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}")
        os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}")
        os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}/{charactername}/inventory")
        makecharacter(ctx, charactername)
    else:
        charactername = getcharacter(ctx.user.id)
        makecharacter(ctx, charactername)

    await enterdungeon(ctx, bot, ctx.author, ctx.user.id, charactername)


@bot.slash_command(guild_ids=Support, description="Command to set your current character.")
async def setcharacter(ctx):
    def is_auth(m):
        return m.author == ctx.author

    await ctx.respond("Character set tool started.")
    isfolder = []
    if not os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}"):
        os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}")
        makecharacter(ctx, "default")
        characters = os.listdir(f"{dirr}/Players/{str(ctx.user.id)}")
    else:
        characters = os.listdir(f"{dirr}/Players/{str(ctx.user.id)}")
    for a in characters:
        if not a.endswith(".txt"):
            isfolder.append(a)
    unn = []
    num = []
    if len(isfolder) != 0:
        for a, b in enumerate(isfolder):
            unn.append(f"{a + 1}. {b}")
            num.append(f"{a + 1}")
        await ctx.send(f"**{ctx.user.name}'s Characters:** \n" + '\n'.join(unn))
        await ctx.send(f"Please select the character you want to choose.")
        unitmsg = await bot.wait_for('message', check=is_auth, timeout=300)
        if not unitmsg.content.isdigit():
            await ctx.respond(f"{unitmsg.content} is not a valid entry, please re-run the command to try again.")
        else:
            try:
                ind = num.index(unitmsg.content)
                with open(f"{dirr}/Players/{str(ctx.user.id)}/character.txt", "w+") as character:
                    character.write(isfolder[ind])
                await ctx.send("Character set!")
            except:
                await ctx.respond(f"{unitmsg.content} is not a valid choice, please re-run the command to try again.")


@bot.slash_command(guild_ids=Support, description="Command to create new character.")
async def createcharacter(ctx):
    def is_auth(m):
        return m.author == ctx.author

    await ctx.respond("What do you want the character's name to be?")
    character = await bot.wait_for('message', check=is_auth, timeout=300)
    if not os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}"):
        os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}")
    os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}/{character.content}")
    os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}/{character.content}/inventory")
    try:
        makecharacter(ctx, character.content)
        await ctx.respond("Character created!")
    except:
        await ctx.respond("Character not created!")


@bot.slash_command(guild_ids=Support)
async def classcreator(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Design Lead")
    if role in ctx.user.roles:
        await createclass(ctx, bot)
    else:
        await ctx.respond("You do not have the required permissions to run this command. Role needed: **Design Lead**")


@bot.slash_command(guild_ids=Support)
async def enemycreator(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Design Lead")
    if role in ctx.user.roles:
        await createenemy(ctx, bot)
    else:
        await ctx.respond("You do not have the required permissions to run this command. Role needed: **Design Lead**")


@bot.slash_command(guild_ids=Support)
async def dungeoncreator(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Design Lead")
    if role in ctx.user.roles:
        await createdungeon(ctx, bot)
    else:
        await ctx.respond("You do not have the required permissions to run this command. Role needed: **Design Lead**")


bot.run("OTM3NTQ2NTI3NDY1OTYzNTkw.YfdUPg.EIaW-h0t1qDZLr0nDgJgwJbXRa0")
