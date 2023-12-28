import pygame
import random
import argparse
import logging
import sys
import os
import re

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
parser = argparse.ArgumentParser(description='snake game')
parser.add_argument('--bg-color-1', default="#FFFFFF", help="Permet de déterminer la 1ère couleur du damier."+
                    "Valeur du type #hexadecimal")
parser.add_argument('--bg-color-2', default="#000000", help="Permet de déterminer la 2ème couleur du damier."+
                    "Valeur du type #hexadecimal")
parser.add_argument('--height',default=400, help="Permet de déterminer la hauteur du damier."+
                    "Valeur du type int")
parser.add_argument('--width', default=400, help="Permet de déterminer la largeur du damier."+
                    "Valeur du type int")
parser.add_argument('--fps', default=5, help="Permet de déterminer le nombre d'actions par seconde."+
                    "Valeur du type int")
parser.add_argument('--fruit-color', default="#FF0000", help="Permet de déterminer la couleur du fruit."+
                    "Valeur du type #hexadecimal")
parser.add_argument('--snake-color', default="#00FF00", help="Permet de déterminer la couleur du serpent."+
                    "Valeur du type #hexadecimal")
parser.add_argument('--snake-length', default=3, help="Permet de déterminer la longueur initiale du serpent."+
                    "Valeur du type int")
parser.add_argument('--tile-size', default=20,help="Permet de déterminer la taille d'un carreau du damier."+
                    "Valeur du type int")
parser.add_argument('--gameover-on-exit', help='flag : activer pour mourir quand on sort', action='store_true')
parser.add_argument('--debug', help='flag : activer pour messages de debug', action='store_true')
parser.add_argument('--high-scores-file', default=os.path.join(os.environ['HOME'], '.snake_scores.txt'))
parser.add_argument('--max-high-scores', type=int, default=5)
args = parser.parse_args()

#création des constantes
BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
WIDTH=int(args.width)
HEIGHT=int(args.height)
TIME=int(args.fps)
LARGEUR=int(args.tile_size)
LONGUEUR=int(args.snake_length)
max_scores=int(args.max_high_scores)
POS1=[10*LARGEUR,7*LARGEUR]
POS2=[10*LARGEUR,8*LARGEUR]
POS3=[10*LARGEUR,9*LARGEUR]

#vérification des arguments

#tile_size divise height
if HEIGHT % LARGEUR !=0 :
    raise ValueError("Height must be a multiple of tile size")
#tile_size divise width
if WIDTH % LARGEUR !=0 :
    raise ValueError("Width must be a multiple of tile size")
#20 colonnes minimum
MIN_COLUMNS = 20
if  WIDTH//LARGEUR < MIN_COLUMNS :
    raise ValueError("There must be at least %d columns" % MIN_COLUMNS)
#12 lignes minimum
MIN_ROWS = 12
if HEIGHT//LARGEUR < MIN_ROWS :
    raise ValueError("There must be at least %d rows" % MIN_ROWS)
#longueur initiale du serpent plus grande que 2
MIN_SIZE=2
if LONGUEUR < MIN_SIZE:
    raise ValueError("The initial size of the snake must be greater or equal to %d." % MIN_SIZE)
#couleur du serpent et du damier différentes
if args.snake_color == args.bg_color_1 or args.snake_color == args.bg_color_2 :
    raise ValueError("Snake color must be different from checkboard color")

#initialisation des variables
longueur=LONGUEUR
execute=True
direction=(0,1)
mange=False
score=0
curseur=0
serpent = [POS3,POS2,POS1]

#coordonnées de la pomme générées aléatoirement
pomme1=random.randrange(0,HEIGHT,LARGEUR)
pomme2=random.randrange(0,WIDTH,LARGEUR)

#afficher messages de debug s'il faut
if args.debug :
    logger.setLevel(logging.DEBUG)

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
clock = pygame.time.Clock()

logger.debug('Start main loop')

