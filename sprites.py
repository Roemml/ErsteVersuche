#Python Imports
import pygame
import random
import os
#Eigene Imports
import Roemdules.mp3 as mp3
pygame.init()
class Sprites:
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "")
    SCREEN_WIDTH:int = 1200 # Breite des Spiel Fensters
    SCREEN_HEIGHT:int = 900 # Höhe des Spiel Fensters
    ####################################################################
    LAYER_HG:int = 0 #Hintergründe sind ganz im Hintergrund
    LAYER_ENEMY:int = 1 #Enemy Layer
    LAYER_SHIP:int = 2 #Schill Layer
    LAYER_LASER:int = 3 #Laser layer
    LAYER_UI:int = 4 #Layer User Interface
    ####################################################################
    all_sprites:pygame.sprite.LayeredUpdates = pygame.sprite.LayeredUpdates() # Alle Sprites des Spiels selbst
    pause_sprites:pygame.sprite.LayeredUpdates = pygame.sprite.LayeredUpdates() # für Pause Update
    level:int = 1 # Level
    frame_counter:int = 0 #Framecounter
    screen:pygame.Surface = None
    pause1 = None
    pause2 = None
#Enemy Laser Definitionen
class LaserBase:
    sprite:str = ""
    speed_x:int = 0
    speed_y:int = 0
    hp:int = 0
    fire_rate:int = 0
class LaserE1(LaserBase):
    sprite:str = f"{Sprites.DATA_DIR}LaserE1.png"
    speed_x:int = 0
    speed_y:int = 10
    hp:int = 10
class LaserE2(LaserBase):
    sprite:str = f"{Sprites.DATA_DIR}LaserE2.png"
    speed_x:int = 0
    speed_y:int = 20
    hp:int = 5
class LaserE2a(LaserE2):
    speed_x:int = -20
class LaserE2b(LaserE2):
    speed_x:int = +20
