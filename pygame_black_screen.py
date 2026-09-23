import pygame

pygame.init()
WIDTH = 800
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
BLACK = (0, 0, 0)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill(BLACK)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()