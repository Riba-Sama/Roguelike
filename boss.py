from rog import Mob,Armor,Weapon
from settings import *
class Boss(Mob):
    def __init__(self):
        self.hp=200
        self.str=40
        self.dex=20
        self.int=40
        self.AC=12
        self.bp=0
        self.fp=0
        self.aware=0
        self.type=5
        self.icon=Boss_icon
        self.name='World Ender'
        self.inventory=[]
        self.wear=Armor(5,Armor_icon,'white dragonscalemail',-1)
        self.wield=Weapon(4,2,4,Weapon_icon,'Excalibolg')
        self.lvl=99
        self.mp=(self.int*self.wield.intm*ER_divide)//(ER_divide+self.wear.ER)
        self.VIT=self.hp
        self.xp=xp_fun(self)*ab[11]
