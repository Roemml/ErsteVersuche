#Python Imports
import pygame
#Eigene Imports
import sprites
import gui
import Roemdules.mp3 as mp3
bgm = None
#Erst "Menü"
gui.init_start_fenster()
while sprites.state != sprites.STATE_CLOSE:
    if sprites.state == sprites.STATE_INIT:
        if sprites.level == 0:    
            # Initialisierungen pygame
            pygame.init()
            screen: pygame.Surface = pygame.display.set_mode((sprites.SCREEN_WIDTH, sprites.SCREEN_HEIGHT))
            pygame.display.set_icon(pygame.image.load("Gameico.png"))
            pygame.display.set_caption("2D Power")
            sprites.level = 1
        # Initialisierung Level
        sprites.init()
        bgm = mp3.Music(f"Level{sprites.level}.mp3")
        sprites.state = sprites.STATE_PLAY
    if sprites.state == sprites.STATE_PLAY:
        # Ereignis-Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sprites.state = sprites.STATE_CLOSE
            elif event.type == pygame.USEREVENT and event.EventID == "GameOver":
                sprites.state = sprites.STATE_CLOSE
                gui.init_game_over()
            elif event.type == pygame.USEREVENT and event.EventID == "L1 Complete":
                sprites.state = sprites.STATE_INIT
                bgm.end_music()
                gui.init_game_done()
        # Key Pressed Handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or (keys[pygame.K_LALT] and keys[pygame.K_q]): 
            sprites.state = sprites.STATE_CLOSE
        if keys[pygame.K_p]:
            bgm.pause_music()
            gui.init_pause()
            bgm.resume_music()
    if sprites.state == sprites.STATE_PLAY:
        sprites.enemy_creation()
        sprites.all_sprites.update()
        sprites.all_sprites.draw(screen)
        pygame.display.flip()
        sprites.frame_couter += 1
        pygame.time.Clock().tick(60)
    if sprites.state == sprites.STATE_CLOSE:
        try:
            pygame.quit()
            bgm.end_music()
        except:
            pass    
# Kreis zeichnen
#pygame.draw.rect(screen, grün, (pSchiffal.X-25, pSchiffal.Y-25, 50, 50))
#pygame.draw.circle(screen, rot, (x, y), radius)