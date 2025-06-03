#Python Imports
import pygame
import random
import os
#Eigene Imports
import Roemdules.mp3 as mp3
# Globale Konstanzen
SCREEN_WIDTH:int = 800 # Breite des Spiel Fensters
SCREEN_HEIGHT:int = 600 # Höhe des Spiel Fensters
LAYER_HG:int = 0 #Hintergründe sind ganz im Hintergrund
LAYER_ENEMY:int = 1 #Enemy Layer
LAYER_SHIP:int = 2 #Schill Layer
LAYER_LASER:int = 3 #Laser layer
LAYER_UI:int = 4 #Layer User Interface
STATE_CLOSE:int = 0 #Schluss Aus Ende Vorbei
STATE_INIT:int = 1 #Start 2DPower
STATE_PLAY:int = 2 #Spiele 2DPower
# Globale Variablen
all_sprites:pygame.sprite.LayeredUpdates = pygame.sprite.LayeredUpdates() # Alle Sprites des Spiels selbst
state:int = STATE_INIT
level:int = 0 # Level
frame_couter:int = 0 #Framecounter
#Enemy Laser Definitionen
class LaserBase:
    sprite:str = ""
    speed_x:int = 0
    speed_y:int = 0
    hp:int = 0
    fire_rate:int = 0
class LaserE1(LaserBase):
    sprite:str = "LaserE1.png"
    speed_x:int = 0
    speed_y:int = 10
    hp:int = 10
class LaserE2(LaserBase):
    sprite:str = "LaserE2.png"
    speed_x:int = 0
    speed_y:int = 20
    hp:int = 1
class LaserE2a(LaserE2):
    speed_x:int = -20
class LaserE2b(LaserE2):
    speed_x:int = +20
class LaserEB1(LaserBase):
    sprite:str = "LaserEB1.png"
    speed_x:int = 0
    speed_y:int = 10
    hp:int = 30
class Hintergrund(pygame.sprite.Sprite):
    """
    Der Hintergrund des Spiels.
    """
    # Klassen Konstanten
    SCROLL_NO:int = 0 # Der Hintergrund ist statisch
    SCROLL_DOWN:int = 1 # Her Hintergrund scrollt nach unten, man bewegt sich nach oben
    SCROLL_SPEED:int = 15 # Scrollgeschwindigkeit
    def __init__(self, bg_scroll:int = SCROLL_NO):
        """
        Konstruktor des Hintergrunds.
        """
        super().__init__()
        self._layer = LAYER_HG
        _set_image_and_rect(self,"HGTest.png",False)
        self.rect.topleft = (0, 0)
        self.scrolling = bg_scroll
        self.scrolled = 0
        # Attribute, die nur für scrollende Hintergründe benötigt werden
        if not self.scrolling == Hintergrund.SCROLL_NO:
            self.image_unscrolled = self.image.copy()
            if self.scrolling == Hintergrund.SCROLL_DOWN:
                self.rect.top = -(self.image.get_height() - SCREEN_HEIGHT)
    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        if self.scrolling == Hintergrund.SCROLL_DOWN:
            self.image.scroll(dy = Hintergrund.SCROLL_SPEED)
            self.scrolled += Hintergrund.SCROLL_SPEED
            # Wenn der Hintergrund am Ende angelangt ist, muss er wieder neu gesetzt werden, hier aus der Kopie des Original Images
            if self.scrolled >= self.image.get_height() - SCREEN_HEIGHT:
                self.image = self.image_unscrolled.copy()
                self.scrolled = 0
