import sys
import re
seq=''
var=''
i=0
id_seq=None
id_var=None
for line in sys.stdin:

    line=line.rstrip()

    if not line.startswith(';'):

        if line.startswith('>'):

            if id_seq is None:

                id_seq = line[1:]

            elif id_var is None:

                id_var = line[1:]

            else:

                print(id_seq,'  ',seq,id_var,'  ',var,i)

                seq=''

                var=''

                id_seq=line[1:]

                id_var=None

                i=i+1

        elif re.match('[ACTG]*$',line):

            if id_var is None:

                seq=seq+line

            else:

                var=var+line

    #else:

        #raise Exception('Invalid line: %s' % line)


def Needleman_Wunsch(seq, var):
    l=[[None]*len(seq)]*len(var)
    for i in range(len(seq)):
        for j in range(len(var)):
            if i == 0 or j ==0 :
                l[i][j]=-2*(i+j)
            else :
                if seq[i]==var[j]:
                    matchscore=1
                else:
                    matchscore=-1
                sup=l[i-1][j]+(-2) 
                dte=l[i][j-1]+(-2)
                diag=l[i-1][j-1]+matchscore
                l[i][j]=max(sup, dte, diag)
    return(l)

print(Needleman_Wunsch('ATGC','ATGA'))

def remonte_chemin(seq,var):#TODO the scores list isn't +1, -1 or -2 : change that
    tab=Needleman_Wunsch(seq,var)
    scores=[]
    i=len(seq)-1
    j=len(var)-1
    while i>0 and j>0:
        up=tab[i-1][j]
        left=tab[i][j-1]
        diag=tab[i-1][j-1]
        next = max(up,left,diag)
        if next == diag:
            scores.append(tab[i][j]-tab[i-1][j-1]) #TODO returns 0 sometimes
            i=i-1
            j=j-1
        elif next == up:
            scores.append(tab[i][j]-tab[i-1][j])
            i=i-1
        elif next == left:
            scores.append(tab[i][j]-tab[i][j-1])
            j=j-1
    return scores

def alignment(seq,var):#doesn't work (bc of the scores list too)
    scores=remonte_chemin(seq,var)
    seq_align=''
    var_align=''
    for i in range(len(scores)):
        if scores[i]==1:
            seq_align=seq_align+seq[i]
            var_align=var_align+var[i]
        elif scores[i]==-1:
            seq_align=seq_align+'-'
            var_align=var_align+var[i]
        elif scores[i]==-2:
            seq_align=seq_align+seq[i]
            var_align=var_align+'-'
    return(seq_align,var_align)

print(remonte_chemin('ATGC','ATGA'))
print(alignment('ATGC','ATGA'))