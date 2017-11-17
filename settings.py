
EASINESS=10

bonus=0
awares=0
PT_awares=0
transcript=13
ER_divide=2
MR_divide=8
SR_divide=12
Mob_appear=30*EASINESS
Noob_Confetti=100*EASINESS
Mob_ungroup=EASINESS
safe=5
Messages=['']*transcript*3
Messages+=['Press ? to get info about controls.']
Total_list=[]
X_Y_list=[]
Potion_icon='?'
Weapon_icon='!'
Armor_icon=']'
Shield_icon='['
Food_icon='%'
Player_icon='@'
Magic_icon='*'
Boss_icon='&'
Wall_icon='#'
Mob_list=((200,0,0,0,1000,0,0,0,-3,Wall_icon,'Wall',0,(0,0,0,Weapon_icon,''),(0,Armor_icon,'',0)),
(10,6,6,4,2,80,6,0,0,'g','Goblin',1,(2,2,2,Weapon_icon,'dagger'),(1,Armor_icon,'robe',0)),
(20,8,2,3,8,60,2,0,0,'k','Kobold',1,(3,2,2,Weapon_icon,'sword'),(3,Armor_icon,'leather armor',2),(2,0,0,Shield_icon,'buckler',2)),
(30,4,8,4,7,40,10,0,4,'G','Gnoll',1,(2,4,1,Weapon_icon,'spear'),(3,Armor_icon,'leather armor',2)),
(20,9,4,2,20,60,4,0,2,'o','Orc',1,(5,1,1,Weapon_icon,'mace'),(5,Armor_icon,'ringmail',10),(6,10,8,Shield_icon,'ceremonial shield',2)),
(10,3,6,8,1,20,8,0,3,'i','Lesser Imp',1,(2,1,4,Weapon_icon,'wand'),(0,Armor_icon,'rags',0)),
(60,20,8,4,20,10,20,0,2,'O','Ogre',1,(8,1,0,Weapon_icon,'cudgel',3,6,10,4),(9,Armor_icon,'shellmail',100)),
(20,8,12,30,4,5,8,0,3,'D','Crimson Demon',1,(0,2,7,Weapon_icon,'rod',3,2,0,12),(0,Armor_icon,'archmage robe',-1)),
(30,12,16,16,9,5,10,0,1,'I','Greater Imp',1,(1,4,4,Weapon_icon,'trident',3,4,0,4),(0,Armor_icon,'rags',0)))
RL_Mobs=(0,8,8,4,4,4,2,1,1)
Effects_list=('healing potion','magic potion','poison potion','energetic potion','experience potion')
Titles_list=[]
RL_Potions=(6,3,5,4,2)
Weapon_types_list=('dagger','sword','mace','spear','wand','cudgel','rod','trident','buckler','ceremonial shield','')
Weapon_m_list=((2,2,2),(3,2,2),(5,1,1),(2,4,1),(2,1,4))
RL_Weapons=(2,8,6,3,3)
Armor_types_list=('ringmail','leather armor','robe','rags','shellmail','archmage robe')
Armor_AC_ER_list=([5,10],[3,2],[1,0],[0,0])
RL_Armor=(1,4,3,0)
Food_types_list=('chunk of meat','bread ration','pizza')
Food_nutrition_list=(2,4,8)
RL_Food=(0,2,1)
VIT=20
Ability={'caster','lancer','berserker'}
Cool_dict={'caster':['Now you possess legendary power of Caster! You can cast dark magic by pressing z!',0,0,5],'lancer':['Now you possess legendary power of Lancer! You can make far-reaching lunges by pressing x!',0,5,0],'berserker':['Now you possess legendary power of Berserker! You can crush your foes by pressing c!',5,0,0]}
Coolness=3
Magic_value=4
Magic_distance=6
XP=0
XP_base=500
familiar=[1,1,1]
lvl=1
Targets=[]
def xp_fun(self):
    if(self.type==0):
        return (self.str**2+self.dex**2+self.str*self.dex+self.int+int(self.hp*1.13**self.BAC))**2//25
    elif(self.type==1):
        return (int((self.int+self.dex)*(1.13**self.int+1.13**self.dex))+self.int**2+self.dex**2+self.int*self.dex++int(self.hp*self.BAC/1.13))**2//25
    elif(self.type==2):
        return (int(self.dex*1.13**self.str)+self.str**2+self.str*self.dex+int(self.int**.13)+int(self.hp*self.BAC**1.13))**2//60
    elif(self.type==3):
        return (int(self.int*1.13**self.int)+self.int**2+self.int*self.dex+self.str+int(self.hp**.19*self.BAC))**2//10
    elif(self.type==4):
        return (int(self.dex*1.13**self.dex)+self.dex**2+self.int+self.str+int(self.hp*self.BAC**1.13/1.13))**2//30
    elif(self.type==5):
        return (int((self.int+self.str+self.dex)*(1.13**self.int+1.13**self.str))+self.int**2+self.str**2+(self.int+self.str)*self.dex++int(self.hp*self.BAC**1.13))**2//60
    else:
        return (2*((self.type%3==2)+2)*self.str**3+2*((self.type%3==1)+2)*self.dex**3+2*((self.type%2==1)+2)*self.int**3+(self.str+self.dex+self.int+2*(self.AC-self.wear.AC-self.shield.AC))*self.str*self.dex*self.int)//100*(self.VIT+self.AC-self.wear.AC-self.shield.AC+self.str+self.dex+self.int)
