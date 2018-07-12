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
        global x_size,y_size,Map,spawn_x,spawn_y,Messages,Mob_appear,Noob_Confetti,Mob_ungroup,Lead_c,RL_Mobs
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
    newstage()
except ModuleNotFoundError as err :
    Messages+=['Failed to import map file, '+str(err)]
    Map='.'*262144
    x_size=512
    y_size=512
    spawn_x,spawn_y=x_size//2,y_size//2
except NameError as err:
    Messages+=['Failed to import map, '+str(err)]
    Map='.'*262144
    x_size=512
    y_size=512
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
#####################
#######setting#######
#####################
def consume(ent,what):
    if what == 0:
        ent.hp=ent.VIT
        ent.bp=0
        ent.fp=ent.fp//2
        ent.sp+=2
    elif what == 1:
        ent.mp=(ent.int*ent.wield.intm*ER_divide)//(ER_divide+ent.ER)
        ent.fp=ent.fp//2
        ent.bp=ent.bp//2
        ent.sp+=2
    elif what == 2:
        ent.hp=ent.hp//3
        ent.fp+=10
        ent.sp-=2
    elif what == 3:
        ent.fp=-(ent.dex+10)**2//25
        ent.bp=ent.bp*3
        ent.sp+=4
    elif what == 4:
        ent=lvlup(ent)
