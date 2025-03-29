#Python Imports
import pygame

#Eigene Imports
import sprites
import gui
import MP3

#Erst "Menü"
gui.init_start_fenster()
running: bool = gui.starten # Spiel läuft noch?
# Initialisierungen
if running:
    #pygame
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((sprites.SCREEN_WIDTH, sprites.SCREEN_HEIGHT))
    pygame.display.set_icon(pygame.image.load("Gameico.png"))
    pygame.display.set_caption("2D Power")
    #eigene
    sprites.init()
    MP3.start_music()
    # Spiel Schleife
while running:
    # Ereignis-Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT and event.EventID == "GameOver":
            running = False
            gui.init_game_over()
    # Key Pressed Handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] or (keys[pygame.K_LALT] and keys[pygame.K_q]): 
        running = False
    if keys[pygame.K_p]:
        MP3.pause_music()
        gui.init_pause()
        MP3.resume_music()

    sprites.enemy_creation()
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
    sprites.frame_couter += 1
    pygame.time.Clock().tick(60)
if gui.starten:
    # Pygame beenden
    pygame.quit()
    MP3.end_music()
    #pyinstaller --onefile --windowed --icon=Game.ico 2DPower.py