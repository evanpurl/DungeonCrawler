import os
import sys
import discord
from discord.ui import Button, View

dirr = sys.path[0]


def makecharacter(ctx, name):
    if not os.path.exists(f"{dirr}/Players/{str(ctx.user.id)}/{name}"):
        os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}/{name}")
        os.mkdir(f"{dirr}/Players/{str(ctx.user.id)}/{name}/inventory")
    with open(f"{dirr}/Players/{str(ctx.user.id)}/character.txt", "w+") as character:
        character.write(name)
    with open(f"{dirr}/Players/{str(ctx.user.id)}/{name}/wallet.txt", "w+") as wallet:
        wallet.write(str(250))
    with open(f"{dirr}/Players/{str(ctx.user.id)}/{name}/damage.txt", "w+") as damage:
        damage.write(str(5))
    with open(f"{dirr}/Players/{str(ctx.user.id)}/{name}/defense.txt", "w+") as defense:
        defense.write(str(4))
    with open(f"{dirr}/Players/{str(ctx.user.id)}/{name}/health.txt", "w+") as health:
        health.write(str(100))
    with open(f"{dirr}/Players/{str(ctx.user.id)}/{name}/level.txt", "w+") as level:
        level.write(str(1))
    with open(f"{dirr}/Players/{str(ctx.user.id)}/{name}/mana.txt", "w+") as mana:
        mana.write(str(100))
    with open(f"{dirr}/Players/{str(ctx.user.id)}/{name}/xp.txt", "w+") as xp:
        xp.write(str(0))


async def createclass(ctx, bot):
    def is_auth(m):
        return m.author == ctx.author

    classname = Button(label="Class Name", style=discord.ButtonStyle.primary)

    clasname = View()
    clasname.add_item(classname)

    await ctx.respond("Welcome to the class creator! You will be asked a series of questions to create your class.",
                      view=clasname)

    async def classnamecallback(interaction):
        c = []
        await interaction.response.edit_message(view=None)
        await ctx.respond("What is the class' name?")

        cname = await bot.wait_for('message', check=is_auth, timeout=300)
        cname = cname.content

        await ctx.respond(f"The name you chose is {cname}")
        await ctx.respond("Does this class boost the player's health?")
        hyorn = await bot.wait_for('message', check=is_auth, timeout=300)
        if hyorn.content.lower() == "y":
            await ctx.respond("How much would the player's health increase by?")
            health = await bot.wait_for('message', check=is_auth, timeout=300)
            health = health.content
            c.append(f'health: {health}')
        await ctx.respond("Does this class boost the player's damage?")
        dyorn = await bot.wait_for('message', check=is_auth, timeout=300)
        if dyorn.content.lower() == "y":
            await ctx.respond("How much would the player's damage increase by?")
            damage = await bot.wait_for('message', check=is_auth, timeout=300)
            damage = damage.content
            c.append(f'damage: {damage}')
        await ctx.respond("Does this class boost the player's defense?")
        deyorn = await bot.wait_for('message', check=is_auth, timeout=300)
        if deyorn.content.lower() == "y":
            await ctx.respond("How much would the player's defense increase by?")
            defense = await bot.wait_for('message', check=is_auth, timeout=300)
            defense = defense.content
            c.append(f'defense: {defense}')
        if not os.path.exists(f"{dirr}/globals/classes/"):
            os.mkdir(f"{dirr}/globals/classes/")
        with open(f"{dirr}/globals/classes/{cname}.txt", "w+") as cl:
            for a in c:
                cl.write(a + '\n')

        await ctx.respond(f"Class with the name {cname} has been created!")

    classname.callback = classnamecallback


async def createenemy(ctx, bot):
    dirr = sys.path[0]

    def is_auth(m):
        return m.author == ctx.author

    ename = Button(label="Enemy Name", style=discord.ButtonStyle.primary)

    enemy = View()
    enemy.add_item(ename)

    await ctx.respond("Welcome to the enemy creator! Follow the prompt to create your enemy.",
                      view=enemy)

    async def enemynamecallback(interaction):
        c = []
        await interaction.response.edit_message(view=None)
        await ctx.respond("What is the enemy's name?")

        cname = await bot.wait_for('message', check=is_auth, timeout=300)
        cname = cname.content

        await ctx.respond(f"The name you chose is {cname}")
        await ctx.respond("How much health does this enemy have?")
        health = await bot.wait_for('message', check=is_auth, timeout=300)
        health = health.content
        c.append(f'health: {health}')
        await ctx.respond(f'health: {health}')
        await ctx.respond("How much damage would this enemy do?")
        damage = await bot.wait_for('message', check=is_auth, timeout=300)
        damage = damage.content
        c.append(f'damage: {damage}')
        await ctx.respond(f'damage: {damage}')
        await ctx.respond("How much defense does this enemy have?")
        defense = await bot.wait_for('message', check=is_auth, timeout=300)
        defense = defense.content
        c.append(f'defense: {defense}')
        await ctx.respond(f'defense: {defense}')
        if not os.path.exists(f"{dirr}/globals/enemies/"):
            os.mkdir(f"{dirr}/globals/enemies/")
        with open(f"{dirr}/globals/enemies/{cname}.txt", "w+") as cl:
            for a in c:
                cl.write(a + '\n')

        await ctx.respond(f"Enemy with the name {cname} has been created!")

    ename.callback = enemynamecallback


