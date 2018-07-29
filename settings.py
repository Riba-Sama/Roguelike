bonus=0
awares=0
PT_awares=0
transcript=19
ER_divide=2
Floor=1
MR_divide=8
SR_divide=4
DV_divide_a=4
DV_divide_f=1
DV_divide_r=2
ST_divide=2
PT_divide=20
FP_bonus=20
P_value=6
NV_value=6
Status_template={'stun':0,'poison':0,'viper':0,'madness':0,'energy':0,'brilliance':0,'regeneration':0}
controllers=[b'r',b't',b'y',b'h',b'n',b'b',b'v',b'f',b'g',b'i',b'd',b's',b' ',b'z',b'x',b'c',b'u',b'.']
name='Player'
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
Target_icon='x'
Boss_icon='&'
Wall_icon='#'
L_N=' Leader'
Mob_list=(
(200,100,100,100,1000,0,0,0,-1,Wall_icon,'Wall',0,0,['huge'],(0,0,0,Weapon_icon,''),(0,Armor_icon,'',0)),
(10,6,6,4,1,80,6,0,0,'g','Goblin',1,400,[],(2,2,2,Weapon_icon,'dagger'),(1,Armor_icon,'robe',0)),
(20,8,2,3,3,60,2,0,0,'k','Kobold',1,500,[],(3,2,2,Weapon_icon,'sword'),(3,Armor_icon,'leather armor',2),(2,0,0,Shield_icon,'buckler',2)),
(30,4,8,4,4,40,10,0,2,'G','Gnoll',1,2000,[],(2,4,1,Weapon_icon,'spear'),(3,Armor_icon,'leather armor',2)),
(20,9,4,2,9,60,4,0,4,'o','Orc',2,5000,[],(5,1,1,Weapon_icon,'mace'),(5,Armor_icon,'ringmail',10),(6,10,8,Shield_icon,'ceremonial shield',2),(' High Priest',('Orc High Priest shouts terrible curses.','You hear terrible curses.'))),
(10,3,6,8,1,20,8,0,1,'i','Lesser Imp',1,2000,['kai'],(2,1,4,Weapon_icon,'wand'),(0,Armor_icon,'',0)),
(60,20,6,4,12,10,20,0,4,'O','Ogre',1,30000,['huge'],(8,1,0,Weapon_icon,'cudgel',3,6,10,4),(9,Armor_icon,'shellmail',100)),
(20,8,12,30,2,5,8,0,1,'D','Crimson Demon',1,200000,['kai'],(0,2,7,Weapon_icon,'rod',3,2,0,12),(0,Armor_icon,'archmage robe',-1)),
(30,12,16,16,6,5,10,0,3,'I','Greater Imp',1,300000,['kai'],(1,4,4,Weapon_icon,'trident',3,4,0,4),(0,Armor_icon,'',0)),
(30,12,24,12,8,20,4,0,0,'v','Vampire',1,400000,['kai','vampirism','stealth'],(3,3,2,Weapon_icon,'vampric dagger',1,0,0,0,['vampirism']),(1,Armor_icon,'robe',0)),
(40,20,20,4,12,100,1,2,0,'p','Phantom',4,100000,['kai','illusion','stealth'],(3,3,3,Weapon_icon,'dagger'),(0,Armor_icon,'',0),(4,0,1,Shield_icon,'mirror shield',2,0,0,0,['illusion']),(' Killer',('You are being haunted.','You are being haunted.'))),
(50,30,8,4,6,20,20,0,0,'d','Demon Footman',1,100000,['kai','vampirism'],(3,3,3,Weapon_icon,'ivory trident'),(6,Armor_icon,'ivory scalemail',6,['vampirism']),(6,6,6,Shield_icon,'ivory shield',2,0,0,0,['vampirism'])),
(30,12,16,8,6,20,8,0,2,'j','Imp Torturer',1,30000,['kai'],(3,3,3,Weapon_icon,'ivory trident'),(0,Armor_icon,'',0)),
(30,12,12,12,12,20,10,0,0,'r','Holy Rabbit',0,30000,['purify','illusion','rabbit'],(0,0,0,Weapon_icon,''),(0,Armor_icon,'',0))
)
Effects_list=('healing potion','magic potion','poison potion','energetic potion','experience potion','brilliance potion','madness potion','regeneration potion','paralyze potion')
Titles_list=[]
RL_Potions=(6,3,5,4,2,3,3,3,1)
Weapon_types_list=('dagger','sword','mace','spear','wand')
Weapon_m_list=((2,2,2),(3,2,2),(5,1,1),(2,4,1),(2,1,4))
RL_Weapons=(2,8,6,3,3)
Armor_types_list=('ringmail','leather armor','robe','rags')
Armor_AC_ER_list=([5,10],[3,2],[1,0],[0,0])
RL_Armor=(1,4,3,0)
Food_types_list=('chunk of meat','bread ration','pizza')
Food_nutrition_list=(2,4,8)
RL_Food=(0,2,1)
VIT=20
Ability=('caster','lancer','berserker')
Cool_dict={'caster':['Now you possess legendary power of Caster! You can cast dark magic by pressing z!',0,0,5],'lancer':['Now you possess legendary power of Lancer! You can make far-reaching lunges by pressing x!',0,5,0],'berserker':['Now you possess legendary power of Berserker! You can crush your foes by pressing c!',5,0,0]}
Skill_list=['e','x','d','a','w','z','s']
Descriptions={'a':['Attacks all enemies around you.',4,0],'e':['Exhausts one enemy.',4,0],'x':['Run in straight line until you hit enemy or tire out.',4,0],'z':['Jump, damaging adjacent enemies.',12,0],'w':['Upgrades vitality and heals.',12,0],'d':['Swap yourself with selected enemy, damaging them.',12,0],'s':['Manage your abilities.',20,10]}
Coolness=3
Magic_value=4
TP_value=4
TP_cost=2
Magic_distance=6
XP=0
XP_base=500
familiar=[1,1,1]
lvl=1
Targets=[]
