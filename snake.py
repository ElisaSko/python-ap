import pygame
BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
WIDTH=400
HEIGHT=300
TIME=1
LARGEUR=20
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
clock = pygame.time.Clock()
execute=True

while execute==True:

    clock.tick(TIME)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            execute=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q :
                execute=False

    screen.fill( WHITE )
    color = BLACK
    left=0
    while left<WIDTH:
        top=0
        while top<HEIGHT:
            rect = pygame.Rect(left, top, LARGEUR, LARGEUR)
            pygame.draw.rect(screen, color, rect)
            top+=40
        left+=40
    
    left=20
    while left<WIDTH:
        top=20
        while top<HEIGHT:
            rect = pygame.Rect(left, top, LARGEUR, LARGEUR)
            pygame.draw.rect(screen, color, rect)
            top+=40
        left+=40
    
    
    POS=[10*LARGEUR,5*LARGEUR]#(line,column)
    serpent =[POS]
    longueur=3
    couleur=GREEN
    curseur=0
    while curseur<longueur:
        print(serpent)
        pos=serpent[0]
        rect = pygame.Rect(pos[1], pos[0], LARGEUR, LARGEUR)
        pygame.draw.rect(screen, couleur, rect)
        curseur+=1
        pos[1]+=LARGEUR
        serpent+=[pos]
    
    postete=serpent[0]
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key==1073741903:#dte
                serpent[0][0]+=LARGEUR
            #if event.key==1073741904:#gauche
            #if event.key==1073741905:#bas
            #if event.key==1073741906:#haut
            


    pygame.display.update()

pygame.quit()