class Ship(pygame.sprite.Sprite):
    """
    Dies ist ein Schiff.
    """
    # Variablen
    hp:int = 500 #Gesundheit des Schiffs
    score:int = 0 # Punkte
    highscore:int = 0 # 
    explosion_sound = pygame.mixer.Sound("PlayerEx.mp3")
    explosion_sound.set_volume(1)
    def __init__(self):
        """
        Initialisieren des Schiffs, image und rect setzen.
        """
        super().__init__()
        Ship.hp = 500
        Ship.score = 0    
        self.speed:int = 10 #Geschwindigkeit des Schiffs
        self.shot_cooldown:int = 0 #Cooldown Timer für Schüsse
        self.iframe:int = 0 #Invulnerability Frames
        self._layer = LAYER_SHIP
        _set_image_and_rect(self,"ship.png")
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - (self.rect.height * 2))
    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        global all_sprites
        # Tastenaktionen
        if self.iframe == 0: curr_speed = self.speed
        else: curr_speed = (self.speed // 4)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.left > curr_speed:
                self.rect.x -= curr_speed
        if keys[pygame.K_RIGHT]:
            if self.rect.right < SCREEN_WIDTH - curr_speed:
                self.rect.x += curr_speed
        if keys[pygame.K_UP]:
            if self.rect.top > curr_speed:    
                self.rect.y -= curr_speed
        if keys[pygame.K_DOWN]:
            if self.rect.bottom < SCREEN_HEIGHT - curr_speed:
                self.rect.y += curr_speed
        if keys[pygame.K_LCTRL]:
            if self.shot_cooldown == 0:
                all_sprites.add(Laser(self.rect))
                Laser.laser_sound.play()
                self.shot_cooldown = 5
        # Andere Akionen
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        if self.iframe > 0:
            self.iframe -= 1
        #Kollisionen
        if self.iframe == 0:
            for sprite in all_sprites.sprites():
                if (isinstance(sprite, Enemy) and not sprite.boss) or isinstance(sprite, EnemyLaser):
                    if self.rect.colliderect(sprite.rect):
                        Ship.hp -= sprite.hp
                        Ship.score += sprite.score
                        if (isinstance(sprite, Enemy)): sprite.explosion_sound.play() 
                        sprite.kill()
                elif (isinstance(sprite, Enemy) and sprite.boss):
                    if self.rect.colliderect(sprite.rect):    
                        Ship.hp -= sprite.damage
                        self.iframe = 15
                        _bounce(self,sprite)
            if Ship.hp <= 0:
                self.explosion_sound.play()
                self.kill()
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'EventID': 'GameOver'}))
class Laser(pygame.sprite.Sprite):
    """
    Dies ist ein Laser des Schiffs.
    """
    hp:int = 10  #Gesundheit des Lasers
    speed:int = 15 #Geschwindigkeit des Lasers
    laser_sound = pygame.mixer.Sound("Laser.mp3")
    laser_sound.set_volume(0.10)
    def __init__(self, shiprect:pygame.Rect):
        """
        Initialisieren des Lasers.
        """
        super().__init__()
        self._layer = LAYER_LASER
        _set_image_and_rect(self,"Laser1.png")
        self.rect.bottomleft = (shiprect.left, shiprect.top + 1)
    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        global all_sprites, ship
        self.rect.top -= self.speed
        if self.rect.bottom < 0:
            self.kill()
        else:
            for sprite in all_sprites.sprites():
                if isinstance(sprite, Enemy):
                    if self.rect.colliderect(sprite.rect):
                        sprite.hp -= self.hp
                        if sprite.hp <= 0:
                            Ship.score += sprite.score
                            sprite.explosion_sound.play()
                            sprite.kill()
                            if sprite.boss == True: pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'EventID': 'L1 Complete'}))
                        self.kill()