while execute==True:

    clock.tick(TIME)

    #faire avancer le serpent tout seul
    serpent=[[serpent[0][0]+LARGEUR*direction[0],serpent[0][1]+LARGEUR*direction[1]]]+serpent
    serpent.pop()

    for event in pygame.event.get():

        #pouvoir fermer la fenêtre
        if event.type==pygame.QUIT:
            execute=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q :
                execute=False
        
        #faire tourner le serpent avec les flèches
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:#dte
                if direction==(0,-1):
                    pass
                else:
                    direction=(0,1)
                    serpent=[[serpent[0][0],serpent[0][1]+LARGEUR]]+serpent
                    serpent.pop()
            if event.key==pygame.K_LEFT:#gauche
                if direction==(0,1):
                    pass
                else:
                    direction=(0,-1)
                    serpent=[[serpent[0][0],serpent[0][1]-LARGEUR]]+serpent
                    serpent.pop()
            if event.key==pygame.K_DOWN:#bas
                if direction==(-1,0):
                    pass
                else:
                    direction=(1,0)
                    serpent=[[serpent[0][0]+LARGEUR,serpent[0][1]]]+serpent
                    serpent.pop()
            if event.key==pygame.K_UP:#haut
                if direction==(1,0):
                    pass
                else:
                    direction=(-1,0)
                    serpent=[[serpent[0][0]-LARGEUR,serpent[0][1]]]+serpent
                    serpent.pop()

    #vérifier que le serpent ne sort pas du cadre
    if serpent[0][0]<0 and direction[0]==-1:
        if args.gameover_on_exit :
            execute=False
            logger.info('The snake exited the checkboard')
        else :
            for i in range (longueur):
                serpent[i][0]=serpent[i][0]+HEIGHT
    if serpent[0][0]>HEIGHT and direction[0]==1:
        if args.gameover_on_exit :
            execute=False
            logger.info('The snake exited the checkboard')
        else :
            for i in range (longueur):
                serpent[i][0]=serpent[i][0]-HEIGHT
    if serpent[0][1]<0 and direction[1]==-1:
        if args.gameover_on_exit :
            execute=False
            logger.info('The snake exited the checkboard')
        else :
            for i in range (longueur):
                serpent[i][1]=serpent[i][1]+WIDTH
    if serpent[0][1]>WIDTH and direction[1]==1:
        if args.gameover_on_exit :
            execute=False
            logger.info('The snake exited the checkboard')
        else :
            for i in range (longueur):
                serpent[i][1]=serpent[i][1]-WIDTH


    #dessiner le damier :
    color2=args.bg_color_2
    screen.fill( color2 )
    color1 = args.bg_color_1
    left=0
    #on dessine une rangée sur 2
    while left<WIDTH:
        top=0
        while top<HEIGHT:
            rect = pygame.Rect(left, top, LARGEUR, LARGEUR)
            pygame.draw.rect(screen, color1, rect)
            top+=2*LARGEUR
        left+=2*LARGEUR
    #puis le reste des rangées en décalant d'une colonne
    left=LARGEUR
    while left<WIDTH:
        top=LARGEUR
        while top<HEIGHT:
            rect = pygame.Rect(left, top, LARGEUR, LARGEUR)
            pygame.draw.rect(screen, color1, rect)
            top+=2*LARGEUR
        left+=2*LARGEUR
    

    #dessiner le serpent
    couleur=args.snake_color
    while curseur<longueur:
        pos=serpent[curseur]
        rect = pygame.Rect(pos[1], pos[0], LARGEUR, LARGEUR)
        pygame.draw.rect(screen, couleur, rect)
        curseur+=1
    curseur=0

    couleur_pomme=args.fruit_color
    rect = pygame.Rect(pomme2, pomme1, LARGEUR, LARGEUR)
    pygame.draw.rect(screen, couleur_pomme , rect)
    
    #détecte quand le serpent mange la pomme 
    if serpent[0]==[pomme1,pomme2]:
        mange=True
    
    #génère une nouvelle pomme
    if mange:
        queue=serpent[longueur-1]
        nv_queue=[queue[0]-LARGEUR*direction[0],queue[1]-LARGEUR*direction[1]]
        serpent=serpent+[nv_queue]
        longueur+=1
        pomme1=random.randrange(0,HEIGHT,LARGEUR)
        pomme2=random.randrange(0,WIDTH,LARGEUR)
        #rect = pygame.Rect(pomme1, pomme2, LARGEUR, LARGEUR)
        #pygame.draw.rect(screen,  , rect)
        logger.debug('Snake has eaten a fruit')
        mange=False
        
    #affiche le score
    score=(longueur-3)*10
    pygame.display.set_caption("SCORE :"+str(score))
    pygame.display.update()

    #gérer la collision
    for e in serpent[1:] : 
        if serpent [0]==e :
            print(serpent, e)
            execute = False
            logger.info('The snake collided itself')

def compare_score(score):
    rank=1
    with open(args.high_scores_file, 'r') as myfile :
        for line in myfile :
            if line !="\n" :
                match=re.search('[0-9]', line)
                print(line)
                start=match.start()
                print(start)
                end=match.end()
                print(end)
                print(line[start:end+1])
                s=int(line[start:end+1])
                if score >=s:
                    return (rank)
                rank=rank+1
    return (rank)

def add_score(score, name, rank, max_scores):
    with open(args.high_scores_file, 'r') as myfile :
        i=0
        d={}
        ajout=False
        for line in myfile :
            if line !="\n" and line !="" :
                line.strip("\n")
                i=i+1
                if i==rank :
                    d[i]=name+':'+score
                    d[i+1]=line
                    i=i+1
                else : 
                    d[i]=line
        if i<rank :
            ajout=True
    with open(args.high_scores_file, 'w') as myfile :
        myfile.truncate()
        print(d)
        for i in range(1,min(len(d)+1,max_scores+1)) :
            print(d[i], file=myfile)
        if ajout :
            print(name+':'+score, file=myfile)
        #print (f"{name} {':'} {score}", file=myfile)


pygame.quit()
logger.debug('Game over')
rank=compare_score(score)
if rank <= max_scores :
    name=input("Entrez votre nom : ")
    add_score(str(score), name , rank, max_scores) 


"""
add_score('1', 'Elisa', 1, max_scores)
add_score('2', 'Elisa', 2, max_scores)
add_score('3', 'Elisa', 3, max_scores)
add_score('4', 'Elisa', 4, max_scores)
add_score('5', 'Elisa', 5, max_scores)
add_score('6', 'Elisa', 6, max_scores)
#compare_score(1)
"""