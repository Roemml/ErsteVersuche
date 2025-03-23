#Python Imports
import pygame

#Eigene Imports
import sprites

# Initialisierungen
#pygame
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((sprites.SCREEN_WIDTH, sprites.SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load("Gameico.png"))
pygame.display.set_caption("2D Power")

#eigene
sprites.init()

# Spiel Schleife
running: bool = True # Spiel läuft noch?
while running:
    
    # Ereignis-Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Key Pressed Handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] or (keys[pygame.K_LALT] and keys[pygame.K_q]): 
        running = False

    # sprite updates
    sprites.all_game_sprites.update()
    sprites.all_hud_sprites.update()
    # sprites zeichnen
    sprites.all_game_sprites.draw(screen)
    sprites.all_hud_sprites.draw(screen)

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