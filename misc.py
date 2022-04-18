import os
import sys

dirr = sys.path[0]


def readwallet(memberid, character):
    with open(
            f"{dirr}/Players/{memberid}/{character}/wallet.txt",
            "r") as item:
        money = item.readline()

    return money


def writewallet(memberid, character, change):
    with open(
            f"{dirr}/Players/{memberid}/{character}/wallet.txt",
            "r") as item:
        money = item.readline()

    with open(
            f"{dirr}/Players/{memberid}/{character}/wallet.txt",
            "w") as item:
        item.write(str(int(money) + int(change)))

    return str(int(money) + int(change))


def getcharacter(userid):
    with open(f"{dirr}/Players/{str(userid)}/character.txt", "r") as m:
        character = m.readline()
    return character


def getvalue(itemname):
    with open(f"{dirr}/globals/items/{itemname}.txt", "r") as item:
        lines = item.readlines()
        value = [i for i in lines if 'Value' in i][0].split(": ")[1]
    return int(value)
