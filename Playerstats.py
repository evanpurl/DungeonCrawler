import os
import sys

dirr = sys.path[0]


class Player:
    def __init__(self, memberid, charactername):

        self.charactername = charactername
        self.health = 0
        self.level = 0
        self.maxhealth = 0
        self.xp = 0
        self.mana = 0
        self.maxmana = 100
        self.name = None
        self.damage = 0
        self.defmode = None
        self.defense = 0
        self.weapon = None
        self.shield = None
        self.armor = None
        self.memberid = memberid
        self.itemlist = None
        self.inv = None

    def gethealth(self):
        if os.path.exists(f"{dirr}/Players/{self.memberid}/{self.charactername}/health.txt"):
            with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/health.txt", "r") as health:
                h = health.readline()
                self.health = int(h)
            return self.health
        else:
            with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/health.txt", "w+") as health:
                self.health = 100
                health.write(str(100))
                health.close()
            return self.health

    def sethealth(self, health):
        self.health += int(health)
        return self.health

    def getmana(self):
        if os.path.exists(f"{dirr}/Players/{self.memberid}/{self.charactername}/mana.txt"):
            with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/mana.txt", "r") as mana:
                h = mana.readline()
                self.mana = int(h)
                mana.close()
            return self.mana
        else:
            with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/mana.txt", "w+") as mana:
                self.mana = 100
                mana.write(str(100))
                mana.close()
            return self.mana

    def getname(self):
        with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/character.txt", "r") as name:
            self.name = name.readline()
        return self.name

    def getdamage(self):  # Updated 3/23/2022
        if os.path.exists(f"{dirr}/Players/{self.memberid}/{self.charactername}/damage.txt"):
            with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/damage.txt", "r") as damage:
                dam = float(damage.readline())
        else:
            with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/damage.txt", "w+") as damage:
                damage.write(str(5))
            dam = 5
        return dam

    def getweapondamage(self, item):
        if item != None:
            with open(f"{dirr}/globals/items/{item}.txt", "r") as weapon:
                lines = weapon.readlines()
                damageline = [i for i in lines if "damage" in i]
                if damageline:
                    defe = float(damageline[0].split()[1])
            return defe
        else:
            return 0.0

    def getdefense(self):  # Updated 3/23/2022
        if os.path.exists(f"{dirr}/Players/{self.memberid}/{self.charactername}/defense.txt"):
            with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/defense.txt", "r") as defense:
                defe = float(defense.readline())
        else:
            with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/defense.txt", "w+") as defense:
                defense.write(str(4))
            defe = 4
        return defe

    def getshielddef(self, shield):
        if shield is not None:
            with open(f"{dirr}/globals/items/{shield}.txt", "r") as shield:
                lines = shield.readlines()
                defenseline = [i for i in lines if "defense" in i]
                if defenseline:
                    defe = float(defenseline[0].split()[1])
            return defe
        else:
            return 0.0

    def getarmordef(self, armor):
        if armor != None:
            with open(f"{dirr}/globals/items/{armor}.txt", "r") as armorr:
                lines = armorr.readlines()
                defenseline = [i for i in lines if "defense" in i]
                if defenseline:
                    defe = float(defenseline[0].split()[1])
            return defe
        else:
            return 0.0

    def getitems(self, itemtype):
        itemlist = []
        os.chdir(f"{dirr}/globals/items")
        items = os.listdir(f"{dirr}/Players/{self.memberid}/{self.charactername}/inventory")
        for a in items:
            with open(a, "r") as f:
                lines = f.readlines()
                types = [i for i in lines if itemtype in i]
                if types:
                    itemlist.append(a.replace(".txt", ""))
        self.itemlist = itemlist
        return self.itemlist

    def addtoinv(self, itemname):
        pitems = os.listdir(f"{dirr}/Players/{self.memberid}/{self.charactername}/inventory")
        if itemname + '.txt' in pitems:
            with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/inventory/{itemname}.txt",
                      "r") as f:
                lines = f.readlines()
                amount = [i for i in lines if 'quantity' in i]
            with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/inventory/{itemname}.txt",
                      "w") as f:
                f.write(f"quantity: {str(int(amount[0].split(' ')[1]) + 1)}")
        else:
            with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/inventory/{itemname}.txt", "w") as f:
                f.write(f"quantity: {str(1)}")

    def remfrominv(self, itemname):
        itemname = itemname.replace(' \n', '')
        with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/inventory/{itemname}.txt",
                  "r") as f:
            amount = f.readlines()
        with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/inventory/{itemname}.txt",
                  "w") as f:
            f.write(f"quantity: {str(int(amount[0].split(' ')[1]) - 1)}")
            if len(amount) > 1:
                f.write("\n" + amount[1])
        with open(f"{dirr}/Players/{self.memberid}/{self.charactername}/inventory/{itemname}.txt",
                  "r") as f:
            amount = f.readlines()
        if int(amount[0].split(" ")[1]) <= 0:
            os.remove(f"{dirr}/Players/{self.memberid}/{self.charactername}/inventory/{itemname}.txt")

    def totalinv(self):
        inv = []
        os.chdir(f"{dirr}/Players/{self.memberid}/{self.charactername}/inventory")
        items = os.listdir(os.getcwd())
        for a in items:
            with open(a, "r") as f:
                inv.append(f"{f.readline().split(' ')[1]} {a.replace('.txt', '')}")
        self.inv = inv
        return self.inv

    def getlevel(self):
        if not os.path.exists(f"{dirr}/Players/{str(self.memberid)}/{self.charactername}/level.txt"):
            with open(f"{dirr}/Players/{str(self.memberid)}/{self.charactername}/level.txt", "w+") as level:
                level.write(str(1))
                return 1
        else:
            with open(f"{dirr}/Players/{str(self.memberid)}/{self.charactername}/level.txt", "r") as level:
                l = level.readline()
                return l

    def getxp(self):
        if not os.path.exists(f"{dirr}/Players/{str(self.memberid)}/{self.charactername}/xp.txt"):
            with open(f"{dirr}/Players/{str(self.memberid)}/{self.charactername}/xp.txt", "w+") as level:
                level.write(str(0))
                return 0
        else:
            with open(f"{dirr}/Players/{str(self.memberid)}/{self.charactername}/xp.txt", "r") as level:
                l = level.readline()
                return l

    def setxp(self, xp):
        with open(f"{dirr}/Players/{str(self.memberid)}/{self.charactername}/xp.txt", "w+") as level:
            level.write(str(xp))

    def levelup(self):
        with open(f"{dirr}/Players/{str(self.memberid)}/{self.charactername}/level.txt", "r") as level:
            l = level.readline()
        with open(f"{dirr}/Players/{str(self.memberid)}/{self.charactername}/xp.txt", "w+") as xp:
            xp.write(str(0))
        with open(f"{dirr}/Players/{str(self.memberid)}/{self.charactername}/level.txt", "w+") as level:
            lev = str(int(l) + 1)
            level.write(lev)
        return lev

    def readwallet(self):
        with open(
                f"{dirr}/Players/{self.memberid}/{self.charactername}/wallet.txt",
                "r") as item:
            money = int(item.readline())

        return money

    def writewallet(self, change):
        with open(
                f"{dirr}/Players/{self.memberid}/{self.charactername}/wallet.txt",
                "r") as item:
            money = item.readline()

        with open(
                f"{dirr}/Players/{self.memberid}/{self.charactername}/wallet.txt",
                "w") as item:
            item.write(str(int(money) + int(change)))

        return str(int(money) + int(change))


