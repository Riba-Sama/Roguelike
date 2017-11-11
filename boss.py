from settings import Boss_icon,Armor_icon,Weapon_icon,ER_divide,xp_fun
from entities import Armor,Weapon,Mob
class Boss(Mob):
    def __init__(self):
        self.hp=100
        self.str=30
        self.dex=20
        self.int=30
        self.AC=12
        self.bp=0
        self.fp=0
        self.aware=0
        self.type=5
        self.icon=Boss_icon
        self.name='World Ender'
        self.inventory=[]
        self.wear=Armor(3,Armor_icon,'leather',2)
        self.wield=Weapon(5,0,5,Weapon_icon,'Excalibolg',3,6,6,6)
        self.shield=self.wield
        self.ER=self.wield.ER+self.wear.ER
        self.MR=self.wield.MR
        self.lvl=99
        self.mp=(self.int*self.wield.intm*ER_divide)//(ER_divide+self.ER)
        self.VIT=self.hp
        self.xp=xp_fun(self)*10
        self.drop=[Weapon((5,6),(0,6),(5,6),Weapon_icon,'Excalibolg',3)]