async def createdungeon(ctx, bot):
    dirr = sys.path[0]

    def is_auth(m):
        return m.author == ctx.author

    dname = Button(label="Dungeon Name", style=discord.ButtonStyle.primary)

    enemy = View()
    enemy.add_item(dname)

    await ctx.respond("Welcome to the dungeon creator! Follow the prompt to create your dungeon.",
                      view=enemy)

    async def dungeonnamecallback(interaction):
        c = []
        await interaction.response.edit_message(view=None)
        await ctx.respond("What is this dungeon called?")

        cname = await bot.wait_for('message', check=is_auth, timeout=300)
        cname = cname.content

        await ctx.respond(f"The name you chose is {cname}")
        await ctx.respond("What light level does this dungeon have?")
        health = await bot.wait_for('message', check=is_auth, timeout=300)
        health = health.content
        c.append(f'll: {health}')
        await ctx.respond(f'Light Level: {health}')
        await ctx.respond(
            "What enemies are present in this dungeon? Separate each by commas. ie snake,skeleton,skeleton archer")
        damage = await bot.wait_for('message', check=is_auth, timeout=300)
        damage = damage.content.replace(" ,", ",").replace(", ", ",")
        c.append(f'enemies: {damage}')
        await ctx.respond(f'enemies: {damage}')
        await ctx.respond("What boss is in this dungeon? Check discord for boss list.")
        damage = await bot.wait_for('message', check=is_auth, timeout=300)
        await ctx.respond(f"Boss: {damage.content}")
        c.append(f"boss: {damage.content}")
        if not os.path.exists(f"{dirr}/globals/dungeons/"):
            os.mkdir(f"{dirr}/globals/dungeons/")
        with open(f"{dirr}/globals/dungeons/{cname}.txt", "w+") as cl:
            for a in c:
                cl.write(a + '\n')

        await ctx.respond(f"Dungeon with the name {cname} has been created!")

    dname.callback = dungeonnamecallback


def quickdungeon(stats):
    name = stats[0]
    light = stats[1]
    enemies = stats[2]
    boss = stats[3]

    with open(f"{dirr}/globals/dungeons/{name}.txt", "w+") as cl:
        cl.write(f"ll: {str(light)} \n")
        cl.write(f"enemies: {enemies.replace(', ', ',')} \n")
        cl.write(f"boss: {boss}")


def quickenemy(stats):
    name = stats[0]
    health = stats[1]
    damage = stats[2]
    defense = stats[3]

    with open(f"{dirr}/globals/enemies/{name}.txt", "w+") as cl:
        cl.write(f"health: {str(health)} \n")
        cl.write(f"damage: {str(damage)} \n")
        cl.write(f"defense: {str(defense)}")


def quickclass(stats):
    name = stats[0]
    health = stats[1]
    damage = stats[2]
    defense = stats[3]

    with open(f"{dirr}/globals/classes/{name}.txt", "w+") as cl:
        cl.write(f"health: {str(health)} \n")
        cl.write(f"damage: {str(damage)} \n")
        cl.write(f"defense: {str(defense)}")


def quickitem(stats):
    name = stats[0]
    value = stats[1]

    with open(f"{dirr}/globals/items/{name}.txt", "w+") as cl:
        cl.write(f"Value: {str(value)} \n")
        if stats[2] == "weapon":
            cl.write(f"type: weapon \n")
            cl.write(f"damage: {str(stats[3])}")
        if stats[2] == "shield":
            cl.write(f"type: shield \n")
            cl.write(f"defense: {str(stats[3])}")
        if stats[2] == "armor":
            cl.write(f"type: armor \n")
            cl.write(f"defense: {str(stats[3])}")
        if stats[2] == "loot":
            cl.write(f"type: loot \n")
