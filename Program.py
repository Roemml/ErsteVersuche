#Python Imports
import pygame

#Eigene Imports
import Global
import Ship
import BG

# Initialisierungen
pygame.init()
screen = pygame.display.set_mode((Global.screenWidth, Global.screenHeight))
pygame.display.set_caption("2D Power")
all_sprites = pygame.sprite.Group()
#gameBG = BG.HintergrundFix()
#all_sprites.add(gameBG)
bg1 = BG.Hintergrund(1)
bg2 = BG.Hintergrund(2)
pShip = Ship.Ship()
all_sprites.add((bg1, bg2))
#all_sprites.add(bg2)
all_sprites.add(pShip)

bgc = (200, 200, 200)
#grün = (0, 255, 0)

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

    all_sprites.update()
    #screen.fill(bgc)
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
#pyinstaller --onefile --windowed --icon=Game.ico Program.py
#pyinstaller --onefile --windowed Program.py