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
        self.wield=Weapon(4,0,4,Weapon_icon,'Excalibolg')
        self.lvl=99
        self.mp=(self.int*self.wield.intm*ER_divide)//(ER_divide+self.wear.ER)
        self.VIT=self.hp
        self.xp=xp_fun(self)*10
        self.drop=Weapon(4,0,4,Weapon_icon,'Excalibolg')
