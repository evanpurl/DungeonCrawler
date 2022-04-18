import os
import sys
import time
import random

dirr = sys.path[0]


async def generateshop():  # Generates shop on start
    was = []
    items = os.listdir(f"{dirr}/globals/items/")
    for a in items:
        with open(f"{dirr}/globals/items/{a}", "r") as pitem:
            lines = pitem.readlines()
            weapon = [i for i in lines if 'weapon' in i]
            shield = [i for i in lines if 'shield' in i]
            armor = [i for i in lines if 'armor' in i]
            if weapon:
                was.append(a.replace(".txt", ""))
            elif shield:
                was.append(a.replace(".txt", ""))
            elif armor:
                was.append(a.replace(".txt", ""))
            else:
                pass

    # Adds 5 random items to shop.
    itemchoices = []
    x = 0
    while x != 5:
        x += 1
        choice = random.randint(0, len(was) - 1)
        itemchoices.append(was[choice])

    if not os.path.exists(f"{dirr}/globals/shop"):
        os.mkdir(f"{dirr}/globals/shop")

    currentshop = os.listdir(f"{dirr}/globals/shop")
    if len(currentshop) != 0:
        for a in currentshop:
            os.remove(f"{dirr}/globals/shop/{a}")

    for a in itemchoices:
        with open(f"{dirr}/globals/shop/{a}", "w+") as itemchoices:
            print(f"{a.replace('.txt', '')} added to shop.")


async def purchaseitem(itemtorem, idx):  # When shop item is bought, remove that element and replace it.
    with open(f"{dirr}/globals/items/{itemtorem}.txt", "r") as item: # Move to main function.
        lines = item.readlines()
        val = [i for i in lines if 'Value' in i][0].split(": ")[1]


    was = []
    items = os.listdir(f"{dirr}/globals/items/")
    for a in items:
        with open(f"{dirr}/globals/items/{a}", "r") as pitem:
            lines = pitem.readlines()
            weapon = [i for i in lines if 'weapon' in i]
            shield = [i for i in lines if 'shield' in i]
            armor = [i for i in lines if 'armor' in i]
            if weapon:
                was.append(a.replace(".txt", ""))
            elif shield:
                was.append(a.replace(".txt", ""))
            elif armor:
                was.append(a.replace(".txt", ""))
            else:
                pass

    # Regens one item if it's in the correct position.
    choice = random.randint(0, len(was) - 1)

    currentshop = os.listdir(f"{dirr}/globals/shop")
    if currentshop[idx] == itemtorem+".txt":
        os.remove(f"{dirr}/globals/shop/{itemtorem}.txt")
        print(f"{itemtorem} has been purchased.")
        with open(f"{dirr}/globals/shop/{was[choice]}.txt", "w+") as itemchoices:
            print(f"{was[choice].replace('.txt', '')} added to shop.")


