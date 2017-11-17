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
		self.name=name
		self.icon=icon
		self.number=number
class Weapon(Entity):
	def __init__(self,a,b,c,icon,name,dual=1,d=0,e=0,f=0):
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
class Armor(Entity):
	def __init__(self,AC,icon,name,ER):
		self.AC=AC
		self.icon=icon
		self.name=name
		self.ER=ER
class Food(Entity):
	def __init__(self,nutrition,icon,name):
		self.nutrition=nutrition
		self.icon=icon
		self.name=name
class Mob(Entity):
	def __init__(self,ab):
		self.hp=ab[0]
		self.str=ab[1]
		self.dex=ab[2]
		self.int=ab[3]
		self.AC=ab[4]
		self.bp=0
		self.fp=0
		self.group=ab[5]
		self.shout=ab[6]
		self.aware=ab[7]
		self.type=ab[8]
		self.icon=ab[9]
		self.name=ab[10]
		self.inventory=ab[11]
		self.wield=Weapon(rlrange(ab[12][0]),rlrange(ab[12][1]),rlrange(ab[12][2]),*ab[12][3:])
		self.alarming=1 if self.wield.strm+self.wield.dexm+self.wield.intm==ab[12][0]+ab[12][1]+ab[12][2] else 0
		self.wear=Armor(*ab[13])
		if(self.wield.dual==3):
			self.shield=self.wield
		elif(len(ab)>14):
			self.shield=Weapon(*ab[14])
		else:
			self.shield=Weapon(0,0,0,Shield_icon,'',2)
		self.MR=self.shield.MR
		self.ER=self.shield.ER+self.wear.ER
		self.mp=(self.int*self.wield.intm*ER_divide)//(ER_divide+self.ER)
		self.VIT=self.hp
		self.BAC=self.AC-self.wear.AC-self.shield.AC
		self.xp=xp_fun(self)
		self.lvl=1 if self.xp<=XP_base else floor(log(self.xp/XP_base,2.0))+1
		self.drop=[Food(2,Food_icon,'chunk of meat')]*(rlrange(self.lvl*2)>self.lvl)+[self.shield]*(len(ab)>14 and rlrange(self.lvl)>=d(4))+[self.wield]*(rlrange(self.lvl)>=d(4)-self.alarming)+[self.wear]*(rlrange(self.lvl)>=d(4))

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
		self.name='Player'
		self.inventory=[]
		self.abilities=set()
		self.wear=Armor(0,Armor_icon,'rags',0)
		self.shield=Weapon(2,0,0,Shield_icon,'buckler',2)
		self.wield=Weapon(1,1,1,Weapon_icon,'dagger')
		self.AC=self.BAC+self.shield.AC+self.wear.AC
		self.mp=(self.int*self.wield.intm*ER_divide)//(ER_divide+self.ER)
		self.VIT=self.hp
