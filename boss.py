from settings import *
from entities import *
Weapon_types_list=Weapon_types_list+('Excalibolg',)
class Boss(Mob):
    def __init__(self,num):
        if(num==1):
            self.leader=10
            self.hp=30
            self.str=10
            self.dex=6
            self.int=10
            self.AC=10
            self.bp=0
            self.fp=0
            self.aware=0
            self.type=5
            self.shout=100
            self.icon=Boss_icon
            self.name='World Ender'
            self.inventory=[]
            self.wear=Armor(3,Armor_icon,'leather armor',2)
            self.wield=Weapon(5,0,3,Weapon_icon,'Excalibolg',3,3,3,3)
            self.DV=1
            self.shield=self.wield
            self.ER=self.shield.ER+self.wear.ER
            self.MR=self.shield.MR
            self.lvl=99
            self.mp=(self.int*self.wield.intm*ER_divide)//(ER_divide+self.ER)
            self.VIT=self.hp
            self.BAC=self.AC-self.wear.AC-self.shield.AC
            self.xp=5000
            self.drop=[Weapon(5,0,3,Weapon_icon,'Excalibolg',3,3,3,3)]
            self.doping=[]
        elif(num==2):
            self.leader=0
            self.hp=20
            self.str=12
            self.dex=30
            self.int=6
            self.AC=8
            self.bp=0
            self.fp=0
            self.aware=0
            self.type=0
            self.shout=1
            self.icon=Boss_icon
            self.name='Midorime'
            self.inventory=[]
            self.wear=Armor(3,Armor_icon,'leather armor',2)
            self.wield=Weapon(1,6,0,Weapon_icon,'Satosame',1,0,0,0,['death'])
            self.DV=1
            self.shield=Weapon(0,0,0,Shield_icon,'',2)
            self.ER=self.wear.ER
            self.MR=0
            self.lvl=99
            self.mp=(self.int*self.wield.intm*ER_divide)//(ER_divide+self.ER)
            self.VIT=self.hp
            self.BAC=self.AC-self.wear.AC-self.shield.AC
            self.xp=50000
            self.drop=[Weapon(5,0,5,Weapon_icon,'Satosame',3,6,6,6)]
            self.doping=['stealth','death']
