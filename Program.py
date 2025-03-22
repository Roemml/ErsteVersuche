#Python Imports
import pygame

#Eigene Imports
import sprites

#global vars

shipHP = 500
shipSpeed = 10

# Initialisierungen
pygame.init()
screen = pygame.display.set_mode((sprites.SCREEN_WIDTH, sprites.SCREEN_HEIGHT))
icon = pygame.image.load("Gameico.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("2D Power")

#bg = (sprites.Hintergrund(1), sprites.Hintergrund(2))
#pShip = sprites.Ship()
sprites.init()

# Spiel Schleife
running = True
while running:
    

    # Ereignis-Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] or (keys[pygame.K_LALT] and keys[pygame.K_q]):
        running = False

    sprites.all_game_sprites.update()
    sprites.all_game_sprites.draw(screen)

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
#pyinstaller --onefile --windowed --icon=Game.ico Program.py
#pyinstaller --onefile --windowed Program.py