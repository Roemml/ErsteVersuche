import pygame

import Schiffal

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D Power")

all_sprites = pygame.sprite.Group()
pSchiffal = Schiffal.Schiffal(500,400,300)
all_sprites.add(pSchiffal)

bgc = (200, 200, 200)
#grün = (0, 255, 0)

# Spiel Schleife
running = True
while running:
    

    # Ereignis-Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill(bgc)
    all_sprites.draw(screen)

    # Kreis zeichnen
    #pygame.draw.rect(screen, grün, (pSchiffal.X-25, pSchiffal.Y-25, 50, 50))
    #pygame.draw.circle(screen, rot, (x, y), radius)

    # Bildschirm aktualisieren
    pygame.display.flip()

    # Framerate steuern
    pygame.time.Clock().tick(60)

# Pygame beenden
pygame.quit()

#if rect1.colliderect(rect2)
#pyinstaller --onefile --windowed --icon=mein_icon.ico Program.py