#####################
#setting#####potions#
#####################
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
    for i in range(x_size):
        for l in range(y_size):
            if Map[i+l*(x_size)] != '.':
                a=Map[i+l*(x_size)]
                if a is Wall_icon:
                    Total_list+=[Mob(Mob_list[0])]
                    X_Y_list+=[(i,l)]
                elif a is Boss_icon:
                    try:
                        Total_list+=[Boss(Floor)]
                        X_Y_list+=[(i,l)]
                    except:
                        pass
                elif 97 <= ord(a.lower()) <= 122:
                    usl1=rl(RL_Weapons)
                    usl2=rl(RL_Armor)
                    usl3=rl(RL_Mobs)
                    auto=()
                    for r in Presets:
                        if(r[9] is a):
                            auto=r
                    Total_list+=[Mob(auto)] if auto!=() else [Mob(Mob_list[usl3])]
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
#####################
#######setting#######
#####################
def attack(enA,enD):
    global Messages,ththyhyujy
    atk=d((enA.str+('illusion' in enA.doping)*enD.str//d(enD.int))*enA.wield.strm+d(enA.dex*enA.wield.dexm*2))*(enA.DV+DV_divide_a)//(2*DV_divide_a)
    if atk > enD.AC:
        enD.hp+=enD.AC-atk
        enD.bp+=atk*d(enA.int*enA.wield.intm)//d(enD.AC)
        Messages+=[enA.name+' hits '+enD.name+'.']
        if('vampirism' in enA.doping):
            enA.hp=min(enA.VIT,atk-enD.AC)
            Messages+=[enA.name+' drains '+enD.name+"'s life force."]
            if(enD.__class__.__name__ == 'Me' and not ththyhyujy):
                ththyhyujy=1
        if('death' in enA.doping):
            enD.hp=-45
            Messages+=['The curse of '+enA.wield.name+' kills '+enD.name+'.']
            if(enD.__class__.__name__ == 'Me'):
                ththyhyujy=2
        elif('purify' in enA.doping and 'kai' in enD.doping):
            enD.hp=-45
            Messages+=[enA.name+' purifies '+enD.name+'.']
    else:
        Messages+=[enD.name+' blocks '+enA.name+"'s hit."]
    enA.fp+=2

def farattack(enA,enD):
    global Messages,ththyhyujy
    atk=d((enA.dex+('illusion' in enA.doping)*enD.dex//d(enD.int))*enA.wield.dexm+d(enA.dex*enA.wield.dexm*d(2)))*(enA.DV+DV_divide_f)//(4*DV_divide_f)
    if atk > enD.AC//2:
        enD.hp+=enD.AC//2-atk
        enD.bp+=atk*d(enA.dex*enA.wield.dexm)//d(enD.AC)
        Messages+=[enA.name+' hits '+enD.name+' from afar.']
        if('vampirism' in enA.doping):
            enA.hp=min(enA.VIT,atk-enD.AC//2)
            Messages+=[enA.name+' drains '+enD.name+"'s life force."]
            if(enD.__class__.__name__ == 'Me' and not ththyhyujy):
                ththyhyujy=1
        if('death' in enA.doping):
            enD.hp=-45
            Messages+=['The curse of '+enA.wield.name+' kills '+enD.name+'.']
            if(enD.__class__.__name__ == 'Me'):
                ththyhyujy=2
        elif('purify' in enA.doping and 'kai' in enD.doping):
            enD.hp=-45
            Messages+=[enA.name+' purifies '+enD.name+'.']
    else:
        Messages+=[enD.name+' blocks '+enA.name+"'s hit."]
    enA.fp+=4

def rushattack(enA,enD):
    global Messages,ththyhyujy
    atk=d((enA.str+('illusion' in enA.doping)*enD.str//d(enD.int))*enA.wield.strm+d(enA.str*enA.wield.strm*d(2)))*(enA.DV+DV_divide_r)//(3*DV_divide_r)+(enA.str+('illusion' in enA.doping)*enD.str//enD.int)*enA.wield.strm
    if atk > enD.AC and d(enA.dex) > d(enD.dex):
        enD.hp+=enD.AC//2-atk
        enD.fp+=atk*d(enA.str*enA.wield.strm)//d(enD.AC)
        Messages+=[enA.name+' crushes '+enD.name+' mightily.']
        if('vampirism' in enA.doping):
            enA.hp=min(enA.VIT,atk-enD.AC//2)
            Messages+=[enA.name+' drains '+enD.name+"'s life force."]
            if(enD.__class__.__name__ == 'Me' and not ththyhyujy):
                ththyhyujy=1
        if('death' in enA.doping):
            enD.hp=-45
            Messages+=['The curse of '+enA.wield.name+' kills '+enD.name+'.']
            if(enD.__class__.__name__ == 'Me'):
                ththyhyujy=2
        elif('purify' in enA.doping and 'kai' in enD.doping):
            enD.hp=-45
            Messages+=[enA.name+' purifies '+enD.name+'.']
    else:
        Messages+=[enA.name+' crushes floor near '+enD.name+"'s feet."] if atk > enD.AC else [enD.name+' barely blocks '+enA.name+"'s hit."]
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
    else:
        if atk > enD.AC//3:
            enD.mp+=enD.AC//3-atk
    enA.fp+=4
    enA.mp-=Magic_value

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

def death(n):
    global XP,Total_list,X_Y_list,awares
    ent=Total_list[n]
    XP+=ent.xp
    awares-=ent.aware
    for k in ent.drop:
        X_Y_list+=[X_Y_list[n]+tuple([0])]
        Total_list+=[k]
    Total_list.pop(n)
    X_Y_list.pop(n)
#####################
#setting#####attacks#
#####################
def move(n):
    global Total_list,X_Y_list,Messages,XP,player,awares,PT_awares
    if(len(X_Y_list[n])==2):
        mob=Total_list[n]
        if(mob.hp<=0):
            Messages+=[player.name+' kills '+mob.name+'.']
            death(n)
            levelup()
            return
        elif(mob.type>=0):
            xx=X_Y_list[n][0]
            yy=X_Y_list[n][1]
            if(mob.fp>d(FP_bonus+mob.dex-mob.ER*SR_divide//(SR_divide+mob.str))):
                mob.fp=max(mob.fp-mob.dex,0)
            elif mob.aware==0:
                if dis(xx,yy) < 7 + hey + mob.VIT-mob.hp:
                    mob.aware=1
                    awares+=1
                    if mob.leader==1:
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
            elif dis(xx,yy) < safe - mob.lvl - hey - (mob.VIT-mob.hp) and dis(xx,yy) > (1 if mob.type%2==0 and mob.type%3!=2 else (6 if mob.type%2==1 else 2)):
                PT_awares+=mob.shout
                Messages+=[mob.name+' shouts!'] if dis(xx,yy)<9 else [player.name+' hears a shout!']
            elif((mob.fp>=mob.dex and mob.type%2==1) or (mob.fp>=d(mob.dex) and mob.type%3==2)):
                mob.fp=max(mob.fp-mob.dex,0)
            elif(dis(xx,yy)==2 and mob.type%3==2):
                farattack(mob,player)
            elif(mob.type%2==1 and mob.mp>=Magic_value and dis(xx,yy)<=Magic_distance):
                magicattack(mob,player)
            elif(dis(xx,yy)==1 and mob.type%5==4):
                rushattack(mob,player)
                if('roller-skates' in mob.doping and d(mob.dex)>d(mob.fp)):
                    stepaway(mob,n)
            elif(dis(xx,yy)==1 and mob.type==0):
                attack(mob,player)
            elif (mob.type==1 and dis(xx,yy)<=4) or (mob.type%3==2 and dis(xx,yy)==1):
                stepaway(mob,n)
            elif(dis(xx,yy)==1):
                attack(mob,player)
            else:
                stepahead(mob,n)
                if('roller-skates' in mob.doping and d(mob.dex)>d(mob.fp)):
                    if(dis(xx,yy)==1):
                        rushattack(mob,player)
                    else:
                        stepahead(mob,n)
            mob.hp-=mob.bp
            mob.bp=mob.bp*3//2
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
    Messages+=['.      rest one turn.']
    Messages+=['g      get item on your tile.']
    Messages+=['i      use item in your inventory.']
    Messages+=['d      destroy item in inventory.']
    Messages+=['a      use ability.']
    Messages+=['Esc    exit.']
    Messages+=['?      help.']
    Messages+=['!      abbreviations in stats.']
    Messages+=['#      icons list.']
    Messages+=['*      view transcript.']
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
        if(show[8-dy][8+dx]==Magic_icon):
            if(bonus==1):
                if(player.mp>=max(abs(dx),abs(dy))*2):
                    player.x+=dx
                    player.y+=dy
                    player.mp-=max(abs(dx),abs(dy))*2
                    Messages+=['Player teleports.']
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
        if(show[8-dy][8+dx]==Magic_icon):
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
        if(show[8-dy][8+dx]==Magic_icon):
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
    else:
        player.inventory+=[player.shield]
        Messages+=[player.name+' unwields '+player.shield.name+'.']
        player.shield=player.inventory[a]
        Messages+=[player.name+' wields '+player.shield.name+'.']
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

def item_using():
    global player,Messages
    if(len(player.inventory)>0):
        clearchat()
        for i in range(len(player.inventory)):
            print(chr(i+97)+" - "+player.inventory[i].name)
        a=ord(getcharkey())-97
        if(0<=a<=len(player.inventory)-1):
            if(player.inventory[a].name in Weapon_types_list):
                change_weapon(a)
            elif(player.inventory[a].name in Armor_types_list):
                change_armor(a)
            elif(player.inventory[a].name in Food_types_list):
                player.sp=min(player.VIT,player.sp+player.inventory[a].nutrition)
                Messages+=[player.name+' eats '+player.inventory[a].name+'.']
            elif(player.inventory[a].name in Effects_list or player.inventory[a].name in Titles_list):
                what=player.inventory[a].number
                consume(player,what)
                global Know_list
                if(Know_list[what]==0):
                    Know_list[what]=Titles_list[what]
                    for i in player.inventory:
                        if(i.name is Titles_list[what]):
                            i.name=Effects_list[what]
                Messages+=[player.name+' drinks '+Effects_list[what]+'.']
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
    atk=player.str*player.wield.strm*(player.DV+2)//5
    for i in ((-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0))[start-1-(wise==1):start+7-(wise==1)][::wise]:
        if(not un(player.x-i[0],player.y-i[1])):
            enD=Total_list[X_Y_list.index((player.x-i[0],player.y-i[1]))]
            if(atk>enD.AC):
                atk=atk-enD.AC//4
                enD.hp-=atk
                enD.fp+=atk//3
                Messages+=[player.name+' hits '+enD.name+'.']
                player.fp+=2
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
                enD.fp+=atk//2
                player.fp+=4
                atk=atk*3//5
                Messages+=[enD.name+' struggles to block '+player.name+"'s hit."]
            Total_list[X_Y_list.index((player.x-i[0],player.y-i[1]))]=enD

def runattack(i=(1,0)):
    global Messages,Total_list,player
    while un(player.x+i[0],player.y+i[1]) and d(player.fp)<player.dex:
        player.x+=i[0]
        player.y+=i[1]
        player.fp+=2
    if not un(player.x+i[0],player.y+i[1]):
        enD=Total_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]
        atk=player.dex*player.wield.dexm*(player.DV+1)*3//max(5,player.fp)
        if atk > enD.AC//4:
            enD.hp+=enD.AC//4-atk
            enD.bp+=atk*player.dex*player.wield.dexm//d(enD.AC)
            Messages+=[player.name+' lunges at '+enD.name+'.']
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
            Messages+=[enD.name+' blocks '+player.name+"'s lunge."]
        player.fp+=4
        Total_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]=enD

def exhaustattack(i=(1,0)):
    global Messages,Total_list,player
    enD=Total_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]
    atk=(player.int+('illusion' in player.doping)*enD.int//d(enD.int))*player.wield.intm
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
#    player.VIT+=1
    player.hp=player.VIT
    player.bp=0
    player.fp+=8

def jumpattack(dx,dy):
    global Messages,Total_list,player
    player.x+=dx
    player.y+=dy
    atk=(player.str+player.dex)*player.AC*ER_divide//(ER_divide+player.ER)//12
    Messages+=['As '+player.name+' lands, stones fly.']
    for i in ((-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)):
        if(not un(player.x+i[0],player.y+i[1])):
            enD=Total_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]
            enD.hp-=atk
            enD.fp+=atk//4
            Messages+=['Stones hit '+enD.name+'.']
            Total_list[X_Y_list.index((player.x+i[0],player.y+i[1]))]=enD
    player.fp+=player.AC-player.BAC

def swapattack(dx,dy):
    global Messages,Total_list,player
    n=X_Y_list.index((player.x+dx,player.y+dy))
    X_Y_list[n]=(player.x,player.y)
    player.x+=dx
    player.y+=dy
    atk=player.int*player.wield.intm*ER_divide//(ER_divide+player.ER)
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

def Skilling():
    global Messages,player
    if player.skills:
        qyu=''
        for i in player.skills:
            qyu+=i+'- '+Descriptions[i][0]+' SP cost: '+str(Descriptions[i][1])+'.\n'
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
                    clockattack(dire,1)
                    return 0
                elif inpy==b'c':
                    player.sp-=Descriptions[inpu][1]
                    clockattack(dire,-1)
                    return 0
                if inpy!=b'\x1b':Messages+=['Invalid direction.']
                return 1
            elif inpu=='x' and player.sp>=Descriptions[inpu][1]:
                screen(0,0,'r t y\nf   h to choose direction, Esc to abort.\nv b n')
                inpy=getkey()
                if isdir(inpy):
                    player.sp-=Descriptions[inpu][1]
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
                    if(show[8-dy][8+dx]==Magic_icon):
                        Messages+=['Invalid target.']
                        return 1
                    else:
                        player.sp-=Descriptions[inpu][1]
                        exhaustattack((dx,dy))
                        return 0
            elif inpu=='w' and player.sp>=Descriptions[inpu][1]:
                screen(0,0,'Esc to abort.')
                if(a==b'\x1b'):
                    return 1
                player.sp-=Descriptions[inpu][1]
                healability()
                return 0
            elif inpu=='z' and player.sp>=Descriptions[inpu][1]:
                a=b''
                dx=0
                dy=0
                while(a!=b'\r' and a!=b'\n' and a!=b'\x1b' and a!=b'g'):
                    if(isdir(a)):
                        if(not un(player.x+dx+direction(a)[0],player.y+dy+direction(a)[1]) and Total_list[X_Y_list.index((player.x+dx+direction(a)[0],player.y+dy+direction(a)[1]))].type<0):
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
                    if(show[8-dy][8+dx]!=Magic_icon or player.x+dx>x_size):
                        Messages+=['Invalid target.']
                        return 1
                    else:
                        player.sp-=Descriptions[inpu][1]
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
                    if(show[8-dy][8+dx]==Magic_icon or Total_list[X_Y_list.index((player.x+dx,player.y+dy))].type<0):
                        Messages+=['Invalid target.']
                        return 1
                    else:
                        player.sp-=Descriptions[inpu][1]
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
                        return 0
                    else:
                        if inpi!='\x1b':Messages+=['Invalid ability.']
                        return 1
                else:
                    if inpy!='\x1b':Messages+=['Invalid ability.']
                    return 1
            else:
                Messages+=['Coming soon!']
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
    player.doping=player.wield.doping+(player.shield.doping)*(1-player.DV)+player.wear.doping

def controls(fatigue):
    global player,Total_list,Messages,familiar,Floor
    retry=0
    a=getkey() if player.fp<=fatigue else b'.'
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
    if(player.bp>player.VIT):
        Messages+=[player.name+' will die.']
    elif(player.bp*3>player.VIT):
        Messages+=[player.name+' bleeds severely.']
    elif(player.bp*5>player.VIT):
        Messages+=[player.name+' bleeds heavily.']
    elif(player.bp*9>player.VIT):
        Messages+=[player.name+' bleeds mildly.']
    elif(player.bp>0):
        Messages+=[player.name+' bleeds lightly.']
    if(player.sp>0 or (player.sp==0 and player.hp==player.VIT)):
        if(player.sp*5<player.VIT):
            Messages+=[player.name+' is almost starving.']
        elif(player.sp*3<player.VIT):
            Messages+=[player.name+' is very hungry.']
        elif(player.sp*2<player.VIT):
            Messages+=[player.name+' is hungry.']

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
        mobmob+='\n'
    Messages=Messages[-transcript*3:]
    clearchat()
    prints(mobmob,extra)

def prints(mobmob,extra):
    ab=''
    for i in player.abilities:
        ab+=i+' '
    if(ab==''):
        ab='-'
    print('\n'+mobmob[0:17]+' '*4+'STR:{:<6}HP:{}'.format(player.str,player.hp))
    print(mobmob[18:35]+' '*4+'DEX:{:<6}MP:{}'.format(player.dex,player.mp))
    print(mobmob[36:53]+' '*4+'INT:{:<6}FP:{}'.format(player.int,player.fp))
    print(mobmob[54:71]+' '*4+'SP:{:<7}BP:{}'.format(player.sp,player.bp))
    print(mobmob[72:89]+' '*4+'Wield:'+player.wield.name)
    print(mobmob[90:107]+' '*4+'Wear:'+player.wear.name)
    print(mobmob[108:125]+' '*4+'Shield:'+('-' if player.DV else player.shield.name))
    print(mobmob[126:143]+' '*4+'Abilities:'+ab)
    print(mobmob[144:161]+' '*4+'AC:{:<7}ER:{}'.format(player.AC,player.ER))
    print(mobmob[162:179]+' '*4+'MR:{:<7}SM:{},{},{}'.format(player.MR,player.wield.strm if familiar[0] else '?',player.wield.dexm if familiar[1] else '?',player.wield.intm if familiar[2] else '?'))
    print(mobmob[180:197]+' '*4+'XP:{:<7}Level:{}'.format(XP,player.lvl))
    print(mobmob[198:],*Messages[-transcript:],sep='\n')
    print(extra)

def ignorant():
    global XP,familiar,Know_list,Titles_list
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

    hey=0
    newstage()
    generate()
    player=Me([VIT,8,8,8,4,0,0,spawn_x,spawn_y])

    while(True):
            alarms()
            ST_dice=d(player.dex)
            screen()
            controls(d(FP_bonus+player.dex-player.ER*SR_divide//(SR_divide+player.str)))
            hey=floor(log(awares+PT_awares+1.0,2.0))
            PT_awares=0
            for i in range(len(Total_list)-1,-1,-1):
                move(i)
            if(player.hp<=0):
                clearchat()
                Messages+=[player.name+' dies.']
                if ththyhyujy:
                    if ththyhyujy==1:
                        Messages+=[player.name+', unable to move, rots alive for ages.','Dead End 2:Bloodlust']
                    elif ththyhyujy==2:
                        Messages+=[player.name+"'s heart stops instantly.",'Dead End 1:Curse']
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
