from msvcrt import getch as g
from msvcrt import getwch as w
from copy import deepcopy
from os import system as s
from os import path
from settings import *
from entities import *
try:
	from map import Map
except ModuleNotFoundError as err :
	Messages+=['Failed to import map file, '+str(err)]
	Map='.'*262144
try:
	from presets import *
except ModuleNotFoundError as err:
	Presets=()
	Messages+=['Failed to import presets file, '+str(err)]
Know_list=[0]*len(Effects_list)
for i in range(len(Effects_list)):
	Title=''
	for l in range(d(4)*d(2)+d(4)):
		Title+=chr(64+d(26))
	Titles_list+=[Title]
try:
	from boss import *
except ImportError as err:
	Messages+=['Failed to import boss file, '+str(err)]
except NameError as err:
	Messages+=['Failed to import boss file, '+str(err)]
def un(x,y):
	return not (x,y) in Total_list[::2]
def disx(x):
	return abs(player.x-x)
def disy(y):
	return abs(player.y-y)
def dis(x,y):
	return max(disx(x),disy(y))
def sig(x):
	if(x>0):
		return 1
	elif(x<0):
		return -1
	else:
		return 0
def lvlup(x):
	x.lvl+=1
	if(d(3)==1):
		x.str+=1
	elif(d(2)==1):
		x.dex+=1
	else:
		x.int+=1
	if(x.lvl%5==0):
		if(x.name=='Player' and not x.abilities is Ability):
			qyu=''
			for i in (Ability - x.abilities):
				qyu+='If you want to become '+i[0].upper()+i[1:]+', type in '+i+'.\n'
			qyu+='If you want to become stronger, type in anything else.'
			screen(0,0,qyu)
			a=input('')
			global Messages
			if(a in Ability):
				x.abilities=x.abilities | {a}
				a=Cool_dict[a]
				Messages+=[a[0]]
				x.str+=a[1]
				x.dex+=a[2]
				x.int+=a[3]
			else:
				x.str+=Coolness
				x.dex+=Coolness
				x.int+=Coolness
		else:
			x.str+=Coolness
			x.dex+=Coolness
			x.int+=Coolness
	return x
def levelup():
	global player
	while(XP>=XP_base*2**player.lvl):
		player=lvlup(player)
#####################
#######setting#######
#####################
def consume(ent,what):
	if(what==0):
		ent.hp=ent.VIT
		ent.bp=0
		ent.fp=ent.fp//2
		ent.sp+=2
	elif(what==1):
		ent.mp=(ent.int*ent.wield.intm*ER_divide)//(ER_divide+ent.ER)
		ent.fp=ent.fp//2
		ent.bp=ent.bp//2
		ent.sp+=2
	elif(what==2):
		ent.hp=ent.hp//3
		ent.fp+=10
		ent.sp-=2
	elif(what==3):
		ent.fp=-(ent.dex+10)**2//25
		ent.bp=ent.bp*3
		ent.sp+=4
	elif(what==4):
		ent=lvlup(ent)
	return ent