class LaserEB1(LaserBase):
    sprite:str = f"{Sprites.DATA_DIR}LaserEB1.png"
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
    SCROLL_SPEED:int = 10 # Scrollgeschwindigkeit
    def __init__(self, bg_scroll:int = SCROLL_NO):
        """
        Konstruktor des Hintergrunds.
        """
        super().__init__()
        self._layer = Sprites.LAYER_HG
        _set_image_and_rect(self,f"{Sprites.DATA_DIR}HG{Sprites.level}.png",False)
        self.rect.topleft = (0, 0)
        self.scrolling = bg_scroll
        self.scrolled = 0
        # Attribute, die nur für scrollende Hintergründe benötigt werden
        if not self.scrolling == Hintergrund.SCROLL_NO:
            self.image_unscrolled = self.image.copy()
            if self.scrolling == Hintergrund.SCROLL_DOWN:
                self.rect.top = -(self.image.get_height() - Sprites.SCREEN_HEIGHT)
    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        if self.scrolling == Hintergrund.SCROLL_DOWN:
            self.image.scroll(dy = Hintergrund.SCROLL_SPEED)
            self.scrolled += Hintergrund.SCROLL_SPEED
            # Wenn der Hintergrund am Ende angelangt ist, muss er wieder neu gesetzt werden, hier aus der Kopie des Original Images
            if self.scrolled >= self.image.get_height() - Sprites.SCREEN_HEIGHT:
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
    explosion_sound = pygame.mixer.Sound(f"{Sprites.DATA_DIR}PlayerEx.mp3")
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
        self._layer = Sprites.LAYER_SHIP
        _set_image_and_rect(self,f"{Sprites.DATA_DIR}ship.png")
        self.rect.center = (Sprites.SCREEN_WIDTH / 2, Sprites.SCREEN_HEIGHT - (self.rect.height * 2))
    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        # Tastenaktionen
        if self.iframe == 0: curr_speed = self.speed
        else: curr_speed = (self.speed // 4)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.left > curr_speed:
                self.rect.x -= curr_speed
        if keys[pygame.K_RIGHT]:
            if self.rect.right < Sprites.SCREEN_WIDTH - curr_speed:
                self.rect.x += curr_speed
        if keys[pygame.K_UP]:
            if self.rect.top > curr_speed:    
                self.rect.y -= curr_speed
        if keys[pygame.K_DOWN]:
            if self.rect.bottom < Sprites.SCREEN_HEIGHT - curr_speed:
                self.rect.y += curr_speed
        if keys[pygame.K_LCTRL]:
            if self.shot_cooldown == 0:
                Sprites.all_sprites.add(Laser(self.rect))
                Laser.laser_sound.play()
                self.shot_cooldown = 4
        # Andere Akionen
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        if self.iframe > 0:
            self.iframe -= 1
        #Kollisionen
        if self.iframe == 0:
            for sprite in Sprites.all_sprites.sprites():
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
    speed:int = 20 #Geschwindigkeit des Lasers
    laser_sound = pygame.mixer.Sound(f"{Sprites.DATA_DIR}Laser.mp3")
    laser_sound.set_volume(0.10)
    def __init__(self, shiprect:pygame.Rect):
        """
        Initialisieren des Lasers.
        """
        super().__init__()
        self._layer = Sprites.LAYER_LASER
        _set_image_and_rect(self,f"{Sprites.DATA_DIR}Laser1.png")
        self.rect.bottomleft = (shiprect.left, shiprect.top + 1)
    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        self.rect.top -= self.speed
        if self.rect.bottom < 0:
            self.kill()
        else:
            for sprite in Sprites.all_sprites.sprites():
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
    explosion_sound = pygame.mixer.Sound(f"{Sprites.DATA_DIR}EnemyEx.mp3")
    explosion_sound.set_volume(0.25)
    def __init__(self, gegnertyp:int):
        """
        Initialisieren des Gegners.
        """
        super().__init__()
        self._layer = Sprites.LAYER_ENEMY
        self.gegnertyp = gegnertyp
        if self.gegnertyp == Enemy.ENEMY_EINS:
            _set_image_and_rect(self,f"{Sprites.DATA_DIR}Enemy1.png")
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
            self.rect.topleft = (random.randint(0,Sprites.SCREEN_WIDTH - self.rect.width), 0)
        elif self.gegnertyp == Enemy.ENEMY_ZWEI:
            _set_image_and_rect(self,f"{Sprites.DATA_DIR}Enemy2.png")
            self.hp = 10
            self.score = 5
            self.laser = (LaserE2,LaserE2a,LaserE2b)
            self.fire_rate = 75
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
            self.rect.topleft = (random.randint(0,Sprites.SCREEN_WIDTH - self.rect.width), 0)
        elif self.gegnertyp == Enemy.ENEMY_BOSS_EINS:
            _set_image_and_rect(self,f"{Sprites.DATA_DIR}EnemyB1.png")
            self.hp = 2000
            self.score = 100
            self.laser = (LaserEB1,)
            self.fire_rate = 100
            self.boss = True
            self.explosion_sound = pygame.mixer.Sound(f"{Sprites.DATA_DIR}BossEx.mp3")
            self.explosion_sound.set_volume(0.25)
            self.laser_sound = pygame.mixer.Sound(f"{Sprites.DATA_DIR}BossLaser.mp3")
            self.laser_sound.set_volume(0.10)
            self.damage = 50
            self.init = True
            self.speed = 8
            self.bewegung = ((0,self.speed,(Sprites.SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (0,-self.speed,(Sprites.SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (-self.speed,0,(Sprites.SCREEN_WIDTH-self.image.get_width())//(self.speed*2)),
                             (0,self.speed,(Sprites.SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (0,-self.speed,(Sprites.SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (self.speed,0,(Sprites.SCREEN_WIDTH-self.image.get_width())//(self.speed*2)),
                             (0,self.speed,(Sprites.SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (0,-self.speed,(Sprites.SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (self.speed,0,(Sprites.SCREEN_WIDTH-self.image.get_width())//(self.speed*2)),
                             (0,self.speed,(Sprites.SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (0,-self.speed,(Sprites.SCREEN_HEIGHT-self.image.get_height())//self.speed ),
                             (-self.speed,0,(Sprites.SCREEN_WIDTH-self.image.get_width())//(self.speed*2)))
            self.rect.center = ((Sprites.SCREEN_WIDTH / 2),1-(self.rect.height/2))
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
                for laser in self.laser:
                    if (self.boss == True): self.laser_sound.play()
                    Sprites.all_sprites.add(EnemyLaser(self.rect, laser))

        #Tod durch Bildschirmaustritt
        if self.rect.top > Sprites.SCREEN_HEIGHT or self.rect.bottom < 0 or self.rect.left > Sprites.SCREEN_WIDTH or self.rect.right < 0:
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
        self._layer = Sprites.LAYER_LASER
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
        if self.rect.top > Sprites.SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > Sprites.SCREEN_WIDTH:
            self.kill()
class UI_Element_Text(pygame.sprite.Sprite):
    """
    Hier werden alle UI Textelemente instanziert.
    """
    #Konstanten
    UI_HP = 0  #Konstante für UI Element Gesundheit
    UI_SCORE = 1 # Konstante für UI Element Score
    UI_PAUSE1 = 2 #Konstante Für das UI Element PAUSE1
    UI_PAUSE2 = 3 #Konstante Für das UI Element PAUS2E
    def _get_color_by_bits(colorbit:int) ->  tuple[int, int, int]:
        if colorbit < 0 or colorbit > 7:
            raise Exception("Input int darf nur zwischen 0 und 7 liegen")
        color_string = f"{colorbit:03b}"
        r = 255 * int(color_string[0:1])
        g = 255 * int(color_string[1:2])
        b = 255 * int(color_string[2:3])
        return (r, g, b)
    def __init__(self, element:int):
        """
        Initialisierung des UI Elements.
        """
        super().__init__()
        self._layer = Sprites.LAYER_UI
        self.element = element
        self.FONT = pygame.font.Font(None,30)
        if self.element == UI_Element_Text.UI_PAUSE1 or self.element == UI_Element_Text.UI_PAUSE2:
            self.FONT = pygame.font.Font(None,60)
            self.pause_counter = 0
            self.colorbit = 7
            self.color = UI_Element_Text._get_color_by_bits(self.colorbit)
            if self.element == UI_Element_Text.UI_PAUSE1:
                self.image = self.FONT.render("PAUSE",0,self.color ,None)
                self.y = 400
            elif self.element == UI_Element_Text.UI_PAUSE2:
                self.image = self.FONT.render("P für weiterspielen",0,self.color,None)
                self.y = 500
            self.rect = self.image.get_rect()
            self.rect.topleft = ((Sprites.SCREEN_WIDTH - self.rect.width) / 2, self.y)
    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        if self.element == UI_Element_Text.UI_HP:
            self.image = self.FONT.render(f"HP: {Ship.hp}",0,(255,255,255),None)
            self.rect = self.image.get_rect()
            self.rect.topleft = (0, 20)
        elif self.element == UI_Element_Text.UI_SCORE:
            self.image = self.FONT.render(f"Punkte: {Ship.score}",0,(255,255,255),None)
            self.rect = self.image.get_rect()
            self.rect.topleft = (0, 0)
        elif self.element == UI_Element_Text.UI_PAUSE1 or self.element == UI_Element_Text.UI_PAUSE2:
            if self.pause_counter >= 10:
                self.pause_counter = 0
                self.colorbit = 7 if self.colorbit == 0 else self.colorbit - 1
                self.color = UI_Element_Text._get_color_by_bits(self.colorbit)
            else:
                self.pause_counter += 1
            if self.element == UI_Element_Text.UI_PAUSE1:
                self.image = self.FONT.render("PAUSE",0,self.color,None)
            elif self.element == UI_Element_Text.UI_PAUSE2:
                self.image = self.FONT.render("P für weiterspielen",0,self.color,None)
    def init(self) -> None:
        if self.element == UI_Element_Text.UI_PAUSE1 or self.element == UI_Element_Text.UI_PAUSE2:
            self.pause_counter = 0
            self.colorbit = 7
            self.color = UI_Element_Text._get_color_by_bits(self.colorbit)
def init() -> None:
    """
    Genereller Spielstart.
    """
    if Sprites.screen is None:
        Sprites.screen = pygame.display.set_mode((Sprites.SCREEN_WIDTH, Sprites.SCREEN_HEIGHT))
        pygame.display.set_icon(pygame.image.load(f"{Sprites.DATA_DIR}Gameico.png"))
        pygame.display.set_caption("2D Power")
    if Sprites.pause1 is None: 
        Sprites.pause1 = UI_Element_Text(UI_Element_Text.UI_PAUSE1)
    if Sprites.pause2 is None: 
        Sprites.pause2 = UI_Element_Text(UI_Element_Text.UI_PAUSE2)
    if Sprites.level == 1:
        # Überprüfen, ob die Datei existiert und sie leer ist
        if not os.path.exists(f"{Sprites.DATA_DIR}Highscore.bin") or os.path.getsize(f"{Sprites.DATA_DIR}Highscore.bin") == 0:
            # Datei existiert nicht oder ist leer, also schreiben wir "0" hinein
            with open(f"{Sprites.DATA_DIR}Highscore.bin", 'wb') as file:
                file.write(int("0").to_bytes(1, byteorder="big"))
        with open(f"{Sprites.DATA_DIR}Highscore.bin", 'rb') as file:
            try:
                Ship.highscore  = int.from_bytes(file.readline(), byteorder="big")
                print('Highscore erfolgreich geslesen')
            except:
                Ship.highscore = 0
                print('Highscore manuell auf 0 gesetzt')
        ship = Ship()
    Sprites.frame_counter = 0
    Sprites.all_sprites.empty()
    Sprites.all_sprites.add(Hintergrund(Hintergrund.SCROLL_DOWN), ship,UI_Element_Text(UI_Element_Text.UI_HP), UI_Element_Text(UI_Element_Text.UI_SCORE))
def enemy_creation() -> None:
    """
    Hier werden die Gegner erzeugt.
    """
    generate_new_enemy = random.randint(0,1000)
    if Sprites.level == 1:
        if Sprites.frame_counter < 900:
            if generate_new_enemy < 20:
                Sprites.all_sprites.add(Enemy(Enemy.ENEMY_EINS))
        elif Sprites.frame_counter < 3000:
            if generate_new_enemy < 10:
                Sprites.all_sprites.add(Enemy(Enemy.ENEMY_EINS))
            elif generate_new_enemy < 30:
                Sprites.all_sprites.add(Enemy(Enemy.ENEMY_ZWEI))
        elif Sprites.frame_counter == 3500:
            Sprites.all_sprites.add(Enemy(Enemy.ENEMY_BOSS_EINS))
def pause() -> None:
    Sprites.pause1.init();Sprites.pause2.init()
    Sprites.all_sprites.add(Sprites.pause1,Sprites.pause2)
    Sprites.pause_sprites.add(Sprites.pause1,Sprites.pause2)
def resume() -> None:
    Sprites.pause1.kill()
    Sprites.pause2.kill()
def update(running:bool = True):
    if running:
        enemy_creation()
        Sprites.all_sprites.update()
        Sprites.frame_counter += 1
    else:
        Sprites.pause_sprites.update()
    Sprites.screen.fill((0, 0, 0))
    Sprites.all_sprites.draw(Sprites.screen)
    pygame.display.flip()
    # pygame.time.Clock().tick(60)
def set_new_highscore() -> bool:
    try:
        with open(f"{Sprites.DATA_DIR}Highscore.bin", 'wb') as file:
            file.write(Ship.score.to_bytes((Ship.score.bit_length()+7)//8, byteorder="big"))
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
        if weak.rect.right < (Sprites.SCREEN_WIDTH - bounce_x - 1): weak.rect.right += bounce_x
        else: weak.rect.left = (Sprites.SCREEN_WIDTH - 1)
    if weak.rect.centery < strong.rect.centery:
        if weak.rect.top > bounce_y: weak.rect.top -= bounce_y
        else: weak.rect.top = 0
    elif weak.rect.centery > strong.rect.centery:
        if weak.rect.bottom < (Sprites.SCREEN_HEIGHT - bounce_y - 1): weak.rect.bottom += bounce_y
        else: weak.rect.bottom = (Sprites.SCREEN_HEIGHT - 1)
    