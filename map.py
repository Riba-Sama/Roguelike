Map=('#'*512)+('#'+'.'*510+'#')*246+('#'+'.'*246+' '*17+'.'*247+'#')*8+('#'+'.'*246+' '*8+'@'+' '*8+'.'*247+'#')+('#'+'.'*246+' '*17+'.'*247+'#')*8+('#'+'.'*510+'#')*224+('#'+'.'*243+'#'*8+'.'*8+'#'*8+'.'*243+'#')+(('#'+'.'*243+'#'+'.'*22+'#'+'.'*243+'#')*2+('#'+'.'*243+'#'+'.'*8+'g'+'.'*4+'k'+'.'*8+'#'+'.'*243+'#'))*3+('#'+'.'*243+'#'+'.'*11+'&'+'.'*10+'#'+'.'*243+'#')+('#'+'.'*243+'#'+'.'*22+'#'+'.'*243+'#')*12+('#'*512)
x_size=512
y_size=512
if(len(Map)!=x_size*y_size):
    print('Map size is',len(Map),', must be',x_size*y_size,'instead.')
    Map='.'*(x_size*y_size)
