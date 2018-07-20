from settings import *
from random import randint as r
from math import ceil,floor,log
def d(nii):
    return r(nii>0,max(0,nii))
def rl(li):
    q=sum(li)
    t=d(q)
    n=0
    while(t>li[n]):
        t-=li[n]
        n+=1
    return n
def rlrange(n):
    return ceil((8*d(n*(n+1)//2)+1)**0.5/2.0-0.5)

class Entity:
    def __init__(self,name):
        self.name=name

class Item(Entity):
    def __init__(self,icon,number,name):
        self.icon=icon
        self.number=number
        self.name=name

class Weapon(Entity):
    def __init__(self,a,b,c,icon,name,dual=1,d=0,e=0,f=0,doping=[]):
        self.icon=icon
        self.name=name
        self.dual=dual
        if(dual==1):
            self.strm=a
            self.dexm=b
            self.intm=c
        elif(dual==2):
            self.AC=a
            self.ER=b
            self.MR=c
        elif(dual==3):
            self.strm=a
            self.dexm=b
            self.intm=c
            self.AC=d
            self.ER=e
            self.MR=f
        self.doping=doping

class Armor(Entity):
    def __init__(self,AC,icon,name,ER,doping=[]):
        self.AC=AC
        self.icon=icon
        self.name=name
        self.ER=ER
        self.doping=doping

class Food(Entity):
    def __init__(self,nutrition,icon,name):
        self.nutrition=nutrition
        self.icon=icon
        self.name=name

class Mob(Entity):
    def __init__(self,ab,leader=0):
        self.leader=leader
        self.hp=ab[0]*(4+self.leader)//4
        self.str=ab[1]*(6+self.leader)//6
        self.dex=ab[2]*(6+self.leader)//6
        self.int=ab[3]*(6+self.leader)//6
        self.BAC=ab[4]*(8+self.leader)//8
        self.bp=0
        self.fp=0
        self.group=ab[5]
        self.shout=ab[6]*(1+self.leader)
        self.aware=ab[7]
        self.type=ab[8]
        self.icon=ab[9]
        self.name=ab[10]+((L_N if self.leader==1 else ab[17][0]) if self.leader else '')
        self.wield=Weapon(ab[14][0],ab[14][1],ab[14][2],*ab[14][3:]) if self.leader else Weapon(1,1,1,Weapon_icon,'')
        self.wear=Armor(*ab[15]) if self.leader else Armor(0,Armor_icon,'',0)
        if(self.wield.dual==3):
            self.shield=self.wield
            self.DV=1
        elif(len(ab)>16 and self.leader):
            self.shield=Weapon(*ab[16])
            self.DV=0
        else:
            self.shield=Weapon(0,0,0,Shield_icon,'',2)
            self.DV=1
        self.MR=self.shield.MR
        if leader:
            self.inventory=[Item('?',1,'magic potion')]*(d(self.int)*(2+self.leader)//PT_divide)+[Item('?',0,'healing potion')]*(d(self.str)*(2+self.leader)//PT_divide)+[Item('?',3,'energetic potion')]*(d(self.dex)*(2+self.leader)//PT_divide)+[Food(4,'%','bread ration')]*(d(d(3*self.leader+1))-1)+[Food(8,'%','pizza')]*(d(d(self.leader))-1)
        else:
            self.inventory=[Food(4,'%','bread ration')]*(d(d(d(d(4))))-1)
        self.ER=self.shield.ER+self.wear.ER
        self.mp=(self.int*self.wield.intm*ER_divide)//(ER_divide+self.ER)
        self.VIT=self.hp
        self.AC=self.BAC+self.wear.AC+self.shield.AC
        self.xp=ab[12]*(2**self.leader)
        self.lvl=1 if self.xp<=XP_base else floor(log(self.xp/XP_base,2.0))+1
        self.drop=[Food(2,Food_icon,'chunk of meat')]*(rlrange(self.lvl*2)>self.lvl)+[self.shield]*(self.shield.name!=self.wield.name and bool(self.shield.name))+[self.wield]*bool(self.wield.name)+[self.wear]*bool(self.wear.name)
        self.doping=ab[13]
        self.status={'hitstun':0,'poison':0}
        if(len(ab)>17):
            self.catchphrase=ab[17][1]

class Me(Entity):
    def __init__(self,ab):
        self.hp=ab[0]
        self.str=ab[1]
        self.dex=ab[2]
        self.int=ab[3]
        self.BAC=ab[4]
        self.bp=ab[5]
        self.fp=ab[6]
        self.x=ab[7]
        self.y=ab[8]
        self.MR=0
        self.ER=0
        self.lvl=lvl
        self.sp=self.hp
        self.name=name
        self.inventory=[]
        self.abilities=set()
        self.skills=set()
        self.wear=Armor(0,Armor_icon,'rags',0)
        self.shield=Weapon(2,0,0,Shield_icon,'buckler',2)
        self.DV=0
        self.wield=Weapon(1,1,1,Weapon_icon,'dagger')
        self.AC=self.BAC+self.shield.AC+self.wear.AC
        self.mp=(self.int*self.wield.intm*ER_divide)//(ER_divide+self.ER)
        self.VIT=self.hp
        self.doping=[]
        self.status={'hitstun':0,'poison':0}
        self.relics={'Stakes':[0,7],'Rabbit Feet':[0,400]}
