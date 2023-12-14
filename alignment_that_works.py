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
    print(l)

Needleman_Wunsch('ATGC','ATGA')
