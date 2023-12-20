import pygame
import random
import argparse
import logging
import sys

BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
parser = argparse.ArgumentParser(description='snake game')

def read_args():
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
    args = parser.parse_args()

    #création des constantes
    width=int(args.width)
    height=int(args.height)
    time=int(args.fps)
    largeur=int(args.tile_size)
    longueur=int(args.snake_length)
    color1 = args.bg_color_1
    color2 = args.bg_color_2
    couleur = args.snake_color 
    fruit_color = args.fruit_color
    game_over_on_exit = args.gameover_on_exit
    debug = args.debug


    #vérification des arguments

    #tile_size divise height
    if height % largeur !=0 :
        raise ValueError("Height must be a multiple of tile size")
    #tile_size divise width
    if width % largeur !=0 :
        raise ValueError("Width must be a multiple of tile size")
    #20 colonnes minimum
    MIN_COLUMNS = 20
    if  width//largeur < MIN_COLUMNS :
        raise ValueError("There must be at least %d columns" % MIN_COLUMNS)
    #12 lignes minimum
    MIN_ROWS = 12
    if height//largeur < MIN_ROWS :
        raise ValueError("There must be at least %d rows" % MIN_ROWS)
    #longueur initiale du serpent plus grande que 2
    MIN_SIZE=2
    if longueur < MIN_SIZE:
        raise ValueError("The initial size of the snake must be greater or equal to %d." % MIN_SIZE)
    #couleur du serpent et du damier différentes
    if args.snake_color == args.bg_color_1 or args.snake_color == args.bg_color_2 :
        raise ValueError("Snake color must be different from checkboard color")
    
    #afficher messages de debug s'il faut
    if args.debug :
        logger.setLevel(logging.DEBUG)
    
    return (width, height, time, largeur, longueur, color1, color2, couleur, fruit_color, game_over_on_exit, debug)

def draw_checkerboard(screen, COLOR1, COLOR2, WIDTH, LARGEUR, HEIGHT):
    screen.fill( COLOR2 )
    
    left=0
    #on dessine une rangée sur 2
    while left<WIDTH:
        top=0
        while top<HEIGHT:
            rect = pygame.Rect(left, top, LARGEUR, LARGEUR)
            pygame.draw.rect(screen, COLOR1, rect)
            top+=2*LARGEUR
        left+=2*LARGEUR
    #puis le reste des rangées en décalant d'une colonne
    left=LARGEUR
    while left<WIDTH:
        top=LARGEUR
        while top<HEIGHT:
            rect = pygame.Rect(left, top, LARGEUR, LARGEUR)
            pygame.draw.rect(screen, COLOR1, rect)
            top+=2*LARGEUR
        left+=2*LARGEUR

def get_score(longueur) :
    score=(longueur-3)*10
    return score

def draw_fruit(screen, FRUIT_COLOR, pomme1, pomme2, LARGEUR, longueur):
    rectangle = pygame.Rect(pomme2, pomme1, LARGEUR, LARGEUR)
    pygame.draw.rect(screen, FRUIT_COLOR , rectangle)

def draw_snake(screen,COULEUR, LARGEUR, serpent, longueur):
    curseur = 0
    while curseur<longueur:
        pos=serpent[curseur]
        rect = pygame.Rect(pos[1], pos[0], LARGEUR, LARGEUR)
        pygame.draw.rect(screen, COULEUR, rect)
        curseur+=1
    curseur=0

def draw(screen, FRUIT_COLOR, COULEUR, COLOR1, COLOR2, HEIGHT, LARGEUR, WIDTH, pomme1, pomme2, serpent, longueur):
    draw_checkerboard(screen, COLOR1, COLOR2, WIDTH, LARGEUR, HEIGHT)
    draw_fruit(screen, FRUIT_COLOR, pomme1, pomme2, LARGEUR, longueur)
    draw_snake(screen, COULEUR, LARGEUR, serpent, longueur)

def update_display(screen, FRUIT_COLOR, COULEUR, COLOR1, COLOR2, HEIGHT, LARGEUR, WIDTH, pomme1, pomme2, serpent, longueur):
    draw(screen, FRUIT_COLOR, COULEUR, COLOR1, COLOR2, HEIGHT, LARGEUR, WIDTH, pomme1, pomme2, serpent, longueur)
    score= get_score(longueur)
    pygame.display.set_caption("SCORE :"+str(score))
    pygame.display.update()

