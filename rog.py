import sys, os

def clearchat():
  if os.name == "posix":
    print ("\033[2J")
  elif os.name in ("nt", "dos", "ce"):
    os.system('CLS')
  else:
    print('\n' * 100)

def getcharkey():
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getwch()
    else:
        import termios
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    return result

def getkey():
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        try:
            result = getcharkey().encode()
        except:
            result = b''
    return result

try:
    from settings import *
except ModuleNotFoundError as err:
    print("Failed to import settings file \n"+str(err)+"\nCan't proceed executing programm.")
    getkey()
    exit()

try:
    from entities import *
except ModuleNotFoundError as err:
    print("Failed to import entities file \n"+str(err)+"\nCan't proceed executing programm.")
    getkey()
    exit()

try:
    from map import Maps
    def newstage():
        global x_size,y_size,Map,spawn_x,spawn_y,Messages,Mob_appear,Noob_Confetti,Mob_ungroup,Lead_c,RL_Mobs,ththyhyujy
        Map=Maps[Floor-1][0]
        x_size=Maps[Floor-1][1]
        y_size=Maps[Floor-1][2]
        Mob_appear=Maps[Floor-1][3]
        Noob_Confetti=Maps[Floor-1][4]
        Mob_ungroup=Maps[Floor-1][5]
        Lead_c=Maps[Floor-1][6]
        RL_Mobs=Maps[Floor-1][7]
        awares=0
        try:
            spawn_x,spawn_y=Maps[Floor-1][0].index('@')%x_size,Maps[Floor-1][0].index('@')//x_size
        except ValueError as err :
            Messages+=['Map file misses player, '+str(err)]
            spawn_x,spawn_y=x_size//2,y_size//2
        if Floor==5 and ththyhyujy==1:
            global player
            player.hp=-45
            ththyhyujy=4
    newstage()
except ModuleNotFoundError as err :
    Messages+=['Failed to import map file, '+str(err)]
    Map='.'*262144
    x_size=512
    y_size=512
    Mob_appear=500
    Noob_Confetti=500
    Mob_ungroup=12
    Lead_c=4
    RL_Mobs=(0,8,8,8,3,3,3,1,1,1)
    awares=0
    spawn_x,spawn_y=x_size//2,y_size//2
except NameError as err:
    Messages+=['Failed to import map, '+str(err)]
    Map='.'*262144
    x_size=512
    y_size=512
    Mob_appear=500
    Noob_Confetti=500
    Mob_ungroup=12
    Lead_c=4
    RL_Mobs=(0,8,8,8,3,3,3,1,1,1)
    awares=0
    spawn_x,spawn_y=x_size//2,y_size//2

try:
    from map import Presets
except ModuleNotFoundError as err:
    Presets=()
    Messages+=['Failed to import presets file, '+str(err)]
except NameError as err:
    Presets=()
    Messages+=['Failed to import presets, '+str(err)]

try:
    from boss import *
except ModuleNotFoundError as err:
    Messages+=['Failed to import boss file, '+str(err)]

Know_list=[0]*len(Effects_list)
for i in range(len(Effects_list)):
    Title=''
    for l in range(d(4)*d(2)+d(4)):
        Title+=chr(64+d(26))
    Titles_list+=[Title]

def un(x,y):
    return not (x,y) in X_Y_list
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
    if d(3) == 1:
        x.str+=1
    elif d(2) == 1:
        x.dex+=1
    else:
        x.int+=1
    if x.lvl%5 == 0:
        if x.__class__.__name__ == 'Me' and x.abilities != set(Ability):
            qyu=''
            for i in set(Ability) - x.abilities:
                qyu+='If '+x.name+' wants to become '+i.capitalize()+', type in '+i+'.\n'
            qyu+='If '+x.name+' wants to become stronger, type in anything else.'
            screen(0,0,qyu)
            a=input('')
            global Messages
            if a in Ability:
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
            mol=0
            qun=1
            for i in Ability:
                mol+=(i in x.abilities)*qun
                qun*=2
            if mol:
                x.skills=x.skills | {Skill_list[mol-1]}
        else:
            x.str+=Coolness
            x.dex+=Coolness
            x.int+=Coolness
    return x

def levelup():
    global player
    while XP >= XP_base*2**player.lvl:
        player=lvlup(player)

def outro(num):
    global Messages
    clearchat()
    print('Any key to advance epilogue')
    getkey()
    clearchat()
    if num==1:
        a=(player.name+' defeated all princes of Hell,',
        ' and therefore was prime candidate for next inauguration.',
        'But as they were alive,',
        ' they could not be official resident of Hell.',
        'As thus,','\choice','They decided to depart from Hell.','They decided to establish themselves as tyrant.')
    elif num==2:
        a=('Cerberus by the exit of Hell had eaten '+player.name+"'s soul.",'Bad End 4: Coward.')
    elif num==3:
        a=('Being feared by everyone,',
        ' '+player.name+' easily conquered Hell.',
        'Good End 2: Tyrant.')
    elif num==4:
        a=(player.name+' defeated all princes of Hell,',
        ' and therefore was prime candidate for next inauguration.',
        "Being converted to dead soul by Lucifer's exploded pride,",
        ' they could become king of Hell officially.',
        'Good End 3: Incorporeal King.')
    elif num==5:
        a=(player.name+' defeated all princes of Hell,',
        ' and therefore was prime candidate for next inauguration.',
        "Being a vampire,",
        ' they could become king of Hell officially.',
        'Good End 4: Undead King.')
    elif num==6:
        a=('Having been killed at holy place,',
        ' '+player.name+' have been sent to Purgatory.',
        'Unable to successfully atone,',
        ' they were sent to Hell.',
        'Bad End 2: Sinner.')
    elif num==7:
        a=('Having been killed at holy place,',
        ' '+player.name+' have been sent to Purgatory.',
        'After atoning successfully,',
        ' they were sent to Heaven.',
        'Good End 1: Innocent.')
    elif num==8:
        a=('After '+player.name+' killed all four hundred holy rabbits,',
        ' Special Archangel force was dispatched,',
        ' they were murdered in very gruesome way,',
        ' and sent to Hell afterwards.',
        'Bad End 3: Infidel.')
    elif num==9:
        a=('As '+player.name+' sees walls of a cathedral,',
        ' they turn to ashes.',
        'Bad End 1: Desecrator.')
    for i in range(len(a)):
        if a[i]=='\choice':
            for j in range(len(a)-i-1):
                print(chr(j+97)+" - "+a[j+i+1])
            b=-1
            while(not 0<=b<=len(a)-i-2):
                b=ord(getcharkey())-97
            outro(num+b+1)
            return
        else:
            print(a[i])
            Messages+=[a[i]]
            getkey()

def consume(ent,what):
    global Messages
    if what == 0:
        ent.hp=ent.VIT
        ent.bp=0
        ent.status['poison']=0
        ent.fp=ent.fp//2
        if ent.__class__.__name__=='Me':
            ent.sp+=4
    elif what == 1:
        ent.mp=(ent.int*ent.wield.intm*ER_divide)//(ER_divide+ent.ER)
        ent.fp=ent.fp//2
        ent.bp=ent.bp//2
    elif what == 2:
        if Know_list[what] is 0 and ent.__class__.__name__=='Me':
            ent.status['poison']+=10
        else:
            ent.status['viper']+=10
            Messages+=[ent.name+' applies '+Effects_list[what]+' to their weapon.']
            return None
    elif what == 3:
        ent.status['energy']+=10
    elif what == 4:
        ent=lvlup(ent)
    elif what == 5:
        ent.int+=10
        ent.status['brilliance']+=10
    elif what == 6:
        ent.status['madness']+=ent.int-1-ent.status['brilliance']
        ent.str+=ent.int-1-ent.status['brilliance']
        ent.int=1+ent.status['brilliance']
        ent.mp=0
    elif what == 7:
        ent.status['regeneration']+=10
        if ent.__class__.__name__=='Me':
            ent.sp+=4
    elif what == 8:
        ent.status['stun']+=4
        ent.bp=0
    Messages+=[ent.name+' drinks '+Effects_list[what]+'.']

