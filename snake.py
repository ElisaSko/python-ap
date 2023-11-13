import pygame
import random

#création des constantes
BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
WIDTH=400
HEIGHT=300
TIME=5
LARGEUR=20
LONGUEUR=3
POS1=[10*LARGEUR,7*LARGEUR]
POS2=[10*LARGEUR,8*LARGEUR]
POS3=[10*LARGEUR,9*LARGEUR]

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

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
clock = pygame.time.Clock()


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

   #vérifier que le serpent ne sort pas du cadre
    if serpent[0][0]<0 and direction[0]==-1:
            execute=False
        
    if serpent[0][0]>HEIGHT and direction[0]==1:
        execute=False
        
    if serpent[0][1]<0 and direction[1]==-1:
        execute=False
        
    if serpent[0][1]>WIDTH and direction[1]==1:
        execute=False

    #dessiner le damier :
    screen.fill( WHITE )
    color = BLACK
    left=0
    #on dessine une rangée sur 2
    while left<WIDTH:
        top=0
        while top<HEIGHT:
            rect = pygame.Rect(left, top, LARGEUR, LARGEUR)
            pygame.draw.rect(screen, color, rect)
            top+=40
        left+=40
    #puis le reste des rangées en décalant d'une colonne
    left=20
    while left<WIDTH:
        top=20
        while top<HEIGHT:
            rect = pygame.Rect(left, top, LARGEUR, LARGEUR)
            pygame.draw.rect(screen, color, rect)
            top+=40
        left+=40
    

    #dessiner le serpent
    couleur=GREEN
    while curseur<longueur:
        pos=serpent[curseur]
        rect = pygame.Rect(pos[1], pos[0], LARGEUR, LARGEUR)
        pygame.draw.rect(screen, couleur, rect)
        curseur+=1
    curseur=0

    rect = pygame.Rect(pomme2, pomme1, LARGEUR, LARGEUR)
    pygame.draw.rect(screen, RED , rect)
    
    #détecte quand le serpent mange la pomme 
    if serpent[0]==[pomme1,pomme2]:
        mange=True
    
    #génère une nouvelle pomme
    if mange:
        serpent=[[pomme1,pomme2]]+serpent
        longueur+=1
        pomme1=random.randrange(0,HEIGHT,LARGEUR)
        pomme2=random.randrange(0,WIDTH,LARGEUR)
        rect = pygame.Rect(pomme1, pomme2, LARGEUR, LARGEUR)
        pygame.draw.rect(screen, RED , rect)
        mange=False
        
    #affiche le score
    score=(longueur-3)*10
    pygame.display.set_caption("SCORE :"+str(score))
    pygame.display.update()

pygame.quit()