#####################
#setting#####potions#
#####################
def generate():
	global Total_list
	Total_list=[]
	for i in range(512):
		for l in range(512):
			if(Map[i+l*512]=='.'):
				if(i==511 or i==0 or l==511 or l==0):
					Total_list+=[(i,l),Mob(Mob_list[0])]
				elif(250<i and i<262 and 250<l and l<262):
					pass
				elif(d(200)==1):
					usl=rl(RL_Mobs)
					Total_list+=[(i,l),Mob(Mob_list[usl])]
				elif(d(1000)==1):
					usl=rl(RL_Potions)
					Total_list+=[(i,l,0),Item(Potion_icon,usl,Titles_list[usl])]
				elif(d(1000)==1):
					usl=rl(RL_Food)
					Total_list+=[(i,l,0),Food(Food_nutrition_list[usl],Food_icon,Food_types_list[usl])]
				elif(d(5000)==1):
					usl=rl(RL_Weapons)
					Total_list+=[(i,l,0),Weapon(d(Weapon_m_list[usl][0]),d(Weapon_m_list[usl][1]),d(Weapon_m_list[usl][2]),Weapon_icon,Weapon_types_list[usl])]
				elif(d(5000)==1):
					usl=rl(RL_Armor)
					Total_list+=[(i,l,0),Armor(Armor_AC_ER_list[usl][0],Armor_icon,Armor_types_list[usl],Armor_AC_ER_list[usl][1])]
			else:
				a=Map[i+l*512]
				if(a is Wall_icon):
					Total_list+=[(i,l),Mob(Mob_list[0])]
				elif(a is Boss_icon):
					try:
						Total_list+=[(i,l),Boss()]
					except NameError as err:
						Total_list+=[(i,l),Mob(Mob_list[rl(RL_Mobs)])]
						global Messages
						Messages+=['Failed to import boss, '+str(err)]
				elif(97<=ord(a.lower())<=122):
					usl1=rl(RL_Weapons)
					usl2=rl(RL_Armor)
					usl3=rl(RL_Mobs)
					auto=()
					for r in Presets:
						if(r[9] is a):
							auto=r
					Total_list+=[(i,l),Mob(auto)] if auto!=() else [(i,l),Mob(Mob_list[usl3])]
				elif(a is Potion_icon):
					usl=rl(RL_Potions)
					Total_list+=[(i,l,0),Item(Potion_icon,usl,Titles_list[usl])]
				elif(a is Food_icon):
					usl=rl(RL_Food)
					Total_list+=[(i,l,0),Food(Food_nutrition_list[usl],Food_icon,Food_types_list[usl])]
				elif(a is Weapon_icon):
					usl=rl(RL_Weapons)
					Total_list+=[(i,l,0),Weapon(d(Weapon_m_list[usl][0]),d(Weapon_m_list[usl][1]),d(Weapon_m_list[usl][2]),Weapon_icon,Weapon_types_list[usl])]
				elif(a is Armor_icon):
					usl=rl(RL_Armor)
					Total_list+=[(i,l,0),Armor(Armor_AC_ER_list[usl][0],Armor_icon,Armor_types_list[usl],Armor_AC_ER_list[usl][1])]
#####################
#######setting#######
#####################
	return Me([VIT,8,8,8,4,0,0,256,256])
def attack(enA,enD):
	global Messages
	atk=d(enA.str*enA.wield.strm+d(enA.dex*enA.wield.dexm*2))//2
	if(atk>enD.AC):
		enD.hp+=enD.AC-atk
		enD.bp+=atk*d(enA.int*enA.wield.intm)//d(enD.AC)
		Messages+=[enA.name+' hits '+enD.name+'.']
	else:
		Messages+=[enD.name+' blocks '+enA.name+"'s hit."]
	enA.fp+=2
	return enA,enD
