import pygame

pygame.init()

window_surf = pygame.display.set_mode((800, 600))

# Setup a background
background_surf = pygame.Surface((800, 600))
background_surf.fill(pygame.Color(50, 60, 201))

# Setup an drawing surface with alpha
draw_surf = pygame.Surface((800, 600), pygame.SRCALPHA)
draw_surf.fill(pygame.Color('#535253'))

# Draw shapes with alpha
pygame.draw.line(draw_surf, pygame.Color(255, 255, 255, 0), (1000, 1000), (-1000, -1000))
pygame.draw.aaline(draw_surf, pygame.Color(255, 255, 255, 150), (400, 1000), (400, -1000))
pygame.draw.circle(draw_surf, pygame.Color(255, 255, 255, 120), (600, 500), 50)

clock = pygame.time.Clock()
running = True

while running:
    frame_time = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window_surf.blit(background_surf, (0, 0))
    window_surf.blit(draw_surf, (0, 0))

    pygame.display.update()