class Enemy:
    def __init__(self, unitname):
        self.health = 0
        self.name = unitname
        self.damage = 0
        self.defense = 0
        self.defmode = None
        self.level = 0

    def getname(self):
        return self.name

    def islevelten(self, level):
        if self.level != 1:
            self.damage = self.setdamage((self.damage * 4)-self.damage)
            self.health = self.sethealth((self.health * 4)-self.health)
            self.defense = self.setdefense((self.defense * 4)-self.defense)
            self.level = 1

    def gethealth(self):
        with open(f"{dirr}/globals/enemies/{self.name}.txt", "r") as enemyh:
            lines = enemyh.readlines()
            for a in lines:
                if "health" in a:
                    self.health = int(a.split(" ")[1])
        return self.health

    def sethealth(self, healthh):
        self.health += int(healthh)
        return self.health
    def setdamage(self, healthh):
        self.damage += int(healthh)
        return self.damage
    def setdefense(self, healthh):
        self.defense += float(healthh)
        return self.defense

    def getdamage(self):
        with open(f"{dirr}/globals/enemies/{self.name}.txt", "r") as enemyd:
            lines = enemyd.readlines()
            for a in lines:
                if "damage" in a:
                    self.damage = float(a.split(" ")[1].replace("/n", ""))
        return self.damage

    def getdefense(self):
        with open(f"{dirr}/globals/enemies/{self.name}.txt", "r") as enemyd:
            lines = enemyd.readlines()
            for a in lines:
                if "defense" in a:
                    self.defense = float(a.split(" ")[1].replace("/n", ""))
        return self.defense