class Enemy(pygame.sprite.Sprite):
    """
    Hier werden alle Gegner instanziert.
    """
    ENEMY_EINS:int = 1 # Erster Gegner
    ENEMY_ZWEI:int = 2 # Zweiter Gegner
    ENEMY_BOSS_EINS:int = 1001 # Erster Boss
    explosion_sound = pygame.mixer.Sound("EnemyEx.mp3")
    explosion_sound.set_volume(0.25)
    def __init__(self, gegnertyp:int):
        """
        Initialisieren des Gegners.
        """
        super().__init__()
        self._layer = LAYER_ENEMY
        self.gegnertyp = gegnertyp
        if self.gegnertyp == Enemy.ENEMY_EINS:
            _set_image_and_rect(self,"Enemy1.png")
            self.hp = 20
            self.score = 10
            self.laser = (LaserE1,)
            self.fire_rate = 25
            self.boss = False
            self.init = False
            self.bewegung = ((2,2,8),
                             (0,2,8),
                             (-2,2,8),
                             (0,2,8),
                             (-2,2,8),
                             (0,2,8),
                             (2,2,8),
                             (0,2,8))
            self.rect.topleft = (random.randint(0,SCREEN_WIDTH - self.rect.width), 0)
        elif self.gegnertyp == Enemy.ENEMY_ZWEI:
            _set_image_and_rect(self,"Enemy2.png")
            self.hp = 10
            self.score = 5
            self.laser = (LaserE2,LaserE2a,LaserE2b)
            self.fire_rate = 200
            self.boss = False
            self.init = False
            self.bewegung = ((-2,1,20),
                             (-1,1,20),
                             (0,1,10),
                             (1,1,20),
                             (2,1,40),
                             (1,1,20),
                             (0,1,10),
                             (-1,1,20),
                             (-2,1,20))
            self.rect.topleft = (random.randint(0,SCREEN_WIDTH - self.rect.width), 0)
        elif self.gegnertyp == Enemy.ENEMY_BOSS_EINS:
            _set_image_and_rect(self,"EnemyB1.png")
            self.hp = 2000
            self.score = 100
            self.laser = (LaserEB1,)
            self.fire_rate = 100
            self.boss = True
            self.explosion_sound = pygame.mixer.Sound("BossEx.mp3")
            self.explosion_sound.set_volume(0.25)
            self.laser_sound = pygame.mixer.Sound("BossLaser.mp3")
            self.laser_sound.set_volume(0.10)
            self.damage = 50
            self.init = True
            self.speed = 8
            self.bewegung = ((0,self.speed,(SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (0,-self.speed,(SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (-self.speed,0,(SCREEN_WIDTH-self.image.get_width())//(self.speed*2)),
                             (0,self.speed,(SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (0,-self.speed,(SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (self.speed,0,(SCREEN_WIDTH-self.image.get_width())//(self.speed*2)),
                             (0,self.speed,(SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (0,-self.speed,(SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (self.speed,0,(SCREEN_WIDTH-self.image.get_width())//(self.speed*2)),
                             (0,self.speed,(SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (0,-self.speed,(SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (-self.speed,0,(SCREEN_WIDTH-self.image.get_width())//(self.speed*2)))
            self.rect.center = ((SCREEN_WIDTH / 2),1-(self.rect.height/2))
        self.bewegungs_wiederholungen = self.bewegung[0][2]
        self.bewegungs_counter = 0

    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        # Bewegung
        if self.init == False:
            self.rect.x += self.bewegung[self.bewegungs_counter][0]
            self.rect.y += self.bewegung[self.bewegungs_counter][1]
            self.bewegungs_wiederholungen -= 1
            if self.bewegungs_wiederholungen < 1:
                self.bewegungs_counter += 1
                if self.bewegungs_counter >= len(self.bewegung):
                    self.bewegungs_counter = 0
                self.bewegungs_wiederholungen = self.bewegung[self.bewegungs_counter][2]
        else:
            self.rect.y += 2
            if self.rect.top >= 0:
                self.init = False
        #Schuss
        if self.laser != None:
            generate_new_laser = random.randint(0,1000)
            if generate_new_laser < self.fire_rate:
                global all_sprites
                for laser in self.laser:
                    if (self.boss == True): self.laser_sound.play()
                    all_sprites.add(EnemyLaser(self.rect, laser))

        #Tod durch Bildschirmaustritt
        if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()
class EnemyLaser(pygame.sprite.Sprite):
    """
    Dies ist ein Laser eines Gegners.
    """
    score:int = 0
    def __init__(self, enemy_rect:pygame.Rect, enemy_laser:LaserBase):
        """
        Initialisieren des Lasers.
        """
        super().__init__()
        self._layer = LAYER_LASER
        _set_image_and_rect(self,enemy_laser.sprite)
        self.rect.centerx = enemy_rect.centerx
        self.rect.top = enemy_rect.bottom + 1
        self.speed_x = enemy_laser.speed_x
        self.speed_y = enemy_laser.speed_y
        self.hp = enemy_laser.hp
    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        self.rect.top += self.speed_y
        self.rect.left += self.speed_x
        if self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
class UI_Element_Text(pygame.sprite.Sprite):
    """
    Hier werden alle UI Textelemente instanziert.
    """
    #Konstanten
    UI_HP = 0  #Konstante für UI Element Gesundheit
    UI_SCORE = 1 # Konstante für UI Element Score
    def __init__(self, element:int):
        """
        Initialisierung des UI Elements.
        """
        super().__init__()
        self._layer = LAYER_UI
        self.element = element
        self.FONT = pygame.font.Font(None,30)
    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        global ship
        if self.element == UI_Element_Text.UI_HP:
            self.image = self.FONT.render(f"HP: {Ship.hp}",0,(255,255,255),None)
            self.rect = self.image.get_rect()
            self.rect.topleft = (0, 20)
        elif self.element == UI_Element_Text.UI_SCORE:
            self.image = self.FONT.render(f"Punkte: {Ship.score}",0,(255,255,255),None)
            self.rect = self.image.get_rect()
            self.rect.topleft = (0, 0)
def init() -> None:
    """
    Genereller Spielstart.
    """
    if level == 1:
        # Überprüfen, ob die Datei existiert und sie leer ist
        if not os.path.exists("Highscore.bin") or os.path.getsize("Highscore.bin") == 0:
            # Datei existiert nicht oder ist leer, also schreiben wir "0" hinein
            with open("Highscore.bin", 'w') as file:
                file.write("0")
        with open("Highscore.bin", 'r') as file:
            try:
                Ship.highscore  = int(file.read())
                print('Highscore erfolgreich geslesen')
            except:
                Ship.highscore = 0
                print('Highscore manuell auf 0 gesetzt')
        ship = Ship()
    global all_sprites, frame_couter
    frame_couter = 0
    all_sprites.empty()
    all_sprites.add(Hintergrund(Hintergrund.SCROLL_DOWN), ship,UI_Element_Text(UI_Element_Text.UI_HP), UI_Element_Text(UI_Element_Text.UI_SCORE))
def enemy_creation() -> None:
    """
    Hier werden die Gegner erzeugt.
    """
    global all_sprites
    generate_new_enemy = random.randint(0,1000)
    if level == 1:
        if frame_couter < 900:
            if generate_new_enemy < 20:
                all_sprites.add(Enemy(Enemy.ENEMY_EINS))
        elif frame_couter < 3000:
            if generate_new_enemy < 10:
                all_sprites.add(Enemy(Enemy.ENEMY_EINS))
            elif generate_new_enemy < 40:
                all_sprites.add(Enemy(Enemy.ENEMY_ZWEI))
        elif frame_couter == 3300:
            all_sprites.add(Enemy(Enemy.ENEMY_BOSS_EINS))
def set_new_highscore() -> bool:
    try:
        with open("Highscore.bin", 'w') as file:
            file.write(str(Ship.score))
        print("Highscore erfolgreich geupdated")
        return True
    except Exception as e:
        print(f"Highscore nicht erfolgreich geupdated: {e}")
        return False
def _set_image_and_rect(sprite:pygame.sprite.Sprite,image:str,set_colorkey:bool = True,colorkey:tuple[int, int, int] = (255, 255, 255)):
        sprite.image = pygame.image.load(image)
        if set_colorkey:
            sprite.image.set_colorkey(colorkey)
        sprite.rect = sprite.image.get_rect()
def _bounce(weak:pygame.sprite.Sprite,strong:pygame.sprite.Sprite,bounce_x:int = 50, bounce_y:int = 50):
    if weak.rect.centerx < strong.rect.centerx:
        if weak.rect.left > bounce_x: weak.rect.left -= bounce_x
        else: weak.rect.left = 0
    elif weak.rect.centerx > strong.rect.centerx:
        if weak.rect.right < (SCREEN_WIDTH - bounce_x - 1): weak.rect.right += bounce_x
        else: weak.rect.left = (SCREEN_WIDTH - 1)
    if weak.rect.centery < strong.rect.centery:
        if weak.rect.top > bounce_y: weak.rect.top -= bounce_y
        else: weak.rect.top = 0
    elif weak.rect.centery > strong.rect.centery:
        if weak.rect.bottom < (SCREEN_HEIGHT - bounce_y - 1): weak.rect.bottom += bounce_y
        else: weak.rect.bottom = (SCREEN_HEIGHT - 1)
    