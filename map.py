from settings import *
from entities import *
Maps=[(
'###################'+
'#        >        #'+
'#   g g g g g g   #'+
'#    g g g g g    #'+
'#   g g g g g g   #'+
'#    g g & g g    #'+
'#   kkkkkkkkkkk   #'+
'#                 #'+
'##               ##'+
'###             ###'+
'####           ####'+
'#####         #####'+
'####           ####'+
'###             ###'+
'##      ?]?      ##'+
'#       ?!?       #'+
'#.................#'*168+
'#                 #'*14+
'#        @        #'+
'###################'
,19,200,200,60,15,10,(0,16,16,1,1,1)),
(
'###################'+
'#  #  #  #  #  #  #'+
'# # #   #>#   # # #'+
'#  #  #  &  #  #  #'+
'# # #   # #   # # #'+
'#  #  #  #  #  #  #'+
'##  # O # # O #  ##'+
'###   #  #  #   ###'+
'####    # #    ####'+
'##### O  #  O #####'+
'####    # #    ####'+
'###   #  #  #   ###'+
'##  #   # #   #  ##'+(
'#..#..#..#..#..#..#'+
'#.#..#..#.#..#..#.#')*84+(
'#  #  #  #  #  #  #'+
'# #  #  # #  #  # #')*8+
'#        @        #'+
'#                 #'+
'###################'
,19,200,200,30,12,4,(0,12,12,3,3,3,1)),
(
'#######################################'+
'#                  #                  #'+
'#                 #>#                 #'+
'#        #         #        #         #'+
'#       #v#                #v#        #'+
'#        #         #        #         #'+
'#                 #&#                 #'+
'#        #         #        #         #'+
'#       # #                # #        #'+
'#        #         #        #         #'+
'#                 #v#                 #'+
'#        #         #        #         #'+
'#       # #                # #        #'+
'#        #         #        #         #'+
'#                 # #                 #'+
'#                  #                  #'+(
'#........#..................#.........#'+
'#.......#.#................#.#........#'+
'#........#..................#.........#'+
'#..................#..................#'+
'#.................#.#................##'+
'#..................#..................#')*28+
'#                                     #'*13+
'#                  @                  #'+
'#                                     #'+
'#######################################'
,39,200,200,80,10,3,(1,1,1,8,8,8,2,1,1,1)),
(
'#######################################'+
'#                                     #'+
'#                  &                  #'+
'#                                     #'+
'#.....................................#'*182+
'#                                     #'*11+
'#                  @                  #'+
'#                                     #'+
'#######################################'
,39,200,100,40,9,2,(10,0,0,2,2,2,10,6,6,10,5))]
'''1-x size,2-y size,3-Mob appear,4-Noob Confetti,5-Mob ungroup,6-Lead c,7-RL Mobs'''
for i in range(len(Maps)):
    if(len(Maps[i][0])!=Maps[i][1]*Maps[i][2]):
        print('Map size is',len(Maps[i][0]),', must be ',Maps[i][1]*Maps[i][2],' instead.')
        Maps[i][0]='.'*(Maps[i][1]*Maps[i][2])
Presets=Mob_list
