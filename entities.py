from settings import Armor_icon,Weapon_icon,ER_divide,xp_fun,lvl
class Entity:
	def __init__(self,name):
		self.name=name
class Item(Entity):
	def __init__(self,icon,number,name):
		self.name=name
		self.icon=icon
		self.number=number
class Weapon(Entity):
	def __init__(self,strm,dexm,intm,icon,name):
		self.strm=strm
		self.dexm=dexm
		self.intm=intm
		self.icon=icon
		self.name=name
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
	def __init__(self,ab,wield=Weapon(1,1,1,Weapon_icon,'dagger'),wear=Armor(0,Armor_icon,'rags',0),inventory=[],l=1):
		self.hp=ab[0]
		self.str=ab[1]
		self.dex=ab[2]
		self.int=ab[3]
		self.AC=ab[4]
		self.bp=ab[5]
		self.fp=ab[6]
		self.aware=ab[7]
		self.type=ab[8]
		self.icon=ab[9]
		self.name=ab[10]
		self.inventory=inventory
		self.wear=wear
		self.wield=wield
		self.lvl=l
		self.mp=(self.int*self.wield.intm*ER_divide)//(ER_divide+self.wear.ER)
		self.VIT=self.hp
		self.xp=xp_fun(self)*ab[11]
class Me(Entity):
	def __init__(self,ab):
		self.hp=ab[0]
		self.str=ab[1]
		self.dex=ab[2]
		self.int=ab[3]
		self.AC=ab[4]
		self.bp=ab[5]
		self.fp=ab[6]
		self.x=ab[7]
		self.y=ab[8]
		self.lvl=lvl
		self.sp=self.hp
		self.name='Player'
		self.inventory=[]
		self.abilities=set()
		self.wear=Armor(0,Armor_icon,'rags',0)
		self.wield=Weapon(1,1,1,Weapon_icon,'dagger')
		self.mp=(self.int*self.wield.intm*ER_divide)//(ER_divide+self.wear.ER)
		self.VIT=self.hp