def process_events(LARGEUR, GAME_OVER_ON_EXIT, longueur, HEIGHT, WIDTH, pomme1, pomme2, execute, serpent, mange, direction):
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
            if event.key==1073741904:#gauche
                if direction==(0,1):
                    pass
                else:
                    direction=(0,-1)
                    serpent=[[serpent[0][0],serpent[0][1]-LARGEUR]]+serpent
                    serpent.pop()
            if event.key==1073741905:#bas
                if direction==(-1,0):
                    pass
                else:
                    direction=(1,0)
                    serpent=[[serpent[0][0]+LARGEUR,serpent[0][1]]]+serpent
                    serpent.pop()
            if event.key==1073741906:#haut
                if direction==(1,0):
                    pass
                else:
                    direction=(-1,0)
                    serpent=[[serpent[0][0]-LARGEUR,serpent[0][1]]]+serpent
                    serpent.pop()

    if GAME_OVER_ON_EXIT :
        #vérifier que le serpent ne sort pas du cadre
        if serpent[0][0]<0 and direction[0]==-1:
            execute=False
            logger.info('The snake exited the checkboard')
        print(serpent)
        if serpent[0][0]>HEIGHT and direction[0]==1:
            execute=False
            logger.info('The snake exited the checkboard')
        if serpent[0][1]<0 and direction[1]==-1:
            execute=False
            logger.info('The snake exited the checkboard')
        if serpent[0][1]>WIDTH and direction[1]==1:
            execute=False
            logger.info('The snake exited the checkboard')

    else :
        if serpent[0][0]<0 and direction[0]==-1:
            for i in range (longueur):
                serpent[i][0]=serpent[i][0]+HEIGHT
        if serpent[0][0]>HEIGHT and direction[0]==1:
            for i in range(longueur):
                serpent[i][0]=serpent[i][0]-HEIGHT
        if serpent[0][1]<0 and direction[1]==-1:
            for i in range(longueur):
                serpent[i][1]=serpent[i][1]+WIDTH
        if serpent[0][1]>WIDTH and direction[1]==1:
            for i in range(longueur):
                serpent[i][1]=serpent[i][1]-WIDTH
    
    #détecte quand le serpent mange la pomme 
    print((pomme1,pomme2))
    print(serpent[0], 'serpent')
    if serpent[0]==[pomme1,pomme2]:
        print("mange")
        mange=True

    if mange :  
        print ("mangeeeeeeeeeeeee")
        (pomme1, pomme2) = update_fruit(HEIGHT, LARGEUR, WIDTH)
        serpent=[[pomme1,pomme2]]+serpent
        longueur+=1
        logger.debug('Snake has eaten a fruit')
        mange=False

    #gérer la collision
    for e in serpent[1:] : 
        if serpent [0]==e :
            execute = False
            logger.info('The snake collided itself')
    
    return (serpent, direction, execute, mange, pomme1, pomme2)

def move_snake(serpent,LARGEUR, direction):
    serpent=[[serpent[0][0]+LARGEUR*direction[0],serpent[0][1]+LARGEUR*direction[1]]]+serpent
    serpent.pop()
    return (serpent)

def update_fruit(HEIGHT, LARGEUR, WIDTH):
    pomme1=random.randrange(0,HEIGHT,LARGEUR)
    pomme2=random.randrange(0,WIDTH,LARGEUR)
    return (pomme1, pomme2)

def main():

    #initialisation des variables
    longueur=LONGUEUR
    execute=True
    direction=(0,1)
    mange=False
    score=0
    curseur=0
    POS1=[10*LARGEUR,7*LARGEUR]
    POS2=[10*LARGEUR,8*LARGEUR]
    POS3=[10*LARGEUR,9*LARGEUR]
    serpent = [POS3,POS2,POS1]
    (pomme1 , pomme2) =update_fruit(HEIGHT, LARGEUR, WIDTH)

    pygame.init()
    screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
    clock = pygame.time.Clock()

    logger.debug('Start main loop')

    while execute==True:
        clock.tick(TIME)
        serpent = move_snake(serpent,LARGEUR, direction)
        (serpent, direction, execute, mange, pomme1, pomme2) = process_events(LARGEUR, GAME_OVER_ON_EXIT, longueur, HEIGHT, WIDTH, pomme1, pomme2, execute, serpent, mange, direction)
        print (pomme1,pomme2)
        update_display(screen, FRUIT_COLOR, COULEUR, COLOR1, COLOR2, HEIGHT, LARGEUR, WIDTH, pomme1, pomme2, serpent, longueur)

    pygame.quit()
    logger.debug('Game over')

(WIDTH, HEIGHT, TIME, LARGEUR, LONGUEUR, COLOR1, COLOR2, COULEUR, FRUIT_COLOR, GAME_OVER_ON_EXIT, DEBUG) = read_args()

main()