def farattack(enA,enD):
	global Messages
	atk=d(enA.dex*enA.wield.dexm+d(enA.dex*enA.wield.dexm*d(2)))//2
	if(atk>enD.AC//2):
		enD.hp+=enD.AC//2-atk
		enD.bp+=atk*d(enA.dex*enA.wield.dexm)//d(enD.AC)
		Messages+=[enA.name+' hits '+enD.name+' from afar.']
	else:
		Messages+=[enD.name+' blocks '+enA.name+"'s hit."]
	enA.fp+=4
	return enA,enD
def rushattack(enA,enD):
	global Messages
	atk=d(enA.str*enA.wield.strm+d(enA.str*enA.wield.strm*d(2)))//2+enA.str*enA.wield.strm
	if(atk>enD.AC and d(enA.dex)>d(enD.dex)):
		enD.hp+=enD.AC//2-atk
		enD.fp+=atk*d(enA.str*enA.wield.strm)//d(enD.AC)
		Messages+=[enA.name+' crushes '+enD.name+' mightily.']
	else:
		Messages+=[enA.name+' crushes floor near '+enD.name+"'s feet."] if atk>enD.AC else [enD.name+' barely blocks '+enA.name+"'s hit."]
	enA.fp+=8
	return enA,enD
def magicattack(enA,enD):
	global Messages
	atk=d(enA.int*enA.wield.intm+d(enA.int*enA.wield.intm*d(2)))*MR_divide//(MR_divide+enD.ER)//2
	if(atk>enD.AC//3+enD.mp):
		enD.hp+=enD.AC//3+enD.mp-atk
		enD.fp+=d(atk)
		enD.mp=0
		Messages+=[enA.name+' gestures at '+enD.name+'.']
		Messages+=['Pain surges through '+enD.name+"'s body."]
	else:
		if(atk>enD.AC//3):
			enD.mp+=enD.AC//3-atk
		Messages+=[enA.name+' gestures at '+enD.name+'.']
	enA.fp+=4
	enA.mp-=Magic_value
	return enA,enD
#####################
#setting#####attacks#
#####################
def move(n):
	global Total_list,Messages,Pop_list,XP,player
	zz=Total_list[n*2+1]
	if(len(Total_list[n*2])==2):
		if(zz.hp<=0):
			Messages+=[player.name+' kills '+zz.name+'.']
			XP+=zz.xp
			levelup()
			Pop_list+=[n*2]
		elif(zz.type>=0):
			xx=Total_list[n*2][0]
			yy=Total_list[n*2][1]
			if(zz.bp>=zz.hp):
				Messages+=[player.name+' kills '+zz.name+'.']
				XP+=zz.xp
				levelup()
				Pop_list+=[n*2]
			elif(zz.aware==0 or dis(xx,yy)>=6+zz.aware*d(zz.int)//3):
				zz.aware=1 if dis(xx,yy)<6+rl((9,3,1))+zz.aware*d(zz.int)//3 else 0
			elif(zz.fp>d(20+zz.dex-zz.ER*SR_divide//(SR_divide+zz.str)) or (zz.fp>=zz.dex and zz.type%2==1) or (zz.fp>=d(zz.dex) and zz.type%3==2)):
				zz.fp-=zz.dex
				if(zz.fp<0):
					zz.fp=0
			elif(dis(xx,yy)==2 and zz.type%3==1):
				zz,player=farattack(zz,player)
			elif(zz.type%2==1 and zz.mp>=Magic_value and dis(xx,yy)<=Magic_distance):
				zz,player=magicattack(zz,player)
			elif(dis(xx,yy)==1 and zz.type%3==2):
				zz,player=rushattack(zz,player)
			elif(dis(xx,yy)==1):
				zz,player=attack(zz,player)
			elif((zz.type%2==1 and dis(xx,yy)<=4) or (zz.type%3==1 and dis(xx,yy)==1 and d(zz.int)>=4)):
				if(un(xx-sig(player.x-xx),yy-sig(player.y-yy))):
					Total_list[n*2]=(xx-sig(player.x-xx),yy-sig(player.y-yy))
					zz.fp+=1
				elif(disx(xx)>disy(yy) and un(xx-sig(player.x-xx),yy)):
					Total_list[n*2]=(xx-sig(player.x-xx),yy)
					zz.fp+=1
				elif(un(xx,yy-sig(player.y-yy))):
					Total_list[n*2]=(xx,yy-sig(player.y-yy))
					zz.fp+=1
				else:
					zz.fp-=zz.dex
					if(zz.fp<0):
						zz.fp=0
			elif(un(xx+sig(player.x-xx),yy+sig(player.y-yy))):
				Total_list[n*2]=(xx+sig(player.x-xx),yy+sig(player.y-yy))
				zz.fp+=1
			elif(disx(xx)>disy(yy) and un(xx+sig(player.x-xx),yy)):
				Total_list[n*2]=(xx+sig(player.x-xx),yy)
				zz.fp+=1
			elif(un(xx,yy+sig(player.y-yy))):
				Total_list[n*2]=(xx,yy+sig(player.y-yy))
				zz.fp+=1
			else:
				zz.fp-=zz.dex
				if(zz.fp<0):
					zz.fp=0
			zz.hp-=zz.bp
			zz.bp=zz.bp*3//2
			if(d(zz.VIT-zz.bp)>0 and zz.hp<zz.VIT):
				zz.hp+=1
			if(d(zz.VIT+zz.int*zz.wield.intm-zz.mp)>zz.VIT-zz.int*zz.wield.intm and zz.mp<(zz.int*zz.wield.intm*ER_divide)//(ER_divide+zz.ER)):
				zz.mp+=1
			Total_list[n*2+1]=zz
def help():
	global Messages
	Messages+=['']
	Messages+=['r t y']
	Messages+=['f   h  move/attack.']
	Messages+=['v b n']
	Messages+=['.      rest one turn.']
	Messages+=['g      get item on your tile.']
	Messages+=['i      use item in your inventory.']
	Messages+=['d      destroy item in inventory.']
	Messages+=['Esc    exit.']
	Messages+=['?      help.']
	Messages+=['!      abbreviations in stats.']
	Messages+=['#      icons list.']
	Messages+=['*      view transcript.']
def abbs():
	global Messages
	Messages+=['']
	Messages+=['STR    strenght.']
	Messages+=['DEX    dexterity.']
	Messages+=['INT    intellect.']
	Messages+=['HP     health points.']
	Messages+=['MP     magic points.']
	Messages+=['BP     bleed points.']
	Messages+=['FP     fatigue points.']
	Messages+=['SP     saturation points.']
	Messages+=['XP     experience points.']
	Messages+=['SM     stats multiplier from wielded weapon.']
	Messages+=['AC     summary armor count.']
	Messages+=['ER     armor encumbrance rating.']
def icons():
	global Messages
	Messages+=['']
	Messages+=[Player_icon+' '*6+'player.']
	Messages+=[Potion_icon+' '*6+'potion.']
	Messages+=[Weapon_icon+' '*6+'weapon.']
	Messages+=[Armor_icon+' '*6+'armor.']
	Messages+=[Food_icon+' '*6+'food.']
	Messages+=[Wall_icon+' '*6+'wall.']
	Messages+=[Boss_icon+' '*6+'boss.']
	Messages+=['Letters represent enemies.']
##!#test#!##
def xp():
	global Messages
	for i in Mob_list:
		zoo=Mob(i)
		Messages+=[zoo.icon+' '+zoo.name+(15-len(zoo.name))*' '+str(zoo.xp)+(8-len(str(zoo.xp)))*' '+str(i)]
def story():
	s('cls')
	print(*Messages[-transcript*3:],sep='\n')
	print('Press any key to continue.')
##!#test#!##
def controls():
	global player,Total_list,Messages,familiar
	retry=0
	a=g()
	if(a==b'?'):
		help()
		retry=1
	elif(a==b'!'):
		abbs()
		retry=1
	elif(a==b'#'):
		icons()
		retry=1
	elif(a==b'.'):
		player.fp=max(player.fp-player.dex*(50-player.VIT+player.sp)//50,0)
	elif(a==b'r'):
		if(un(player.x-1,player.y+1)):
			player.x-=1
			player.y+=1
			player.fp+=1
		else:
			player,Total_list[Total_list.index((player.x-1,player.y+1))+1]=attack(player,Total_list[Total_list.index((player.x-1,player.y+1))+1])
	elif(a==b't'):
		if(un(player.x,player.y+1)):
			player.y+=1
			player.fp+=1
		else:
			player,Total_list[Total_list.index((player.x,player.y+1))+1]=attack(player,Total_list[Total_list.index((player.x,player.y+1))+1])
	elif(a==b'y'):
		if(un(player.x+1,player.y+1)):
			player.x+=1
			player.y+=1
			player.fp+=1
		else:
			player,Total_list[Total_list.index((player.x+1,player.y+1))+1]=attack(player,Total_list[Total_list.index((player.x+1,player.y+1))+1])
	elif(a==b'h'):
		if(un(player.x+1,player.y)):
			player.x+=1
			player.fp+=1
		else:
			player,Total_list[Total_list.index((player.x+1,player.y))+1]=attack(player,Total_list[Total_list.index((player.x+1,player.y))+1])
	elif(a==b'n'):
		if(un(player.x+1,player.y-1)):
			player.x+=1
			player.y-=1
			player.fp+=1
		else:
			player,Total_list[Total_list.index((player.x+1,player.y-1))+1]=attack(player,Total_list[Total_list.index((player.x+1,player.y-1))+1])
	elif(a==b'b'):
		if(un(player.x,player.y-1)):
			player.y-=1
			player.fp+=1
		else:
			player,Total_list[Total_list.index((player.x,player.y-1))+1]=attack(player,Total_list[Total_list.index((player.x,player.y-1))+1])
	elif(a==b'v'):
		if(un(player.x-1,player.y-1)):
			player.x-=1
			player.y-=1
			player.fp+=1
		else:
			player,Total_list[Total_list.index((player.x-1,player.y-1))+1]=attack(player,Total_list[Total_list.index((player.x-1,player.y-1))+1])
	elif(a==b'f'):
		if(un(player.x-1,player.y)):
			player.x-=1
			player.fp+=1
		else:
			player,Total_list[Total_list.index((player.x-1,player.y))+1]=attack(player,Total_list[Total_list.index((player.x-1,player.y))+1])
	elif(a==b'z' and 'caster' in player.abilities):
		a=b''
		dx=0
		dy=0
		dt=-1
		while(a!=b'\r' and a!=b'\x1b' and a!=b'g'):
			if(a==b'r'):
				dx-=1
				dy+=1
			elif(a==b't'):
				dy+=1
			elif(a==b'y'):
				dx+=1
				dy+=1
			elif(a==b'h'):
				dx+=1
			elif(a==b'n'):
				dx+=1
				dy-=1
			elif(a==b'b'):
				dy-=1
			elif(a==b'v'):
				dx-=1
				dy-=1
			elif(a==b'f'):
				dx-=1
			elif(a==b'a' and len(Targets)>0):
				dt+=1
				if(dt==len(Targets)):
					dt=0
				dx=Targets[dt][0]
				dy=Targets[dt][1]
			if(abs(dx)>Magic_distance):
				dx=sig(dx)*Magic_distance
			if(abs(dy)>Magic_distance):
				dy=sig(dy)*Magic_distance
			screen(dx,dy,'    r t y\nUse f   h to navigate, Esc to abort, Enter or g to confirm target.\n    v b n\na to auto-target.')
			a=g()
		if(a==b'\x1b'):
			retry=1
		else:
			if(un(player.x+dx,player.y+dy)):
				if(bonus==1):
					if(player.mp>=max(abs(dx),abs(dy))*2):
						player.x+=dx
						player.y+=dy
						player.mp-=max(abs(dx),abs(dy))*2
						Messages+=['Player teleports.']
					else:
						Messages+=['Not enough MP.']
						retry=1
				else:
					Messages+=['Invalid target.']
					retry=1
			else:
				if(player.mp>=Magic_value):
					player,Total_list[Total_list.index((player.x+dx,player.y+dy))+1]=magicattack(player,Total_list[Total_list.index((player.x+dx,player.y+dy))+1])
				else:
					Messages+=['Not enough MP.']
					retry=1
	elif(a==b'x' and 'lancer' in player.abilities):
		a=b''
		dx=0
		dy=0
		while(a!=b'\r' and a!=b'\x1b' and a!=b'g'):
			if(a==b'r'):
				dx-=1
				dy+=1
			elif(a==b't'):
				dy+=1
			elif(a==b'y'):
				dx+=1
				dy+=1
			elif(a==b'h'):
				dx+=1
			elif(a==b'n'):
				dx+=1
				dy-=1
			elif(a==b'b'):
				dy-=1
			elif(a==b'v'):
				dx-=1
				dy-=1
			elif(a==b'f'):
				dx-=1
			if(abs(dx)>2):
				dx=sig(dx)*2
			if(abs(dy)>2):
				dy=sig(dy)*2
			if(abs(dy)<2 and abs(dx)<2):
				dy=dy*2
				dx=dx*2
			screen(dx,dy,'    r t y\nUse f   h to navigate, Esc to abort, Enter or g to confirm target.\n    v b n')
			a=g()
		if(a==b'\x1b'):
			retry=1
		else:
			if(un(player.x+dx,player.y+dy)):
				Messages+=['Invalid target.']
				retry=1
			else:
				player,Total_list[Total_list.index((player.x+dx,player.y+dy))+1]=farattack(player,Total_list[Total_list.index((player.x+dx,player.y+dy))+1])
	elif(a==b'c' and 'berserker' in player.abilities):
		a=b''
		dx=0
		dy=0
		while(a!=b'\r' and a!=b'\x1b' and a!=b'g'):
			if(a==b'r'):
				dx-=1
				dy+=1
			elif(a==b't'):
				dy+=1
			elif(a==b'y'):
				dx+=1
				dy+=1
			elif(a==b'h'):
				dx+=1
			elif(a==b'n'):
				dx+=1
				dy-=1
			elif(a==b'b'):
				dy-=1
			elif(a==b'v'):
				dx-=1
				dy-=1
			elif(a==b'f'):
				dx-=1
			if(abs(dx)>1):
				dx=sig(dx)
			if(abs(dy)>1):
				dy=sig(dy)
			screen(dx,dy,'    r t y\nUse f   h to navigate, Esc to abort, Enter or g to confirm target.\n    v b n')
			a=g()
		if(a==b'\x1b'):
			retry=1
		else:
			if(un(player.x+dx,player.y+dy)):
				Messages+=['Invalid target.']
				retry=1
			else:
				player,Total_list[Total_list.index((player.x+dx,player.y+dy))+1]=rushattack(player,Total_list[Total_list.index((player.x+dx,player.y+dy))+1])
	elif(a==b'i'):
		if(len(player.inventory)>0):
			s('cls')
			for i in range(len(player.inventory)):
				print(chr(i+97)+'- '+str(player.inventory[i].name))
			a=ord(w())-97
			if(0<=a<=len(player.inventory)-1):
				if(player.inventory[a].name in Weapon_types_list):
					if(player.inventory[a].dual%2==1):
						player.inventory+=[player.wield]
						Messages+=[player.name+' unwields '+player.wield.name+'.']
						player.wield=player.inventory[a]
						Messages+=[player.name+' wields '+player.wield.name+'.']
						familiar=[0,0,0]
					else:
						player.inventory+=[player.shield]
						Messages+=[player.name+' unwields '+player.shield.name+'.']
						player.shield=player.inventory[a]
						Messages+=[player.name+' wields '+player.shield.name+'.']
					if(player.wield.dual==3):
						player.AC=player.BAC+player.wear.AC+player.wield.AC
						player.ER=player.wear.ER+player.wield.ER
						player.MR=player.wield.MR
					else:
						player.AC=player.BAC+player.wear.AC+player.shield.AC
						player.ER=player.wear.ER+player.shield.ER
						player.MR=player.shield.MR
					player.mp=min(player.mp,(player.int*player.wield.intm*ER_divide)//(ER_divide+player.ER))
				elif(player.inventory[a].name in Armor_types_list):
					player.AC-=player.wear.AC
					player.ER-=player.wear.ER
					Messages+=[player.name+' unequips '+player.wear.name+'.']
					player.inventory+=[player.wear]
					player.wear=player.inventory[a]
					player.AC+=player.wear.AC
					player.ER+=player.wear.ER
					player.mp=min(player.mp,(player.int*player.wield.intm*ER_divide)//(ER_divide+player.ER))
					Messages+=[player.name+' equips '+player.wear.name+'.']
				elif(player.inventory[a].name in Food_types_list):
					player.sp=min(player.VIT,player.sp+player.inventory[a].nutrition)
					Messages+=[player.name+' eats '+player.inventory[a].name+'.']
				else:
					what=player.inventory[a].number
					player=consume(player,what)
					global Know_list
					if(Know_list[what]==0):
						Know_list[what]=Titles_list[what]
						for i in player.inventory:
							if(i.name is Titles_list[what]):
								i.name=Effects_list[what]
					Messages+=[player.name+' drinks '+Effects_list[what]+'.']
				player.inventory.pop(a)
			else:
				if(a!=-70):
					Messages+=['No such item.']
				retry=1
		else:
			Messages+=[player.name+"'s inventory is empty."]
			retry=1
	elif(a==b's'):
		player.inventory.sort(key=lambda x : x.fn)
		Messages+=[player.name+' sorts their inventory.']
	elif(a==b'g'):
		if(len(player.inventory)<26):
			ko=(player.x,player.y,0)
			if(ko in Total_list):
				mur=Total_list.index(ko)
				player.inventory+=[Total_list[mur+1]]
				Total_list.pop(mur)
				Total_list.pop(mur)
				if(player.inventory[-1].name in Know_list):
					player.inventory[-1].name=Effects_list[player.inventory[-1].number]
				Messages+=[player.name+' picks up '+player.inventory[-1].name+'.']
			else:
				Messages+=['There is nothing here.']
				retry=1
		else:
			Messages+=[player.name+"'s inventory is already full."]
			retry=1
	elif(a==b'\x1b'):
		exit()
	elif(a==b'd'):
		if(len(player.inventory)>0):
			s('cls')
			for i in range(len(player.inventory)):
				print(chr(i+97)+'- '+str(player.inventory[i].name))
			a=ord(w())-97
			if(0<=a<=len(player.inventory)-1):
				Messages+=['Player destroys '+player.inventory[a].name+'.']
				player.inventory.pop(a)
			else:
				if(a!=-70):
					Messages+=['No such item.']
				retry=1
		else:
			Messages+=[player.name+"'s inventory is empty."]
			retry=1
	elif(a==b'\x18'):
		xp()
		retry=1
	elif(a==b'*'):
		story()
		g()
		retry=1
	else:
		Messages+=['Unknown command.']
		retry=1
	if(retry==1):
		screen()
		controls()
	else:
		if(player.lvl>=player.wield.strm and familiar[0]==0):
			Messages+=[player.name+' feels more familiar with their weapon.']
			familiar[0]=1
		if(player.lvl>=player.wield.dexm and familiar[1]==0):
			Messages+=[player.name+' feels more familiar with their weapon.']
			familiar[1]=1
		if(player.lvl>=player.wield.intm and familiar[2]==0):
			Messages+=[player.name+' feels more familiar with their weapon.']
			familiar[2]=1
		player.hp-=player.bp
		if(bonus!=1):
			if(player.bp*3>player.VIT):
				Messages+=[player.name+' bleeds heavily.']
			elif(player.bp*5>player.VIT):
				Messages+=[player.name+' bleeds severally.']
			elif(player.bp*9>player.VIT):
				Messages+=[player.name+' bleeds mildly.']
			elif(player.bp>0):
				Messages+=[player.name+' bleeds lightly.']
			if(player.sp*5<player.VIT):
				Messages+=[player.name+' is almost starving.']
			elif(player.sp*3<player.VIT):
				Messages+=[player.name+' is very hungry.']
			elif(player.sp*2<player.VIT):
				Messages+=[player.name+' is hungry.']
		player.sp=min(player.sp,player.VIT)
#####################
#######setting#######
#####################
		player.bp=player.bp*player.VIT//(player.sp//2+player.VIT)
		player.sp-=d(player.VIT-player.hp)//5
		if(d(player.VIT-player.bp)>max(player.VIT//2,player.VIT-player.sp) and player.hp<player.sp):
			player.hp+=1
		if(d(player.VIT+player.int*player.wield.intm-player.mp)>player.VIT-player.int*player.wield.intm and player.mp<(player.int*player.wield.intm*ER_divide)//(ER_divide+player.ER)):
			player.mp+=1
		if(player.sp<0):
			player.hp+=player.sp
			player.sp=0
			Messages+=[player.name+' starves.']
#####################
#setting######points#
#####################
def check(xx,yy):
	if((xx,yy) in Total_list[::2]):
		if(max(abs(player.x-xx),abs(player.y-yy))<=Magic_distance):
			global Targets
			Targets+=[(xx-player.x,yy-player.y)]
		return Total_list[Total_list.index((xx,yy))+1].icon
	elif((xx,yy,0) in Total_list[::2]):
		return Total_list[Total_list.index((xx,yy,0))+1].icon
	else:
		return '.'
def screen(x=0,y=0,extra=''):
	global Targets
	show=[]
	for i in range(17):
		show+=[[',']*17]
	Targets=[]
	for i in range(17):
		for l in range(17):
			show[16-l][i]=check(player.x+i-8,player.y+l-8)
	show[8-y][8+x]=Magic_icon
	show[8][8]=Player_icon
	zzzz=''
	for i in show:
		for l in i:
			zzzz+=l
		zzzz+='\n'
	global Messages
	Messages=Messages[-transcript*3:]
	ab=''
	for i in player.abilities:
		ab+=i+' '
	if(ab==''):
		ab='-'
	s('cls')
	print('\nSTR:'+str(player.str)+' '*(10-len(str(player.str)))+'HP:'+str(player.hp),'DEX:'+str(player.dex)+' '*(10-len(str(player.dex)))+'MP:'+str(player.mp),'INT:'+str(player.int)+' '*(10-len(str(player.int)))+'FP:'+str(player.fp),'SP:'+str(player.sp)+' '*(11-len(str(player.sp)))+'BP:'+str(player.bp),sep='\n')
	print('Wield:'+player.wield.name,'Wear:'+player.wear.name,'Shield:'+(str(player.shield.name) if player.wield.dual==1 else '-'),'Abilities:'+ab,sep='\n')
	print('MR:'+str(player.MR)+' '*(11-len(str(player.MR)))+'SM:'+(str(player.wield.strm) if familiar[0]==1 else '?')+','+(str(player.wield.dexm) if familiar[1]==1 else '?')+','+(str(player.wield.intm) if familiar[2]==1 else '?'),'ER:'+str(player.ER)+' '*(11-len(str(player.ER)))+'AC:'+str(player.AC),'XP:'+str(XP)+' '*(11-len(str(XP)))+'Level:'+str(player.lvl),zzzz,*Messages[-transcript:],sep='\n')
	print(extra)
player=generate()
while(True):
	Pop_list=[]
	screen()
	if(player.fp<d(20+player.dex-player.ER*SR_divide//(SR_divide+player.str))):
		controls()
	else:
		player.fp=0 if player.fp<=player.dex else player.fp-player.dex
	for i in range(len(Total_list)//2):
		move(i)
	if(player.hp<=0):
		s('cls')
		print('\n   ***'+Messages[-3]+'***   \n   ***'+Messages[-2]+'***   \n   ***'+Messages[-1]+'***   \n   ***Player dies.***   \n')
		while(g()!=b'\x1b'):
			print('Press Esc to exit.')
		exit()
	for i in Pop_list:
		q=Total_list[i+1]
		for k in q.drop:
			Total_list+=[Total_list[i]+tuple([0])]
			Total_list+=[k]
		Total_list.pop(i)
		Total_list.pop(i)
