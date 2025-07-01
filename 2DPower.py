#Python Imports
import pygame
#Eigene Imports
import sprites
import gui
import Roemdules.mp3 as mp3
class status:
    STATE_CLOSE:int = 0 #Schluss Aus Ende Vorbei
    STATE_INIT:int = 1 #Start 2DPower
    STATE_PLAY:int = 2 #Spiele 2DPower
    STATE_PAUSE:int = 3 # Pause
    status:int = None
    def __init__(self) -> None:
        self.status = self.STATE_INIT
    def init(self) -> None:
        self.status = self.STATE_INIT
    def isInit(self) -> bool:
        return self.status == self.STATE_INIT
    def close(self) -> None:
        self.status = self.STATE_CLOSE
    def isClose(self) -> bool:
        return self.status == self.STATE_CLOSE
    def pause(self) -> None:
        self.status = self.STATE_PAUSE
    def isPause(self) -> bool:
        return self.status == self.STATE_PAUSE
    def play(self) -> None:
        self.status = self.STATE_PLAY
    def isPlay(self) -> bool:
        return self.status == self.STATE_PLAY
game_state = status()
bgm:mp3.Music = None
timer = pygame.time.Clock()
# Keyhandle
def keyhandle() -> None:
    pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] or (keys[pygame.K_LALT] and keys[pygame.K_q]): 
            game_state.close()
    if keys[pygame.K_LALT] and keys[pygame.K_RETURN]:
        pygame.display.toggle_fullscreen()
    if game_state.isPause() and keys[pygame.K_p]:
        game_state.play()
        bgm.resume_music()
        sprites.resume()
        timer.tick(10)
    elif game_state.isPlay() and keys[pygame.K_p]:
        bgm.pause_music()
        sprites.pause()
        timer.tick(10)
        game_state.pause()
#Erst "Menü"
# print(sprites.LaserE2.__dict__)
gui.init_start_fenster(game_state)
while not game_state.isClose():
    events = pygame.event.get()
    keyhandle()
    if game_state.isInit():
        # Initialisierung Level
        sprites.init()
        bgm = mp3.Music(f"data/Level{sprites.Sprites.level}.mp3")
        game_state.play()
    elif game_state.isPlay():
        sprites.update()
        # Ereignis-Handling
        for event in events:
            if event.type == pygame.QUIT:
                game_state.close()
            elif event.type == pygame.USEREVENT and event.EventID == "GameOver":
                game_state.close()
                gui.init_game_over()
            elif event.type == pygame.USEREVENT and event.EventID == "L1 Complete":
                game_state.init()
                bgm.end_music()
                gui.init_game_done(game_state)
    elif game_state.isPause():
        sprites.update(False)
    if game_state.isClose():
        try:
            pygame.quit()
            bgm.end_music()
        except:
            pass 
    timer.tick(30)
# Kreis zeichnen
#pygame.draw.rect(screen, grün, (pSchiffal.X-25, pSchiffal.Y-25, 50, 50))
#pygame.draw.circle(screen, rot, (x, y), radius)