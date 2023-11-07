import pygame
BLACK= (0,0,0)
WHITE= (255,255,255)
WIDTH=400
HEIGHT=300
TIME=1
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
clock = pygame.time.Clock()
while True:

    clock.tick(TIME)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()

    screen.fill( WHITE )

    pygame.display.update()