def birth(x,y,mob):
    global Total_list,X_Y_list,awares
    if un(x,y) and Map[x+y*(x_size)] == '.':
        Total_list+=[Mob(mob,mob[11]//d(Lead_c))]
        awares+=mob[7]
        X_Y_list+=[(x,y)]
    for i in range(d(mob[5])//Mob_ungroup-1):
        x=max(min(x+d(5)-3,x_size-2),1)
        y=max(min(y+d(5)-3,y_size-2),1)
        if un(x,y) and Map[x+y*(x_size)] == '.':
            Total_list+=[Mob(mob)]
            awares+=mob[7]
            X_Y_list+=[(x,y)]

def generate():
    global Total_list,X_Y_list,spawn_x,spawn_y
    Total_list=[]
    X_Y_list=[]
    Uppu=0
    for l in range(y_size):
        for i in range(x_size):
            if Map[i+l*(x_size)] != '.':
                a=Map[i+l*(x_size)]
                if a is Wall_icon:
                    Total_list+=[Mob(Mob_list[0])]
                    X_Y_list+=[(i,l)]
                elif a is Boss_icon:
                    try:
                        Total_list+=[Boss(Floor+Uppu)]
                        Uppu+=1
                        X_Y_list+=[(i,l)]
                    except:
                        pass
                elif 97 <= ord(a.lower()) <= 122:
                    usl1=rl(RL_Weapons)
                    auto=()
                    for r in Presets:
                        if(r[9] is a):
                            auto=r
                    Total_list+=[Mob(auto,max(min(d(Floor)-d(Mob_ungroup),auto[11]),0))] if auto!=() else [Mob(Mob_list[usl3])]
                    X_Y_list+=[(i,l)]
                elif a is Potion_icon:
                    usl=rl(RL_Potions)
                    Total_list+=[Item(Potion_icon,usl,Titles_list[usl])]
                    X_Y_list+=[(i,l,0)]
                elif a is Food_icon:
                    usl=rl(RL_Food)
                    Total_list+=[Food(Food_nutrition_list[usl],Food_icon,Food_types_list[usl])]
                    X_Y_list+=[(i,l,0)]
                elif a is Weapon_icon:
                    usl=rl(RL_Weapons)
                    Total_list+=[Weapon(Weapon_m_list[usl][0],Weapon_m_list[usl][1],Weapon_m_list[usl][2],Weapon_icon,Weapon_types_list[usl])]
                    X_Y_list+=[(i,l,0)]
                elif a is Armor_icon:
                    usl=rl(RL_Armor)
                    Total_list+=[Armor(Armor_AC_ER_list[usl][0],Armor_icon,Armor_types_list[usl],Armor_AC_ER_list[usl][1])]
                    X_Y_list+=[(i,l,0)]
                elif a is Player_icon:
                    spawn_x=i
                    spawn_y=l
    for umlaut in range(Map.count('.')//Mob_appear):
        i=d(x_size)-1
        l=d(y_size)-1
        a=Map[i+l*(x_size)]
        b=rl(RL_Mobs)
        birth(i,l,Mob_list[b])
    for umlaut in range(Noob_Confetti):
        i=d(x_size)-1
        l=d(y_size)-1
        a=Map[i+l*(x_size)]
        if Map[i+l*(x_size)] == '.':
            if d(12)<=5:
                usl=rl(RL_Potions)
                Total_list+=[Item(Potion_icon,usl,Titles_list[usl])]
                X_Y_list+=[(i,l,0)]
            elif d(7)<=5:
                usl=rl(RL_Food)
                Total_list+=[Food(Food_nutrition_list[usl],Food_icon,Food_types_list[usl])]
                X_Y_list+=[(i,l,0)]
            elif d(2)==1:
                usl=rl(RL_Weapons)
                Total_list+=[Weapon(d(Weapon_m_list[usl][0]),d(Weapon_m_list[usl][1]),d(Weapon_m_list[usl][2]),Weapon_icon,Weapon_types_list[usl])]
                X_Y_list+=[(i,l,0)]
            else:
                usl=rl(RL_Armor)
                Total_list+=[Armor(Armor_AC_ER_list[usl][0],Armor_icon,Armor_types_list[usl],Armor_AC_ER_list[usl][1])]
                X_Y_list+=[(i,l,0)]

def attack(enA,enD):
    global Messages,ththyhyujy
    atk=d((enA.str+('illusion' in enA.doping)*enD.str//d(enD.int))*enA.wield.strm+d(enA.dex*enA.wield.dexm*2))*(enA.DV+DV_divide_a)//(2*DV_divide_a)
    if atk > enD.AC:
        enD.hp+=enD.AC-atk
        enD.bp+=atk*d(enA.int*enA.wield.intm)//d(enD.AC)
        Messages+=[enA.name+' hits '+enD.name+'.']
        if('viper' in enA.doping):
            enA.status['viper']-=1
            enD.status['poison']+=max(1,d(enA.dex)-d(enD.dex))
            Messages+=[enA.name+' poisons '+enD.name+'.']
        if('vampirism' in enA.doping):
            enA.hp=min(enA.VIT,atk-enD.AC)
            Messages+=[enA.name+' drains '+enD.name+"'s life force."]
            if(enD.__class__.__name__ == 'Me' and not ththyhyujy and (enA.wield==Weapon(1,1,1,Weapon_icon,''))):
                ththyhyujy=1
                enD.doping+=['kai','vampirism']
        if('death' in enA.doping):
            enD.hp=-45
            Messages+=['The curse of '+enA.wield.name+' kills '+enD.name+'.']
            if(enD.__class__.__name__ == 'Me'):
                ththyhyujy=2
        elif('purify' in enA.doping and 'kai' in enD.doping):
            enD.hp=-45
            Messages+=[enA.name+' purifies '+enD.name+'.']
            if enD.__class__.__name__ == 'Me':
                ththyhyujy==3
        if 'envy' in enD.doping:enD.Aenvy+=d(atk-enD.AC)
    else:
        if('parry' in enD.name):
            enA.status['stun']+=1
            Messages+=[enD.name+' parries '+enA.name+"'s hit!"]
        else:
            if 'gluttony' in enA.doping:
                if enA.hp==enA.VIT:
                    Messages+=[enA.name+' nibbles on '+enD.name+"'s armor."]
                    enD.wear.AC-=1
                    enD.AC-=1
                elif enA.hp>enA.VIT//2:
                    Messages+=[enA.name+' bites off a piece of '+enD.name+"'s armor."]
                    enD.wear.AC-=3
                    enD.AC-=3
                    enA.hp=min(enA.VIT,enA.hp+3)
                    enA.bp=0
                else:
                    Messages+=[enA.name+' devoires the most of '+enD.name+"'s armor."]
                    enD.wear.AC-=5
                    enD.AC-=5
                    enA.hp=min(enA.VIT,enA.hp+8)
                    enA.bp=0
                    enA.fp=0
            else:
                Messages+=[enD.name+' blocks '+enA.name+"'s hit."]
        if 'envy' in enA.doping:enA.Denvy+=d(atk)
    enA.fp+=2

def farattack(enA,enD):
    global Messages,ththyhyujy
    atk=d((enA.dex+('illusion' in enA.doping)*enD.dex//d(enD.int))*enA.wield.dexm+d(enA.dex*enA.wield.dexm*d(2)))*(enA.DV+DV_divide_f)//(4*DV_divide_f)
    if atk > enD.AC//2:
        enD.hp+=enD.AC//2-atk
        enD.bp+=atk*d(enA.dex*enA.wield.dexm)//d(enD.AC)
        Messages+=[enA.name+' hits '+enD.name+' from afar.']
        if('viper' in enA.doping):
            enA.status['viper']-=1
            enD.status['poison']+=max(1,d(enA.dex)-d(enD.dex))
            Messages+=[enA.name+' poisons '+enD.name+'.']
        if('vampirism' in enA.doping):
            enA.hp=min(enA.VIT,atk-enD.AC//2)
            Messages+=[enA.name+' drains '+enD.name+"'s life force."]
            if(enD.__class__.__name__ == 'Me' and not ththyhyujy and (enA.wield==Weapon(1,1,1,Weapon_icon,''))):
                ththyhyujy=1
                enD.doping+=['kai','vampirism']
        if('death' in enA.doping):
            enD.hp=-45
            Messages+=['The curse of '+enA.wield.name+' kills '+enD.name+'.']
            if(enD.__class__.__name__ == 'Me'):
                ththyhyujy=2
        elif('purify' in enA.doping and 'kai' in enD.doping):
            enD.hp=-45
            Messages+=[enA.name+' purifies '+enD.name+'.']
            if enD.__class__.__name__ == 'Me':
                ththyhyujy==3
        if 'envy' in enD.doping:enD.Aenvy+=d(atk-enD.AC//2)
    else:
        if('parry' in enD.name):
            enA.status['stun']+=2
            Messages+=[enD.name+' parries '+enA.name+"'s hit!"]
        else:
            if 'gluttony' in enA.doping:
                if enA.hp==enA.VIT:
                    Messages+=[enA.name+' nibbles on '+enD.name+"'s armor."]
                    enD.wear.AC-=1
                    enD.AC-=1
                elif enA.hp>enA.VIT//2:
                    Messages+=[enA.name+' bites off a piece of '+enD.name+"'s armor."]
                    enD.wear.AC-=3
                    enD.AC-=3
                    enA.hp=min(enA.VIT,enA.hp+3)
                    enA.bp=0
                else:
                    Messages+=[enA.name+' devoires the most of '+enD.name+"'s armor."]
                    enD.wear.AC-=5
                    enD.AC-=5
                    enA.hp=min(enA.VIT,enA.hp+8)
                    enA.bp=0
                    enA.fp=0
            else:
                Messages+=[enD.name+' blocks '+enA.name+"'s hit."]
        if 'envy' in enA.doping:enA.Denvy+=d(atk)
    enA.fp+=4

def rushattack(enA,enD):
    global Messages,ththyhyujy
    atk=d((enA.str+('illusion' in enA.doping)*enD.str//d(enD.int))*enA.wield.strm+d(enA.str*enA.wield.strm*d(2)))*(enA.DV+DV_divide_r)//(3*DV_divide_r)+enA.str*enA.wield.strm
    if atk > enD.AC and d(enA.dex+('illusion' in enA.doping)*enD.dex//d(enD.int)) > d(enD.dex):
        enD.hp+=enD.AC//2-atk
        enD.fp+=atk*d(enA.str*enA.wield.strm)//d(enD.AC)
        Messages+=[enA.name+' crushes '+enD.name+' mightily.']
        if('viper' in enA.doping):
            enA.status['viper']-=1
            enD.status['poison']+=max(1,d(enA.dex)-d(enD.dex))
            Messages+=[enA.name+' poisons '+enD.name+'.']
        if('vampirism' in enA.doping):
            enA.hp=min(enA.VIT,atk-enD.AC//2)
            Messages+=[enA.name+' drains '+enD.name+"'s life force."]
            if(enD.__class__.__name__ == 'Me' and not ththyhyujy and (enA.wield==Weapon(1,1,1,Weapon_icon,''))):
                ththyhyujy=1
                enD.doping+=['kai','vampirism']
        if('death' in enA.doping):
            enD.hp=-45
            Messages+=['The curse of '+enA.wield.name+' kills '+enD.name+'.']
            if(enD.__class__.__name__ == 'Me'):
                ththyhyujy=2
        elif('purify' in enA.doping and 'kai' in enD.doping):
            enD.hp=-45
            Messages+=[enA.name+' purifies '+enD.name+'.']
            if enD.__class__.__name__ == 'Me':
                ththyhyujy==3
                if enD.__class__.__name__ == 'Me':
                    ththyhyujy==3
        if 'envy' in enD.doping:enD.Aenvy+=d(atk-enD.AC//2)
    else:
        if(atk<=enD.AC):
            if('parry' in enD.name):
                enA.status['stun']+=4
                Messages+=[enD.name+' parries '+enA.name+"'s hit!"]
            else:
                if 'gluttony' in enA.doping:
                    if enA.hp==enA.VIT:
                        Messages+=[enA.name+' nibbles on '+enD.name+"'s armor."]
                        enD.wear.AC-=1
                        enD.AC-=1
                    elif enA.hp>enA.VIT//2:
                        Messages+=[enA.name+' bites off a piece of '+enD.name+"'s armor."]
                        enD.wear.AC-=3
                        enD.AC-=3
                        enA.hp=min(enA.VIT,enA.hp+3)
                        enA.bp=0
                    else:
                        Messages+=[enA.name+' devoires the most of '+enD.name+"'s armor."]
                        enD.wear.AC-=5
                        enD.AC-=5
                        enA.hp=min(enA.VIT,enA.hp+8)
                        enA.bp=0
                        enA.fp=0
                else:
                    Messages+=[enD.name+' blocks '+enA.name+"'s hit."]
        else:
            Messages+=[enA.name+' crushes floor near '+enD.name+"'s feet."]
        if 'envy' in enA.doping:enA.Denvy+=d(atk)
    enA.fp+=8

def magicattack(enA,enD):
    global Messages
    atk=d((enA.int+('illusion' in enA.doping)*enD.int//d(enD.int))*enA.wield.intm+d(enA.int*enA.wield.intm*d(2)))*MR_divide//(MR_divide+enD.ER)//2
    Messages+=[enA.name+' gestures at '+enD.name+'.']
    if atk > enD.AC//3+enD.mp:
        enD.hp+=enD.AC//3+enD.mp-atk
        enD.fp+=d(atk)
        enD.mp=0
        Messages+=['Pain surges through '+enD.name+"'s body."]
        if('purify' in enA.doping and 'kai' in enD.doping):
            enD.hp=-45
            Messages+=[enA.name+' purifies '+enD.name+'.']
            if enD.__class__.__name__ == 'Me':
                ththyhyujy==3
        if 'envy' in enD.doping:enD.Aenvy+=d(atk-enD.AC//3)
    else:
        if atk > enD.AC//3:
            enD.mp+=enD.AC//3-atk
            if 'envy' in enD.doping:enD.Aenvy+=d(atk-enD.AC//3)
        if 'envy' in enA.doping:enA.Denvy+=d(atk)
    enA.fp+=4
    enA.mp-=Magic_value

def prideattack(enA,enD):
    global Messages,ththyhyujy
    atk=d((enA.str+('illusion' in enA.doping)*enD.str//d(enD.int))+d(enA.dex*2))*(enA.DV+DV_divide_a)//(2*DV_divide_a)
    if atk > enD.AC:
        enD.hp+=enD.AC-atk
        enD.bp+=atk*d(enA.int)//d(enD.AC)
        Messages+=[enA.name+' hits '+enD.name+'.']
        if('viper' in enA.doping):
            enA.status['viper']-=1
            enD.status['poison']+=max(1,d(enA.dex)-d(enD.dex))
            Messages+=[enA.name+' poisons '+enD.name+'.']
        if('vampirism' in enA.doping):
            enA.hp=min(enA.VIT,atk-enD.AC)
            Messages+=[enA.name+' drains '+enD.name+"'s life force."]
            if(enD.__class__.__name__ == 'Me' and not ththyhyujy and (enA.wield==Weapon(1,1,1,Weapon_icon,''))):
                ththyhyujy=1
                enD.doping+=['kai','vampirism']
        if('death' in enA.doping):
            enD.hp=-45
            Messages+=['The curse of '+enA.wield.name+' kills '+enD.name+'.']
            if(enD.__class__.__name__ == 'Me'):
                ththyhyujy=2
        elif('purify' in enA.doping and 'kai' in enD.doping):
            enD.hp=-45
            Messages+=[enA.name+' purifies '+enD.name+'.']
            if enD.__class__.__name__ == 'Me':
                ththyhyujy==3
    else:
        enA.hp-=atk
        enA.bp+=atk*d(enA.int)
        Messages+=[enD.name+' blocks '+enA.name+"'s hit.",enA.name+' pride hurts.']
    enA.fp+=2

def steal(enA,enD):
    global Messages
    x=d(len(enD.inventory))-1
    Thing_in_question=enD.inventory[x]
    if Thing_in_question.__class__.__name__=='Armor' and Thing_in_question.AC>=enA.wear.AC and Thing_in_question.ER<=enA.wear.ER:
        enA.wear=Thing_in_question
        enA.drop+=[Thing_in_question]
        Messages+=[enA.name+' changes in '+Thing_in_question.name+' from '+player.name+"'s inventory!"]
        enA.fp+=8
    else:
        enA.inventory+=[enD.inventory[x]]
        Messages+=[enA.name+' acquires '+Thing_in_question.name+' from '+player.name+"'s inventory!"]
        enA.fp+=4
    enD.inventory.pop(x)

def stepaway(mob,n):
    global X_Y_list
    xx,yy=X_Y_list[n]
    if(un(xx-sig(player.x-xx),yy-sig(player.y-yy))):
        X_Y_list[n]=xx-sig(player.x-xx),yy-sig(player.y-yy)
        mob.fp+=1
    elif(disx(xx)>=disy(yy) and un(xx-sig(player.x-xx),yy)):
        X_Y_list[n]=xx-sig(player.x-xx),yy
        mob.fp+=1
    elif(disy(yy)>=disx(xx) and un(xx,yy-sig(player.y-yy))):
        X_Y_list[n]=xx,yy-sig(player.y-yy)
        mob.fp+=1
    elif(disx(xx)==0 and un(xx+1,yy-sig(player.y-yy))):
        X_Y_list[n]=xx+1,yy-sig(player.y-yy)
        mob.fp+=1
    elif(disx(xx)==0 and un(xx-1,yy-sig(player.y-yy))):
        X_Y_list[n]=xx-1,yy-sig(player.y-yy)
        mob.fp+=1
    elif(disy(yy)==0 and un(xx-sig(player.x-xx),yy+1)):
        X_Y_list[n]=xx-sig(player.x-xx),yy+1
        mob.fp+=1
    elif(disy(yy)==0 and un(xx-sig(player.x-xx),yy-1)):
        X_Y_list[n]=xx-sig(player.x-xx),yy-1
        mob.fp+=1
    else:
        mob.fp=max(mob.fp-mob.dex,0)
        if 'sloth' in mob.doping:mob.mp=min(mob.mp+mob.int,(mob.int*mob.wield.intm*ER_divide)//(ER_divide+mob.ER))

def stepahead(mob,n):
    global X_Y_list
    xx,yy=X_Y_list[n]
    if(un(xx+sig(player.x-xx),yy+sig(player.y-yy))):
        X_Y_list[n]=xx+sig(player.x-xx),yy+sig(player.y-yy)
        mob.fp+=1
    elif(disx(xx)>=disy(yy) and un(xx+sig(player.x-xx),yy)):
        X_Y_list[n]=xx+sig(player.x-xx),yy
        mob.fp+=1
    elif(disy(yy)>=disx(xx) and un(xx,yy+sig(player.y-yy))):
        X_Y_list[n]=xx,yy+sig(player.y-yy)
        mob.fp+=1
    elif(disx(xx)==0 and un(xx+1,yy+sig(player.y-yy))):
        X_Y_list[n]=xx+1,yy+sig(player.y-yy)
        mob.fp+=1
    elif(disx(xx)==0 and un(xx-1,yy+sig(player.y-yy))):
        X_Y_list[n]=xx-1,yy+sig(player.y-yy)
        mob.fp+=1
    elif(disy(yy)==0 and un(xx+sig(player.x-xx),yy+1)):
        X_Y_list[n]=xx+sig(player.x-xx),yy+1
        mob.fp+=1
    elif(disy(yy)==0 and un(xx+sig(player.x-xx),yy-1)):
        X_Y_list[n]=xx+sig(player.x-xx),yy-1
        mob.fp+=1
    else:
        mob.fp=max(mob.fp-mob.dex,0)
        if 'sloth' in mob.doping:mob.mp=min(mob.mp+mob.int,(mob.int*mob.wield.intm*ER_divide)//(ER_divide+mob.ER))

def death(n):
    global XP,Total_list,X_Y_list,awares
    ent=Total_list[n]
    XP+=ent.xp
    awares-=ent.aware
    for k in ent.drop:
        X_Y_list+=[X_Y_list[n]+tuple([0])]
        Total_list+=[k]
    for k in ent.inventory:
        X_Y_list+=[X_Y_list[n]+tuple([0])]
        Total_list+=[k]
    if Floor>4:
        global player
        if Floor==5:
            player.relics['Rabbit Feet'][0]+=1
        elif ent.lvl==99:
            player.relics['Stakes'][0]+=1
    Total_list.pop(n)
    X_Y_list.pop(n)

def find(lis,nam):
    for i in lis:
        if i.name==nam:
            return True
    return False

def fcount(lis,nam):
    c=0
    for i in lis:
        if i.name==nam:
            c+=1
    return c

def destroy(lis,nam):
    for i in range(len(lis)):
        if lis[i].name==nam:
            lis.pop(i)
            return
    raise ValueError

def move(n):
    global Total_list,X_Y_list,Messages,XP,player,awares,PT_awares
    if(len(X_Y_list[n])==2):
        mob=Total_list[n]
        if(mob.hp<=0):
            if ('wrath' in mob.doping):
                Messages+=[mob.name+' explodes!']
                atk=mob.VIT//4
                for i in ((-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)):
                    if(not un(X_Y_list[n][0]+i[0],X_Y_list[n][1]+i[1])):
                        enD=Total_list[X_Y_list.index((X_Y_list[n][0]+i[0],X_Y_list[n][1]+i[1]))]
                        enD.hp-=atk
                        enD.bp+=atk//4
                        enD.fp+=atk//4
                        enD.status['stun']+=d(enD.fp)//(d(enD.dex)+d(enD.AC))
                        Messages+=[enD.name+' gets caught up in explosion!']
                        Total_list[X_Y_list.index((X_Y_list[n][0]+i[0],X_Y_list[n][1]+i[1]))]=enD
                        if dis(X_Y_list[n][0]+i[0],X_Y_list[n][1]+i[1])==1:
                            player.hp-=atk
                            player.bp+=atk//4
                            player.fp+=atk//4
                            player.status['stun']+=d(player.fp)//(d(player.dex)+d(player.AC))
                            death(n)
                            levelup()
                            return
            else:
                Messages+=[player.name+' kills '+mob.name+'.']
                death(n)
                levelup()
                return
        elif(mob.type>=0):
            xx=X_Y_list[n][0]
            yy=X_Y_list[n][1]
            rol=1
            posx,posy=d(3)-2,d(3)-2
            if mob.status['poison']:
                mob.status['poison']-=1
                mob.hp-=mob.VIT//10
                mob.fp+=2
            if mob.status['energy']:
                mob.status['energy']-=1
                mob.bp*=2
                mob.fp=max(0,mob.fp-mob.dex)
            if mob.status['regeneration']:
                mob.status['regeneration']-=1
                mob.bp//=2
                mob.hp=min(mob.VIT,mob.hp+2)
            if mob.status['viper']:
                mob.status['viper']-=1
            if mob.status['madness']:
                mob.status['madness']-=1
                mob.str-=1
                mob.int+=1
                mob.mp=0
            if mob.status['brilliance']:
                mob.status['brilliance']-=1
                mob.int-=1
                mob.mp=min(mob.mp+mob.int,(mob.int*mob.wield.intm*ER_divide)//(ER_divide+mob.ER))
            if 'wrath' in mob.doping:
                mob.str=mob.Bstr*mob.VIT//mob.hp
            if mob.status['poison']>P_value:
                mob.status['poison']//=2
                mob.fp+=4
                Messages+=[mob.name+' throws up.']
            elif mob.status['stun']:
                mob.AC=mob.BAC+mob.wear.AC
                if 'parry' in mob.doping:
                    mob.doping.remove('parry')
                    mob.doping.append('p')
                if mob.lvl<99:
                    mob.MR=0
                    if mob.status['stun']==1:
                        mob.MR+=mob.shield.MR
                if mob.status['stun']==1:
                    mob.AC+=mob.shield.AC
                    if 'p' in mob.doping:
                        mob.doping.remove('p')
                        mob.doping.append('parry')
                mob.status['stun']-=1
            elif mob.status['madness'] and (not un(xx+posx,yy+posy) or (xx+posx==player.x and yy+posy==player.y)):
                if not un(xx+posx,yy+posy) and not (posx==0 and posy==0):
                    rushattack(mob,Total_list[X_Y_list.index((xx+posx,yy+posy))])
                if xx+posx==player.x and yy+posy==player.y:
                    rushattack(mob,player)
            elif(mob.fp>d(FP_bonus+mob.dex-mob.ER*SR_divide//(SR_divide+mob.str))):
                mob.fp=max(mob.fp-mob.dex,0)
                if 'sloth' in mob.doping:mob.mp=min(mob.mp+mob.int,(mob.int*mob.wield.intm*ER_divide)//(ER_divide+mob.ER))
            elif mob.aware==0:
                if dis(xx,yy) < 7 + hey + mob.VIT-mob.hp:
                    mob.aware=1
                    awares+=1
                    if mob.leader==1:
                        if not 'stealth' in mob.doping:
                            PT_awares+=mob.shout*2
                            Messages+=[mob.name+' shouts vigorously!'] if dis(xx,yy)<9 else [player.name+' hears a vigorous shout!']
                    elif mob.leader:
                        PT_awares+=mob.shout*(1+mob.leader)
                        Messages+=[mob.catchphrase[0]] if dis(xx,yy)<9 else [mob.catchphrase[1]]
                    elif not 'stealth' in mob.doping:
                        PT_awares+=mob.shout
                        Messages+=[mob.name+' shouts!'] if dis(xx,yy)<9 else [player.name+' hears a shout!']
            elif mob.aware==1 and dis(xx,yy) > 7 + hey + mob.VIT-mob.hp:
                awares-=1
                mob.aware=0
            elif(find(mob.inventory,'healing potion') and mob.hp-mob.bp<mob.VIT*min(16,8+fcount(mob.inventory,'healing potion'))//16):
                consume(mob,0)
                destroy(mob.inventory,'healing potion')
            elif(find(mob.inventory,'magic potion') and mob.mp<(mob.int*mob.wield.intm*ER_divide)//(ER_divide+mob.ER)*min(8,fcount(mob.inventory,'magic potion'))//8):
                consume(mob,1)
                destroy(mob.inventory,'magic potion')
            elif(find(mob.inventory,'poison potion') and dis(xx,yy)<=mob.type//2%2+2 and mob.status['poison']<fcount(mob.inventory,'poison potion')):
                consume(mob,2)
                destroy(mob.inventory,'poison potion')
            elif(find(mob.inventory,'energetic potion') and mob.fp>mob.dex*max(0,8-fcount(mob.inventory,'energetic potion'))//8):
                consume(mob,3)
                destroy(mob.inventory,'energetic potion')
            elif(find(mob.inventory,'experience potion')):
                consume(mob,4)
                destroy(mob.inventory,'experience potion')
            elif(find(mob.inventory,'brilliance potion') and mob.type%2==1 and dis(xx,yy)<=Magic_distance+1 and mob.status['brilliance']<fcount(mob.inventory,'brilliance potion')):
                consume(mob,5)
                destroy(mob.inventory,'brilliance potion')
            elif(find(mob.inventory,'madness potion') and dis(xx,yy)==2 and mob.status['madness']<fcount(mob.inventory,'madness potion')):
                consume(mob,6)
                destroy(mob.inventory,'madness potion')
            elif(find(mob.inventory,'regeneration potion') and mob.hp-mob.bp<mob.VIT*min(16,8+fcount(mob.inventory,'regeneration potion'))//16 and mob.hp-mob.bp>0):
                consume(mob,7)
                destroy(mob.inventory,'regeneration potion')
            elif(find(mob.inventory,'paralyze potion') and mob.hp-mob.bp<=0):
                consume(mob,8)
                destroy(mob.inventory,'paralyze potion')
            elif ('envy' in mob.doping) and (d(mob.Aenvy)>=NV_value or d(mob.Denvy)>=NV_value):
                if mob.Denvy>=mob.Aenvy:
                    mob.AC+=d(player.AC-player.BAC)
                    mob.VIT+=d(player.hp)
                    mob.hp=mob.VIT
                    Messages+=[mob.name+' is envious of '+player.name+"'s defense!"]
                    mob.Denvy-=NV_value
                else:
                    mob.wield.strm+=d(player.wield.strm)
                    mob.wield.dexm+=d(player.wield.dexm)
                    mob.wield.intm+=d(player.wield.intm)
                    Messages+=[mob.name+' is envious of '+player.name+"'s offense!"]
                    mob.Aenvy-=NV_value
            elif dis(xx,yy)==1 and ('pride' in mob.doping):
                prideattack(mob,player)
            elif dis(xx,yy)==1 and ('greed' in mob.doping) and player.inventory!=[]:
                steal(mob,player)
                if d(mob.fp)<d(mob.dex):
                    stepaway(mob,n)
            elif(dis(xx,yy)==2 and mob.type//2%2==1):
                farattack(mob,player)
                rol=0
            elif(mob.type%2==1 and mob.mp>=Magic_value and dis(xx,yy)<=Magic_distance):
                magicattack(mob,player)
                rol=0
            elif(dis(xx,yy)==1 and mob.type//4%2==1):
                rushattack(mob,player)
                rol=0
            elif 'teleport' in mob.doping and mob.type%2==1 and dis(xx,yy)<Magic_distance:
                if dis(xx,yy)<3 and (mob.fp>=TP_value or mob.hp-mob.bp<mob.VIT):
                    for i in sorted(((j,-Magic_value) for j in range(-Magic_value,Magic_value+1))+((j,Magic_value) for j in range(-Magic_value,Magic_value+1))+((Magic_value,j) for j in range(-Magic_value,Magic_value+1))+((-Magic_value,j) for j in range(-Magic_value,Magic_value+1)),key= lambda x: d(1000)):
                        if(un(X_Y_list[n][0]+i[0],X_Y_list[n][1]+i[1])):
                            mob.fp+=Magic_value*TP_cost
                            X_Y_list[n]=X_Y_list[n][0]+i[0],X_Y_list[n][1]+i[1]
                            Messages+=[mob.name+' teleports!']
                            break
                elif mob.type//2%2==0:
                    for i in sorted(((-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)),key= lambda x: d(100)):
                        if(un(player.x+i[0],player.y+i[1])):
                            mob.fp+=max(abs(player.x+i[0]-X_Y_list[n][0]),abs(player.y+i[1]-X_Y_list[n][1]))*TP_cost
                            X_Y_list[n]=player.x+i[0],player.y+i[1]
                            Messages+=[mob.name+' teleports!']
                            break
                else:
                    for i in sorted(((-2,2),(-1,2),(0,2),(1,2),(2,2),(2,1),(2,0),(2,-1),(2,-2),(1,-2),(0,-2),(-1,-2),(-2,-2),(-2,-1),(-2,0),(-2,1)),key= lambda x: d(100)):
                        if(un(player.x+i[0],player.y+i[1])):
                            mob.fp+=max(abs(player.x+i[0]-X_Y_list[n][0]),abs(player.y+i[1]-X_Y_list[n][1]))*TP_cost
                            X_Y_list[n]=player.x+i[0],player.y+i[1]
                            Messages+=[mob.name+' teleports!']
                            break
            elif((mob.fp>=mob.dex and mob.type%2==1) or (mob.fp>=d(mob.dex) and mob.type//2%2==1)):
                mob.fp=max(mob.fp-mob.dex,0)
                if 'sloth' in mob.doping:mob.mp=min(mob.mp+mob.int,(mob.int*mob.wield.intm*ER_divide)//(ER_divide+mob.ER))
            elif (mob.type==1 and dis(xx,yy)<=4) or (mob.type//2%2==1 and dis(xx,yy)==1):
                stepaway(mob,n)
            elif(dis(xx,yy)==1):
                attack(mob,player)
            elif dis(xx,yy) < safe - mob.lvl - hey - (mob.VIT-mob.hp):
                PT_awares+=mob.shout
                Messages+=[mob.name+' shouts!'] if dis(xx,yy)<9 else [player.name+' hears a shout!']
            elif not 'sloth' in mob.doping:
                if 'rabbit' in mob.doping:
                    for i in sorted(((-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)),key= lambda x: d(100)):
                        if(not un(player.x+i[0],player.y+i[1])):
                            X_Y_list[X_Y_list.index((player.x+i[0],player.y+i[1]))],X_Y_list[n]=X_Y_list[n],X_Y_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]
                            Messages+=[mob.name+' swaps with a nearby rabbit!']
                            break
                else:
                    stepahead(mob,n)
            else:
                mob.fp=max(mob.fp-mob.dex,0)
                mob.mp=min(mob.mp+mob.int,(mob.int*mob.wield.intm*ER_divide)//(ER_divide+mob.ER))
            if('roller-skates' in mob.doping and d(mob.dex)>d(mob.fp)):
                if(rol and dis(xx,yy)==2 and mob.type//2%2==1):
                    farattack(mob,player)
                elif(rol and mob.type%2==1 and mob.mp>=Magic_value and dis(xx,yy)<=Magic_distance):
                    magicattack(mob,player)
                elif(rol and dis(xx,yy)==1 and mob.type//4%2==1):
                    rushattack(mob,player)
                elif(rol and dis(xx,yy)==1):
                    attack(mob,player)
                elif(dis(xx,yy)==1):
                    stepaway(mob,n)
                else:
                    stepahead(mob,n)
            if 'lust' in mob.doping:
                mob.hp=min(mob.VIT,mob.hp+mob.bp+player.bp)
            else:
                mob.hp-=mob.bp
            mob.bp=mob.bp*2//3
            if mob.hp-mob.bp<=0 and ('pride' in mob.doping):
                mob.doping.remove('pride')
                mob.hp=1
                mob.bp=1
                mob.fp=0
                mob.shield=Weapon(0,0,0,Shield_icon,'',2)
                mob.DV=1
                mob.doping+=['wrath']
                Messages+=[mob.name+"'s pride is destroyed!"]
                X_Y_list+=[X_Y_list[n]+tuple([0])]
                Total_list+=[Weapon(6,0,6,Shield_icon,'ebony shield',2,0,0,0,['vampirism'])]
            if(d(mob.VIT-mob.bp)>0 and mob.hp<mob.VIT):
                mob.hp+=1
            if(d(mob.VIT+mob.int*mob.wield.intm-mob.mp)>mob.VIT-mob.int*mob.wield.intm and mob.mp<(mob.int*mob.wield.intm*ER_divide)//(ER_divide+mob.ER)):
                mob.mp+=1
            Total_list[n]=mob

def help():
    global Messages
    Messages+=['']
    Messages+=['r t y']
    Messages+=['f   h  move/attack.']
    Messages+=['v b n']
    Messages+=['u      shout for attention.']
    Messages+=['j      to throw up.']
    Messages+=['.      rest one turn.']
    Messages+=['g      get item on '+player.name+"'s tile."]
    Messages+=['i      use item in '+player.name+"'s inventory."]
    Messages+=['d      destroy item in inventory.']
    Messages+=['s      sort'+player.name+"'s inventory."]
    Messages+=['a      use ability.']
    Messages+=['Esc    exit.']
    Messages+=['?      help.']
    Messages+=['!      abbreviations in stats.']
    Messages+=['#      icons list.']
    Messages+=['*      view transcript.']
    Messages+=['@      enemy description.']
    Messages+=['Space  toggle dual wield.']
    Messages+=['>      ascend.']

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
    Messages+=['MR     magical resistance from wielded shield.']

def icons():
    global Messages
    Messages+=['']
    Messages+=[Player_icon+' '*6+'player.']
    Messages+=[Potion_icon+' '*6+'potion.']
    Messages+=[Weapon_icon+' '*6+'weapon.']
    Messages+=[Shield_icon+' '*6+'shield.']
    Messages+=[Armor_icon+' '*6+'armor.']
    Messages+=[Food_icon+' '*6+'food.']
    Messages+=[Wall_icon+' '*6+'wall.']
    Messages+=[Boss_icon+' '*6+'boss.']
    Messages+=['Letters represent enemies.']

def story():
    clearchat()
    print(*Messages[-transcript*3:],sep='\n')
    print('Press any key to continue.')

def xp():
    global Messages
    for i in Mob_list:
        zoo=Mob(i)
        Messages+=[zoo.icon+' '+zoo.name+(15-len(zoo.name))*' '+str(zoo.xp)+(8-len(str(zoo.xp)))*' '+str(i)]
    for i in range(4):
        zoo=Boss(i+1)
        Messages+=[zoo.icon+' '+zoo.name+(15-len(zoo.name))*' '+str(zoo.xp)]

def answer(nam):
    if 'Goblin' in nam:
        a='Small, pretty agile and ugly.'
    elif 'Kobold' in nam:
        a='Ugly, clumsy and stupid.'
    elif 'Gnoll' in nam:
        a='Agile, very ugly and can attack from 2 tiles away.'
    elif 'Orc' in nam:
        a='Strong, ugly and can crush from 1 tile away.'
    elif 'Lesser Imp' in nam:
        a='Smart, unholy and can cast magic from '+str(Magic_distance)+' tiles away.'
    elif 'Ogre' in nam:
        a='Big, strong and can crush from 1 tile away.'
    elif 'Crimson Demon' in nam:
        a='Smart, unholy and can cast magic from '+str(Magic_distance)+' tiles away.'
    elif 'Greater Imp' in nam:
        a='Unholy, can attack from 2 tiles away and can cast magic from '+str(Magic_distance)+' tiles away.'
    elif 'Vampire' in nam:
        a='Stealthy, unholy and drains on successfull attacks.'
    elif 'Phantom' in nam:
        a='Stealthy, unholy and illusional.'
    elif 'Imp Torturer' in nam:
        a='Unholy, sadistic and can attack from 2 tiles away.'
    elif 'Holy Rabbit' in nam:
        a='Holy, very cute and illusional.'
    elif 'Wall' in nam:
        a='Extremely dangerous, huge and dormant.'
    elif 'World Ender' in nam:
        a='Huge, can crush from 1 tile away and can cast magic from '+str(Magic_distance)+' tiles away.'
    elif 'Midorime' in nam:
        a='Stealthy, very agile and beautiful.\nHer sword can kill from one wound.'
    elif 'Kill-Shot' in nam:
        a='Unholy, very agile and drains on successfull attacks.\nHer sword purifies unholy beings.'
    elif 'Shounin Bat' in nam:
        a='Unholy, uses roller-skates to move around and can crush from 1 tile away.\nHis bat is illusional.'
    elif 'Dwarf Rabbit' in nam:
        a='Very cute, can crush from 1 tile away and can cast magic from '+str(Magic_distance)+' tiles away.\nHis shellmail is holy.\nHe can use his cudgel to parry attacks.'
    elif 'Lucifer' in nam:
        a='Condescending, unholy and very sturdy.\nAll his equipment exudes dark aura.'
    elif 'Belphegor' in nam:
        a='Lazy, extremely unathletic  and can cast magic from '+str(Magic_distance)+' tiles away.\nAll his equipment exudes dark aura.\nHis wand is illusional.'
    elif 'Mammon' in nam:
        a='Greedy, drains on successfull attacks and can cast magic from '+str(Magic_distance)+' tiles away.\nHis wand can teleport him.'
    elif 'Satan' in nam:
        a='Easily angered, huge and can crush from 1 tile away.\nAll his equipment exudes dark aura.'
    elif 'Leviatan' in nam:
        a='Has inferiority complex, unholy and dirty.\nAll his equipment exudes dark aura.'
    elif 'Beelzebub' in nam:
        a='Has bottomless stomach, strong and huge.\nAll his equipment exudes dark aura.'
    elif 'Asmodeus' in nam:
        a='Disgusting, unholy and strong.\nAll his equipment exudes dark aura.'
    if 'Leader' in nam:
        a+='\nThis one looks more dangerous than others of his kind.'
    elif 'High Priest' in nam:
        a+='\nThis one has numerous amulets around his neck.'
    elif 'Killer' in nam:
        a+="\nThis one's eyes look scary."
    return a

def asking():
    global Messages
    a=b''
    dx=0
    dy=0
    dt=-1
    while(a!=b'\r' and a!=b'\n' and a!=b'\x1b' and a!=b'g'):
        if(isdir(a)):
            dx+=direction(a)[0]
            dy+=direction(a)[1]
        if(abs(dx)>8):
            dx=sig(dx)*8
        if(abs(dy)>8):
            dy=sig(dy)*8
        if show[8-dy][8+dx] in {'.',Potion_icon,Weapon_icon,Shield_icon,Food_icon,Armor_icon,Magic_icon,Player_icon}:
            screen(dx,dy,'    r t y\nUse f   h to navigate, Esc, Enter or g to stop.\n    v b n')
        else:
            mob=Total_list[X_Y_list.index((player.x+dx,player.y+dy))]
            screen(dx,dy,mob.name+'\nHP:{:<7}  MP:{:<7}  STR:{:<6}  DEX:{:<6}  INT:{:<6}\nAC:{:<7}  ER:{:<7}  MR:{:<7}\n'.format(mob.VIT,(mob.int*mob.wield.intm*ER_divide)//(ER_divide+mob.ER),mob.str,mob.dex,mob.int,mob.AC,mob.ER,mob.MR)+answer(mob.name))
        a=getkey()

def direction(a):
    if a==b'r':
        return -1,1
    elif a==b't':
        return 0,1
    elif a==b'y':
        return 1,1
    elif a==b'h':
        return 1,0
    elif a==b'n':
        return 1,-1
    elif a==b'b':
        return 0,-1
    elif a==b'v':
        return -1,-1
    elif a==b'f':
        return -1,0
    else:
        return ValueError

def isdir(a):
    return a in (b'r',b't',b'y',b'h',b'n',b'b',b'v',b'f')

def casting():
    global player,Messages
    a=b''
    dx=0
    dy=0
    dt=-1
    while(a!=b'\r' and a!=b'\n' and a!=b'\x1b' and a!=b'g'):
        if(isdir(a)):
            dx+=direction(a)[0]
            dy+=direction(a)[1]
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
        a=getkey()
    if(a==b'\x1b'):
        return 1
    else:
        if(show[8-dy][8+dx]==Magic_icon or show[8-dy][8+dx]==Player_icon):
            if('teleport' in player.doping and player.DV==1):
                if(player.mp>=max(abs(dx),abs(dy))*TP_cost):
                    player.x+=dx
                    player.y+=dy
                    player.mp-=max(abs(dx),abs(dy))*TP_cost
                    Messages+=['Player teleports.']
                    if(not un(player.x,player.y)):
                        Total_list[X_Y_list.index((player.x,player.y))].hp=-45
                        Messages+=[player.name+' disintegrates something.']
                    return 0
                else:
                    Messages+=['Not enough MP.']
                    return 1
            else:
                Messages+=['Invalid target.']
                return 1
        else:
            if(player.mp>=Magic_value):
                magicattack(player,Total_list[X_Y_list.index((player.x+dx,player.y+dy))])
                return 0
            else:
                Messages+=['Not enough MP.']
                return 1

def lancing():
    global player,Messages
    a=b''
    dx=0
    dy=0
    while(a!=b'\r' and a!=b'\n' and a!=b'\x1b' and a!=b'g'):
        if(isdir(a)):
            dx+=direction(a)[0]
            dy+=direction(a)[1]
        if(abs(dx)>2):
            dx=sig(dx)*2
        if(abs(dy)>2):
            dy=sig(dy)*2
        if(abs(dy)<2 and abs(dx)<2):
            dy=dy*2
            dx=dx*2
        screen(dx,dy,'    r t y\nUse f   h to navigate, Esc to abort, Enter or g to confirm target.\n    v b n')
        a=getkey()
    if(a==b'\x1b'):
        return 1
    else:
        if(show[8-dy][8+dx]==Magic_icon or show[8-dy][8+dx]==Player_icon):
            Messages+=['Invalid target.']
            return 1
        else:
            farattack(player,Total_list[X_Y_list.index((player.x+dx,player.y+dy))])
            return 0

def berserking():
    global player,Messages
    a=b''
    dx=0
    dy=0
    while(a!=b'\r' and a!=b'\n' and a!=b'\x1b' and a!=b'g'):
        if(isdir(a)):
            dx,dy=direction(a)
        if(abs(dx)>1):
            dx=sig(dx)
        if(abs(dy)>1):
            dy=sig(dy)
        screen(dx,dy,'    r t y\nUse f   h to navigate, Esc to abort, Enter or g to confirm target.\n    v b n')
        a=getkey()
    if(a==b'\x1b'):
        return 1
    else:
        if(show[8-dy][8+dx]==Magic_icon or show[8-dy][8+dx]==Player_icon):
            Messages+=['Invalid target.']
            return 1
        else:
            rushattack(player,Total_list[X_Y_list.index((player.x+dx,player.y+dy))])
            return 0

def change_weapon(a):
    global player,familiar,Messages
    if(player.inventory[a].dual%2==1):
        player.inventory+=[player.wield]
        Messages+=[player.name+' unwields '+player.wield.name+'.']
        player.wield=player.inventory[a]
        Messages+=[player.name+' wields '+player.wield.name+'.']
        if player.wield.dual==3:
            player.DV=1
        familiar=[0,0,0]
        if 'vampirism' in player.wield.doping:
            Messages+=[player.name+' feels demonic power emanating from their weapon.']
        if 'purify' in player.wield.doping:
            Messages+=[player.name+' feels holy power emanating from their weapon.']
        if 'death' in player.wield.doping:
            Messages+=[player.name+' feels cursed power emanating from their weapon.']
        if 'teleport' in player.wield.doping:
            Messages+=[player.name+' feels translocational power emanating from their weapon.']
        if 'illusion' in player.wield.doping:
            Messages+=[player.name+"'s weapon appears blurry."]
        if 'parry' in player.wield.doping:
            Messages+=[player.name+"'s weapon appears suitable for parrying."]
        player.status['viper']=0
    else:
        player.inventory+=[player.shield]
        Messages+=[player.name+' unwields '+player.shield.name+'.']
        player.shield=player.inventory[a]
        Messages+=[player.name+' wields '+player.shield.name+'.']
        if 'vampirism' in player.wield.doping:
            Messages+=[player.name+' feels demonic power emanating from their shield.']
        if 'purify' in player.wield.doping:
            Messages+=[player.name+' feels holy power emanating from their shield.']
        if 'death' in player.wield.doping:
            Messages+=[player.name+' feels cursed power emanating from their shield.']
        if 'teleport' in player.wield.doping:
            Messages+=[player.name+' feels translocational power emanating from their shield.']
        if 'illusion' in player.wield.doping:
            Messages+=[player.name+"'s shield appears blurry."]
    shield_recalculate()

def change_armor(a):
    global player,Messages
    player.AC-=player.wear.AC
    player.ER-=player.wear.ER
    Messages+=[player.name+' unequips '+player.wear.name+'.']
    player.inventory+=[player.wear]
    player.wear=player.inventory[a]
    player.AC+=player.wear.AC
    player.ER+=player.wear.ER
    player.mp=min(player.mp,(player.int*player.wield.intm*ER_divide)//(ER_divide+player.ER))
    Messages+=[player.name+' equips '+player.wear.name+'.']
    if 'vampirism' in player.wield.doping:
        Messages+=[player.name+' feels demonic power emanating from their armor.']
    if 'purify' in player.wield.doping:
        Messages+=[player.name+' feels holy power emanating from their armor.']
    if 'death' in player.wield.doping:
        Messages+=[player.name+' feels cursed power emanating from their armor.']
    if 'teleport' in player.wield.doping:
        Messages+=[player.name+' feels translocational power emanating from their armor.']
    if 'illusion' in player.wield.doping:
        Messages+=[player.name+"'s armor appears blurry."]

def knowledge(what):
    global Know_list
    if(Know_list[what]==0):
        Know_list[what]=Titles_list[what]
        for i in player.inventory:
            if(i.name is Titles_list[what]):
                i.name=Effects_list[what]

def item_using():
    global player,Messages
    if(len(player.inventory)>0):
        clearchat()
        for i in range(len(player.inventory)):
            print(chr(i+97)+" - "+player.inventory[i].name)
        a=ord(getcharkey())-97
        if(0<=a<=len(player.inventory)-1):
            if(player.inventory[a].__class__.__name__=='Weapon'):
                change_weapon(a)
            elif(player.inventory[a].__class__.__name__=='Armor'):
                change_armor(a)
            elif(player.inventory[a].__class__.__name__=='Food'):
                player.sp=min(player.VIT,player.sp+player.inventory[a].nutrition)
                Messages+=[player.name+' eats '+player.inventory[a].name+'.']
            elif(player.inventory[a].__class__.__name__=='Item'):
                what=player.inventory[a].number
                consume(player,what)
                knowledge(what)
            else:
                Messages+=[player.name+' uses unrecognised item.']
            player.inventory.pop(a)
            return 0
        else:
            if(a!=-70):
                Messages+=['No such item.']
            return 1
    else:
        Messages+=[player.name+"'s inventory is empty."]
        return 1

def item_destruct():
    global player,Messages
    if(len(player.inventory)>0):
        clearchat()
        for i in range(len(player.inventory)):
            print(chr(i+97)+" - "+player.inventory[i].name)
        a=ord(getcharkey())-97
        if(0<=a<=len(player.inventory)-1):
            Messages+=['Player destroys '+player.inventory[a].name+'.']
            player.inventory.pop(a)
            return 0
        else:
            if(a!=-70):
                Messages+=['No such item.']
            return 1
    else:
        Messages+=[player.name+"'s inventory is empty."]
        return 1

def item_grab():
    global player,Total_list,X_Y_list,Messages
    positioned=(player.x,player.y,0)
    if(positioned in X_Y_list):
        if(len(player.inventory)<26):
            index=X_Y_list.index(positioned)
            player.inventory+=[Total_list[index]]
            Total_list.pop(index)
            X_Y_list.pop(index)
            if(player.inventory[-1].name in Know_list):
                player.inventory[-1].name=Effects_list[player.inventory[-1].number]
            elif(player.inventory[-1].name in Effects_list):
                knowledge(Effects_list.index(player.inventory[-1].name))
            Messages+=[player.name+' picks up '+player.inventory[-1].name+'.']
            return 0
        else:
            Messages+=[player.name+"'s inventory is already full."]
            return 1
    else:
        Messages+=['There is nothing here.']
        return 1

def update_state():
    global player,familiar,Messages
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
    player.sp=min(player.sp,player.VIT)
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

def DoVi():
    global player,Messages
    if(player.wield.dual==3):
        Messages+=['''Can't wield '''+player.wield.name+''' in one hand.''']
        return 1
    else:
        player.DV=1-player.DV
        Messages+=[player.name+' wields his '+player.wield.name+' in both hands.' if player.DV else player.name+' wields his '+player.wield.name+' in right hand.']
        shield_recalculate()
        return 0

def clockattack(start=0,wise=1):
    global Messages,Total_list,player
    atk=d(player.str*player.wield.strm)*(player.DV+2)//5
    for i in ((-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0))[start-1-(wise==1):start+7-(wise==1)][::wise]:
        if(not un(player.x-i[0],player.y-i[1])):
            enD=Total_list[X_Y_list.index((player.x-i[0],player.y-i[1]))]
            if(atk>enD.AC):
                atk=atk-enD.AC//4
                enD.hp-=atk
                enD.fp+=atk//3
                Messages+=[player.name+' hits '+enD.name+'.']
                player.fp+=2
                if('viper' in enA.doping):
                    enA.status['viper']-=1
                    enD.status['poison']+=max(1,d(enA.dex)-d(enD.dex))
                    Messages+=[enA.name+' poisons '+enD.name+'.']
                if('vampirism' in player.doping):
                    player.hp=min(player.VIT,atk)
                    Messages+=[player.name+' drains '+enD.name+"'s life force."]
                if('death' in player.doping):
                    enD.hp=-45
                    Messages+=['The curse of '+player.wield.name+' kills '+enD.name+'.']
                elif('purify' in player.doping and 'kai' in enD.doping):
                    enD.hp=-45
                    Messages+=[player.name+' purifies '+enD.name+'.']
            else:
                if('parry' in enD.name):
                    enD.fp+=atk//4
                    atk=atk//3
                    enA.status['stun']+=2
                    Messages+=[enD.name+' parries '+enA.name+"'s hit!"]
                else:
                    enD.fp+=atk//2
                    atk=atk*3//5
                    Messages+=[enD.name+' blocks '+player.name+"'s hit."]
                player.fp+=4
            Total_list[X_Y_list.index((player.x-i[0],player.y-i[1]))]=enD

def runattack(i=(1,0)):
    global Messages,Total_list,player
    ran=0
    while un(player.x+i[0],player.y+i[1]) and d(player.fp)<player.dex:
        player.x+=i[0]
        player.y+=i[1]
        player.fp+=2
        ran+=1
    if not un(player.x+i[0],player.y+i[1]):
        enD=Total_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]
        atk=d(player.dex*player.wield.dexm)*(player.DV+1)*(2+min(ran,4))//max(6,player.fp)//2
        if atk > enD.AC//4:
            enD.hp+=enD.AC//4-atk
            enD.bp+=atk*player.dex*player.wield.dexm//d(enD.AC)
            Messages+=[player.name+' lunges at '+enD.name+'.']
            if('viper' in enA.doping):
                enA.status['viper']-=1
                enD.status['poison']+=max(1,d(enA.dex)-d(enD.dex))
                Messages+=[enA.name+' poisons '+enD.name+'.']
            if('vampirism' in player.doping):
                player.hp=min(player.VIT,atk-enD.AC//4)
                Messages+=[player.name+' drains '+enD.name+"'s life force."]
            if('death' in player.doping):
                enD.hp=-45
                Messages+=['The curse of '+player.wield.name+' kills '+enD.name+'.']
            elif('purify' in player.doping and 'kai' in enD.doping):
                enD.hp=-45
                Messages+=[player.name+' purifies '+enD.name+'.']
        else:
            if('parry' in enD.name):
                enA.status['stun']+=2
                Messages+=[enD.name+' parries '+enA.name+"'s lunge!"]
            else:
                Messages+=[enD.name+' blocks '+player.name+"'s lunge."]
        player.fp+=4
        Total_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]=enD

def exhaustattack(i=(1,0)):
    global Messages,Total_list,player
    enD=Total_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]
    atk=d(player.int+('illusion' in player.doping)*enD.int//d(enD.int))*player.wield.intm
    Messages+=[player.name+' gestures at '+enD.name+'.']
    enD.fp+=atk*MR_divide//(enD.MR+MR_divide)
    if atk*MR_divide//(enD.MR+MR_divide)>0:
        Messages+=['Sudden exhaustion washes over '+enD.name+'.']
        if('purify' in player.doping and 'kai' in enD.doping and d(player.int)>d(enD.int)+enD.MR):
            enD.hp=-45
            Messages+=[player.name+' purifies '+enD.name+'.']
    Total_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]=enD
    player.fp+=8

def healability():
    global player,Messages
    player.VIT=20+(player.str+player.lvl)//8
    player.status['poison']=0
    player.hp=player.VIT
    player.bp=0
    player.fp+=8

def jumpattack(dx,dy):
    global Messages,Total_list,player
    player.x+=dx
    player.y+=dy
    atk=player.dex*player.AC*ER_divide//(ER_divide+player.ER//player.str)//6
    if(not un(player.x,player.y)):
        Total_list[X_Y_list.index((player.x,player.y))].hp=-45
        Messages+=[player.name+' lands on something.']
    else:
        Messages+=['As '+player.name+' lands, stones fly.']
    for i in ((-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)):
        if(not un(player.x+i[0],player.y+i[1])):
            enD=Total_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]
            if not 'huge' in mob.doping:
                enD.hp-=atk
                enD.fp+=atk//4
                enD.status['stun']+=d(enD.fp)//(d(enD.dex)+d(enD.AC))
                Messages+=['Stones hit '+enD.name+'.']
            else:
                Messages+=['Stones bounce from '+enD.name+'.']
            Total_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]=enD
    player.fp+=player.ER*SR_divide//(SR_divide+player.str)

def swapattack(dx,dy):
    global Messages,Total_list,player
    n=X_Y_list.index((player.x+dx,player.y+dy))
    X_Y_list[n]=(player.x,player.y)
    player.x+=dx
    player.y+=dy
    atk=player.int*player.wield.intm*ER_divide//(ER_divide+player.ER)//8
    enD=Total_list[n]
    enD.hp+=enD.AC//4-atk*MR_divide//(enD.MR+MR_divide)
    enD.fp+=atk*MR_divide//(enD.MR+MR_divide)
    Messages+=[player.name+' swaps with '+enD.name+'.']
    if('vampirism' in player.doping):
        player.hp=min(player.VIT,atk*MR_divide//(enD.MR+MR_divide)-enD.AC//4)
        Messages+=[player.name+' drains '+enD.name+"'s life force."]
    if('purify' in player.doping and 'kai' in enD.doping and d(player.int)>d(enD.int)+enD.MR):
        enD.hp=-45
        Messages+=[player.name+' purifies '+enD.name+'.']
    Total_list[n]=enD
    player.fp+=8

#def bashattack():
#    global Messages,Total_list,player
#    atk=(player.AC-player.BAC-player.wear.AC)*ER_divide//(player.ER//(player.dex+player.str//2)+ER_divide)+(player.str+player.int)*player.wield.strm
#    for i in ((-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)):
#        if(not un(player.x+i[0],player.y+i[1])):
#            n=X_Y_list.index((player.x+i[0],player.y+i[1]))
#            enD=Total_list[n]
#            for j in range(atk//(mob.str+mob.lvl+mob.ER)+1):
#                if un(X_Y_list[n][0]+i[0],X_Y_list[n][1]+i[1]):

def Skilling():
    global Messages,player
    if player.skills:
        qyu=''
        for i in player.skills:
            qyu+=i+'- '+Descriptions[i][0]+' SP cost: '+str(Descriptions[i][1])+(', Stun: '+str(Descriptions[i][2]))*bool(Descriptions[i][2])+'.\n'
        screen(0,0,qyu)
        inpu=getcharkey()
        if (inpu in player.skills):
            if inpu=='a' and player.sp>=Descriptions[inpu][1]:
                screen(0,0,'r t y\nf   h to choose direction, Esc to abort.\nv b n')
                inpy=getkey()
                if isdir(inpy):
                    dire=direction(inpy)
                else:
                    if inpy!=b'\x1b':Messages+=['Invalid direction.']
                    return 1
                screen(dire[0],dire[1],'w for clockwise, c for counterclockwise, Esc to abort.')
                inpy=getkey()
                dire=((1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)).index(dire)
                if inpy==b'w':
                    player.sp-=Descriptions[inpu][1]
                    player.status['stun']+=Descriptions[inpu][2]
                    clockattack(dire,1)
                    return 0
                elif inpy==b'c':
                    player.sp-=Descriptions[inpu][1]
                    player.status['stun']+=Descriptions[inpu][2]
                    clockattack(dire,-1)
                    return 0
                if inpy!=b'\x1b':Messages+=['Invalid direction.']
                return 1
            elif inpu=='x' and player.sp>=Descriptions[inpu][1]:
                screen(0,0,'r t y\nf   h to choose direction, Esc to abort.\nv b n')
                inpy=getkey()
                if isdir(inpy):
                    player.sp-=Descriptions[inpu][1]
                    player.status['stun']+=Descriptions[inpu][2]
                    runattack(direction(inpy))
                    return 0
                else:
                    if inpy!=b'\x1b':Messages+=['Invalid direction.']
                    return 1
            elif inpu=='e' and player.sp>=Descriptions[inpu][1]:
                a=b''
                dx=0
                dy=0
                while(a!=b'\r' and a!=b'\n' and a!=b'\x1b' and a!=b'g'):
                    if(isdir(a)):
                        dx+=direction(a)[0]
                        dy+=direction(a)[1]
                    if(abs(dx)>8):
                        dx=sig(dx)*8
                    if(abs(dy)>8):
                        dy=sig(dy)*8
                    screen(dx,dy,'    r t y\nUse f   h to navigate, Esc to abort, Enter or g to confirm target.\n    v b n')
                    a=getkey()
                if(a==b'\x1b'):
                    return 1
                else:
                    if(show[8-dy][8+dx]==Magic_icon or show[8-dy][8+dx]==Player_icon):
                        Messages+=['Invalid target.']
                        return 1
                    else:
                        player.sp-=Descriptions[inpu][1]
                        player.status['stun']+=Descriptions[inpu][2]
                        exhaustattack((dx,dy))
                        return 0
            elif inpu=='w' and player.sp>=Descriptions[inpu][1]:
                player.sp-=Descriptions[inpu][1]
                player.status['stun']+=Descriptions[inpu][2]
                healability()
                return 0
            elif inpu=='z' and player.sp>=Descriptions[inpu][1]:
                a=b''
                dx=0
                dy=0
                while(a!=b'\r' and a!=b'\n' and a!=b'\x1b' and a!=b'g'):
                    if(isdir(a)):
                        if(not un(player.x+dx+direction(a)[0],player.y+dy+direction(a)[1]) and 'huge' in Total_list[X_Y_list.index((player.x+dx+direction(a)[0],player.y+dy+direction(a)[1]))].doping):
                            Messages+=["Can't jump over this."]
                        else:
                            dx+=direction(a)[0]
                            dy+=direction(a)[1]
                    if(abs(dx)>8):
                        dx=sig(dx)*8
                    if(abs(dy)>8):
                        dy=sig(dy)*8
                    screen(dx,dy,'    r t y\nUse f   h to navigate, Esc to abort, Enter or g to confirm target.\n    v b n')
                    a=getkey()
                if(a==b'\x1b'):
                    return 1
                else:
                    if(show[8-dy][8+dx]!=Magic_icon and show[8-dy][8+dx]!=Player_icon):
                        Messages+=['Invalid target.']
                        return 1
                    else:
                        player.sp-=Descriptions[inpu][1]
                        player.status['stun']+=Descriptions[inpu][2]
                        jumpattack(dx,dy)
                        return 0
            elif inpu=='d' and player.sp>=Descriptions[inpu][1]:
                a=b''
                dx=0
                dy=0
                while(a!=b'\r' and a!=b'\n' and a!=b'\x1b' and a!=b'g'):
                    if(isdir(a)):
                        dx+=direction(a)[0]
                        dy+=direction(a)[1]
                    if(abs(dx)>8):
                        dx=sig(dx)*8
                    if(abs(dy)>8):
                        dy=sig(dy)*8
                    screen(dx,dy,'    r t y\nUse f   h to navigate, Esc to abort, Enter or g to confirm target.\n    v b n')
                    a=getkey()
                if(a==b'\x1b'):
                    return 1
                else:
                    if((show[8-dy][8+dx]==Magic_icon or show[8-dy][8+dx]==Player_icon) or Total_list[X_Y_list.index((player.x+dx,player.y+dy))].type<0):
                        Messages+=['Invalid target.']
                        return 1
                    else:
                        player.sp-=Descriptions[inpu][1]
                        player.status['stun']+=Descriptions[inpu][2]
                        swapattack(dx,dy)
                        return 0
            elif inpu=='s' and player.sp>=Descriptions[inpu][1]:
                qyu=''
                for i in player.skills:
                    qyu+=i+'- '+Descriptions[i][0]+' SP cost: '+str(Descriptions[i][1])+'.\n'
                qyu+='Select unneeded ability.'
                screen(0,0,qyu)
                inpy=getcharkey()
                if (inpy in player.skills):
                    qyu=''
                    for i in set(Skill_list) - player.skills:
                        qyu+=i+'- '+Descriptions[i][0]+' SP cost: '+str(Descriptions[i][1])+'.\n'
                    qyu+='Select needed ability.'
                    screen(0,0,qyu)
                    inpi=getcharkey()
                    if (inpi in set(Skill_list) - player.skills):
                        player.skills=player.skills - {inpy} | {inpi}
                        player.sp-=Descriptions[inpu][1]
                        player.status['stun']+=Descriptions[inpu][2]
                        return 0
                    else:
                        if inpi!='\x1b':Messages+=['Invalid ability.']
                        return 1
                else:
                    if inpy!='\x1b':Messages+=['Invalid ability.']
                    return 1
            else:
                Messages+=['Not enough SP.']
                return 1
        if inpu!='\x1b':Messages+=['Invalid ability.']
        return 1
    Messages+=[player.name+' does not possess anything.']
    return 1

def shield_recalculate():
    global player
    if player.DV:
        if(player.wield.dual==3):
            player.AC=player.BAC+player.wear.AC+player.wield.AC
            player.ER=player.wear.ER+player.wield.ER
            player.MR=player.wield.MR
        else:
            player.AC=player.BAC+player.wear.AC
            player.ER=player.wear.ER
            player.MR=0
    else:
        player.AC=player.BAC+player.wear.AC+player.shield.AC
        player.ER=player.wear.ER+player.shield.ER
        player.MR=player.shield.MR
    player.mp=min(player.mp,(player.int*player.wield.intm*ER_divide)//(ER_divide+player.ER))
    player.doping=player.wield.doping+(player.shield.doping)*(1-player.DV)+player.wear.doping+['kai','vampirism']*(ththyhyujy==1)

def controls(fatigue):
    global player,Total_list,Messages,familiar,Floor
    retry=0
    no=0
    if player.status['madness']:
        posx,posy=d(3)-2,d(3)-2
        if not un(player.x+posx,player.y+posy):
            rushattack(player,Total_list[X_Y_list.index((player.x+posx,player.y+posy))])
            no=1
    a=b'.' if player.fp>fatigue or player.status['poison']>P_value or player.status['stun'] else (b'no' if no else getkey())
    if player.status['poison']>P_value:
        player.status['poison']//=2
        player.sp//=2
        player.fp+=4
        Messages+=[player.name+' throws up.']
    elif player.status['stun']:
        player.AC=player.BAC+player.wear.AC
        player.MR=0
        if 'parry' in player.doping:
            player.doping.remove('parry')
        if player.status['stun']==1:
            shield_recalculate()
        player.status['stun']-=1
    elif(a==b'?'):
        help()
        retry=1
    elif(a==b'j'):
        player.status['poison']//=2
        player.sp//=2
        player.fp+=4
        Messages+=[player.name+' throws up.']
    elif(a==b'!'):
        abbs()
        retry=1
    elif(a==b'#'):
        icons()
        retry=1
    elif(a==b'.'):
        player.fp=max(player.fp-player.dex,0)
    elif(isdir(a)):
        dx,dy=direction(a)
        if(un(player.x+dx,player.y+dy)):
            player.x+=dx
            player.y+=dy
            player.fp+=1
        else:
            attack(player,Total_list[X_Y_list.index((player.x+dx,player.y+dy))])
    elif(a==b' '):
        retry=DoVi()
    elif(a==b'a'):
        retry=Skilling()
    elif(a==b'>'):
        if(Map[player.y*x_size+player.x]=='>'):
            Floor+=1
            Messages+=['Ascending to Floor '+str(Floor)+'.']
            newstage()
            generate()
            player.x,player.y=spawn_x,spawn_y
        else:
            Messages+=["Can't ascend here."]
            retry=1
    elif(a==b'@'):
        retry=1
        asking()
    elif(a==b'<'):
        if(Map[player.y*x_size+player.x]=='<'):
            Floor+=2
            Messages+=['Days pass as '+player.name+' descends.']
            newstage()
            generate()
            player.x,player.y=spawn_x,spawn_y
        else:
            Messages+=["Can't descend here."]
            retry=1
    elif(a==b'z' and 'caster' in player.abilities):
        retry=casting()
    elif(a==b'x' and 'lancer' in player.abilities):
        retry=lancing()
    elif(a==b'c' and 'berserker' in player.abilities):
        retry=berserking()
    elif(a==b'i'):
        retry=item_using()
    elif(a==b's'):
        player.inventory.sort(key = lambda x : x.__class__.__name__+x.name)
        player.fp=max(player.fp,0)
        Messages+=[player.name+' sorts their inventory.']
    elif(a==b'g'):
        retry=item_grab()
    elif(a==b'\x1b'):
        print('Press Esc again if '+player.name+' is sure, or press anything else.')
        if(getkey()==b'\x1b'):
            exit()
        else:
            retry=1
    elif(a==b'd'):
        retry=item_destruct()
    elif(a==b'\x18'):
        xp()
        retry=1
    elif(a==b'u'):
        global PT_awares
        player.fp=max(player.fp,0)
        PT_awares+=player.str+player.dex+player.int
        Messages+=[player.name+' shouts for attention.']
    elif(a==b'*'):
        story()
        getkey()
        retry=1
    elif(a==b'no'):
        retry=0
    else:
        Messages+=['Unknown command.']
        retry=1
    if(retry==1):
        screen()
        controls(fatigue)
    else:
        update_state()

def alarms():
    global Messages
    if(player.bp>=player.hp):
        Messages+=[player.name+' will die.']
    elif(player.bp*3>player.VIT):
        Messages+=[player.name+' bleeds severely.']
    elif(player.bp*5>player.VIT):
        Messages+=[player.name+' bleeds heavily.']
    elif(player.bp*9>player.VIT):
        Messages+=[player.name+' bleeds mildly.']
    elif(player.bp>0):
        Messages+=[player.name+' bleeds lightly.']
    if(player.sp>0 or (player.sp==0 and player.VIT-player.hp<5)):
        if(player.sp*5<player.VIT):
            Messages+=[player.name+' is almost starving.']
        elif(player.sp*3<player.VIT):
            Messages+=[player.name+' is very hungry.']
        elif(player.sp*2<player.VIT):
            Messages+=[player.name+' is hungry.']
    if(player.status['poison']):
        Messages+=[player.name+' is poisoned.']
    if(player.status['stun']):
        Messages+=[player.name+' is stunned.']

def check(xx,yy):
    if((xx,yy) in X_Y_list):
        if('stealth' in Total_list[X_Y_list.index((xx,yy))].doping and max(abs(player.x-xx),abs(player.y-yy))>=8-Total_list[X_Y_list.index((xx,yy))].dex//(ST_dice+ST_divide)):
            return '.'
        elif(max(abs(player.x-xx),abs(player.y-yy))<=Magic_distance and Total_list[X_Y_list.index((xx,yy))].icon!=Wall_icon):
            global Targets
            Targets+=[(xx-player.x,yy-player.y)]
        return Total_list[X_Y_list.index((xx,yy))].icon
    elif((xx,yy,0) in X_Y_list):
        return Total_list[X_Y_list.index((xx,yy,0))].icon
    elif(y_size>yy>=0 and x_size>xx>=0 and Map[yy*x_size+xx]=='>'):
        return '>'
    elif(y_size>yy>=0 and x_size>xx>=0 and Map[yy*x_size+xx]=='<'):
        return '<'
    else:
        return '.'

def screen(x=0,y=0,extra=''):
    global Targets,Messages,show
    show=[]
    for i in range(17):
        show+=[[',']*17]
        Targets=[]
    for i in range(17):
        for l in range(17):
            show[16-l][i]=check(player.x+i-8,player.y+l-8)
    show[8-y][8+x]=Magic_icon if show[8-y][8+x] in ('.',Player_icon,Food_icon,Potion_icon,Weapon_icon,Armor_icon,Shield_icon) else Target_icon
    show[8][8]=Player_icon
    mobmob=''
    for i in show:
        for l in i:
            mobmob+=l
    Messages=Messages[-transcript*3:]
    clearchat()
    prints(mobmob,extra)

def prints(mobmob,extra):
    ab=''
    for i in player.abilities:
        ab+=i+' '
    if(ab==''):
        ab='-'
    st=''
    for i,j in player.status.items():
        if j:
            st+=i.capitalize()+': '+str(j)+' '
    re=''
    for i,j in player.relics.items():
        if j[0]:
            re+=i.capitalize()+': '+str(j[0])+'/'+str(j[1])+' '
    print('\n'+mobmob[0:17]+' '*4+'STR:{:<6}HP:{}'.format(player.str,player.hp))
    print(mobmob[17:34]+' '*4+'DEX:{:<6}MP:{}'.format(player.dex,player.mp))
    print(mobmob[34:51]+' '*4+'INT:{:<6}FP:{}'.format(player.int,player.fp))
    print(mobmob[51:68]+' '*4+'SP:{:<7}BP:{}'.format(player.sp,player.bp))
    print(mobmob[68:85]+' '*4+'Wield:'+player.wield.name)
    print(mobmob[85:102]+' '*4+'Wear:'+player.wear.name)
    print(mobmob[102:119]+' '*4+'Shield:'+('-' if player.DV else player.shield.name))
    print(mobmob[119:136]+' '*4+'Abilities:'+ab)
    print(mobmob[136:153]+' '*4+'AC:{:<7}ER:{}'.format(player.AC,player.ER))
    print(mobmob[153:170]+' '*4+'MR:{:<7}SM:{},{},{}'.format(player.MR,player.wield.strm if familiar[0] else '?',player.wield.dexm if familiar[1] else '?',player.wield.intm if familiar[2] else '?'))
    print(mobmob[170:187]+' '*4+'Level:{:<4}Level:{}'.format(player.lvl,XP))
    print(mobmob[187:204]+' '*4+re)
    print(mobmob[204:221])
    print(mobmob[221:238])
    print(mobmob[238:255])
    print(mobmob[255:272])
    print(mobmob[272:]+' '*4+st)
    print(*Messages[-transcript:],sep='\n')
    print(extra)

def statuses():
    global player
    if player.status['poison']:
        player.status['poison']-=1
        player.hp-=player.VIT//10
        player.fp+=2
    if player.status['energy']:
        player.status['energy']-=1
        player.fp=max(0,player.fp-player.dex)
        player.bp*=2
        player.sp-=1
    if player.status['regeneration']:
        player.status['regeneration']-=1
        player.bp//=2
        player.hp=min(player.VIT,player.hp+2)
    if player.status['viper']:
        player.status['viper']-=1
    if player.status['madness']:
        player.status['madness']-=1
        player.str-=1
        player.int+=1
        player.mp=0
    if player.status['brilliance']:
        player.status['brilliance']-=1
        player.int-=1
        player.mp=min(player.mp+player.int,(player.int*player.wield.intm*ER_divide)//(ER_divide+player.ER))

def ignorant():
    global XP,familiar,Know_list,Titles_list,ththyhyujy
    XP=0
    familiar=[1,1,1]
    Know_list=[0]*len(Effects_list)
    Titles_list=[]
    for i in range(len(Effects_list)):
        Title=''
        for l in range(d(4)*d(2)+d(4)):
            Title+=chr(64+d(26))
        Titles_list+=[Title]
' ' ' Main ' ' '
while(True):

    print('Please wait while the world is being generated...')

    ththyhyujy=0
    hey=0
    newstage()
    generate()
    player=Me([VIT,8,8,8,4,0,0,spawn_x,spawn_y])
    while(True):
            alarms()
            ST_dice=d(player.dex)
            statuses()
            screen()
            controls(d(FP_bonus+player.dex-player.ER*SR_divide//(SR_divide+player.str)))
            hey=floor(log(awares+PT_awares+1.0,2.0))
            PT_awares=0
            for i in range(len(Total_list)-1,-1,-1):
                move(i)
            if player.relics['Stakes'][0]==player.relics['Stakes'][1]:
                if ththyhyujy==1:
                    outro(5)
                elif player.hp<=0:
                    outro(4)
                else:
                    outro(1)
            if player.relics['Rabbit Feet'][0]==player.relics['Rabbit Feet'][1]:
                outro(8)
            if(player.hp<=0):
                clearchat()
                if ththyhyujy:
                    if ththyhyujy==1:
                        Messages+=[player.name+', unable to move, rots alive for ages.',player.name+' dies.','Dead End 2: Immortality.']
                    elif ththyhyujy==2:
                        Messages+=[player.name+"'s heart stops instantly.",player.name+' dies.','Dead End 1: Curse.']
                    elif ththyhyujy==3:
                        Messages+=[player.name+" turns to ashes.",player.name+' dies.','Dead End 3: Exorcism.']
                    else:
                        outro(9)
                else:
                    if player.sp==0:
                        Messages+=[player.name+" starves to death.",'Dead End 4: Hunger.']
                    elif Floor==5:
                        if player.int<player.relics['Rabbit Feet'][0]:
                            outro(6)
                        else:
                            outro(7)
                    else:
                        Messages+=[player.name+' dies.']
                print('\n   ***{}***   \n   ***{}***   \n   ***{}***\n'.format(Messages[-3],Messages[-2],Messages[-1]))
                a=b''
                while(a!=b'\r' and a!=b'\n' and a!=b'\x1b' and a!=b'\x0f'):
                    print('Press Enter to continue, or Esc to exit.')
                    a=getkey()
                if(a==b'\x1b'):
                    exit()
                break

    Messages+=[player.name+' rejoins the land of living.']

    Floor=1
    awares=0
    PT_awares=0
    ignorant()
