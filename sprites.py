#Python Imports
import pygame
import random

#Eigene Imports

# Globalle sprites Konstanzen
SCREEN_WIDTH: int = 800 # Breite des Spiel Fensters
SCREEN_HEIGHT: int = 600 # Höhe des Spiel Fensters

# globale sprites Variablen
all_game_sprites: pygame.sprite.Group = pygame.sprite.Group() # Alle Sprites des Spiels selbst
all_hud_sprites: pygame.sprite.Group = pygame.sprite.Group() # Alle Sprites für das HUD

hg: pygame.Surface = None # Hintergrund
ship: pygame.Surface = None # Schiff Sprite
frame_couter: int = 0 #Framecounter

class Hintergrund(pygame.sprite.Sprite):
    """
    Der Hintergrund des Spiels
    """
    # Konstanten
    SCROLL_NO: int = 0 # Der Hintergrund ist statisch
    SCROLL_DOWN: int = 1 # Her Hintergrund scrollt nach unten, man bewegt sich nach oben
    SCROLL_SPEED: int = 15 # Scrollgeschwindigkeit
    # Variablen
    image: pygame.Surface = None #Das Hintergrundbild
    rect: pygame.Rect = None #Rechteck kopierziel des Sprites
    scrolling: int = None #Art des Scrolling
    scrolled: int = 0 #Counter wie weit schon gescrollt wurde
    image_unscrolled: pygame.Surface = None #Kopie des Original Images
    def __init__(self,bg_scroll: int=SCROLL_NO):
        """
        Konstruktor des Hintergrunds
        """
        super().__init__()
        self.image = pygame.image.load("HGTest.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.scrolling = bg_scroll
        # Attribute, die nur für scrollende Hintergründe benötigt werden
        if not self.scrolling == Hintergrund.SCROLL_NO:
            self.image_unscrolled =self.image.copy()
            if self.scrolling == Hintergrund.SCROLL_DOWN:
                self.rect.top =-(self.image.get_height() - SCREEN_HEIGHT)
    def update(self):
        """
        Updatemethode für Handling über eine Sprite Gruppe
        """
        if self.scrolling == Hintergrund.SCROLL_DOWN:
            self.image.scroll(dy=Hintergrund.SCROLL_SPEED)
            self.scrolled += Hintergrund.SCROLL_SPEED
            # Wenn der Hintergrund am Ende angelangt ist, muss er wieder neu gesetzt werden, hier aus der Kopie des Original Images
            if self.scrolled >= self.image.get_height() - SCREEN_HEIGHT:
                self.image = self.image_unscrolled.copy()
                self.scrolled = 0
class Ship(pygame.sprite.Sprite):
    """
    Dies ist ein Schiff
    """
    #Konstanten
    UI_HP = 0  #Konstante für UI Element Gesundheit
    UI_SCORE = 1 # Konstante für UI Element Score
    # Variablen
    image: pygame.Surface = None #Das Schiff
    rect: pygame.Rect = None #Rechteck kopierziel des Sprites
    hp: int = 500 #Gesundheit des Schiffs
    speed: int = 10 #Geschwindigkeit des Schiffs
    shot_cooldown: int = 0 #Cooldown Timer für Schüsse
    score: int = 0 # Punkte
    def __init__(self):
        """
        Initialisieren des Schiffs, image und rect setzen
        """
        super().__init__()
        self.image = pygame.image.load("ship.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - (self.rect.height * 2))
    def update(self):
        """
        Updatemethode für Handling über eine Sprite Gruppe
        """
        global all_game_sprites
        # Tastenaktionen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.left > self.speed:
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.rect.right < SCREEN_WIDTH - self.speed:
                self.rect.x += self.speed
        if keys[pygame.K_UP]:
            if self.rect.top > self.speed:    
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.rect.bottom < SCREEN_HEIGHT - self.speed:
                self.rect.y += self.speed
        if keys[pygame.K_LCTRL]:
            if self.shot_cooldown == 0:
                
                all_game_sprites.add(Laser(self.rect))
                self.shot_cooldown = 5
        # Andere Akionen
        if self.shot_cooldown > 0:
            self.shot_cooldown -=1
        #Kollisionen
        for sprite in all_game_sprites.sprites():
            if isinstance(sprite, Enemy) or isinstance(sprite, EnemyLaser):
                if self.rect.colliderect(sprite.rect):
                    self.hp -= sprite.hp
                    self.score += sprite.score
                    all_game_sprites.remove(sprite)
                    if self.hp <= 0:
                        all_game_sprites.remove(self)
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'EventID': 'GameOver'}))
class Laser(pygame.sprite.Sprite):
    """
    Dies ist ein Laser des Schiffs
    """
    image: pygame.Surface = None #Der Laser
    rect: pygame.Rect = None #Rechteck kopierziel des Sprites
    hp: int = 10  #Gesundheit des Lasers
    speed: int = 15 #Geschwindigkeit des Lasers
    def __init__(self,shiprect: pygame.Rect):
        """
        Initialisieren des lasers
        """
        super().__init__()
        self.image = pygame.image.load("Laser1.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (shiprect.left, shiprect.top + 1)
    def update(self):
        """
        Updatemethode für Handling über eine Sprite Gruppe
        """
        global all_game_sprites, ship
        self.rect.top -= self.speed
        if self.rect.bottom < 0:
            all_game_sprites.remove(self)
        else:
            for sprite in all_game_sprites.sprites():
                if isinstance(sprite, Enemy):
                    if self.rect.colliderect(sprite.rect):
                        sprite.hp -= self.hp
                        if sprite.hp <= 0:
                            ship.score += sprite.score
                            all_game_sprites.remove(sprite)
                        all_game_sprites.remove(self)
class Enemy(pygame.sprite.Sprite):
    """
    Hier werden alle Gegner instanziert
    """
    ENEMY_EINS: int = 0 # Erster Gegner
    gegnertyp: int = None # Gegnertyp
    image: pygame.Surface = None #Der Gegner
    rect: pygame.Rect = None #Rechteck kopierziel des Sprites
    hp: int = None #Gesundheit des Gegners
    score: int = 0 #Punkte für das Töten des Gegners
    bewegung = None #Tupel and X:Y Tupel für die Bewegungssteuerung
    bewegungs_counter: int = 0 #der Counter für die Bewegungssteuerung
    bewegungs_wiederholungen: int = None # wie oft soll die selbe Bewegung noch wiederholt werden? 
    def __init__(self,gegnertyp: int):
        """
        Initialisieren des Gegners
        """
        super().__init__()
        self.gegnertyp = gegnertyp
        if self.gegnertyp == Enemy.ENEMY_EINS:
            self.image = pygame.image.load("Enemy1.png")
            self.image.set_colorkey((255, 255, 255))
            self.hp = 20
            self.score =10
            self.bewegung = ((2,2,8),
                             (0,2,8),
                             (-2,2,8),
                             (0,2,8),
                             (-2,2,8),
                             (0,2,8),
                             (2,2,8),
                             (0,2,8))
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0,SCREEN_WIDTH - self.rect.width), 0)
        self.bewegungs_wiederholungen = self.bewegung[0][2]

    def update(self):
        global all_game_sprites
        self.rect.x += self.bewegung[self.bewegungs_counter][0]
        self.rect.y += self.bewegung[self.bewegungs_counter][1]
        self.bewegungs_wiederholungen -= 1
        if self.bewegungs_wiederholungen < 1:
            self.bewegungs_counter += 1
            if self.bewegungs_counter >= len(self.bewegung):
                self.bewegungs_counter = 0
            self.bewegungs_wiederholungen = self.bewegung[self.bewegungs_counter][2]
        
        generate_new_laser = random.randint(0,1000)
        if generate_new_laser < 50:
            all_game_sprites.add(EnemyLaser(self.rect))
        if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            all_game_sprites.remove(self)
class EnemyLaser(pygame.sprite.Sprite):
    """
    Dies ist ein Laser eines Gegners
    """
    score: int = 0
    image: pygame.Surface = None #Der Laser
    rect: pygame.Rect = None #Rechteck kopierziel des Sprites
    hp: int = 10  #Gesundheit des Lasers
    speed: int = 15 #Geschwindigkeit des Lasers
    def __init__(self,enemyrect: pygame.Rect):
        """
        Initialisieren des lasers
        """
        super().__init__()
        self.image = pygame.image.load("LaserE.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (enemyrect.left, enemyrect.bottom +  1)
    def update(self):
        """
        Updatemethode für Handling über eine Sprite Gruppe
        """
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            global all_game_sprites
            all_game_sprites.remove(self)

class UI_Element_Text(pygame.sprite.Sprite):
    """
    Hier werden alle UI Textelemente instanziert
    """
    element: int = None # Das Element des UIs
    FONT: pygame.font.Font = None #Font für die Schrift
    def __init__(self,element: int):
        super().__init__()
        self.element = element
        self.FONT = pygame.font.Font(None,30)
    def update(self):
        """
        Updatemethode für Handling über eine Sprite Gruppe
        """
        global ship
        if self.element == Ship.UI_HP:
            self.image = self.FONT.render(f"HP: {ship.hp}",0,(255,255,255),None)
            self.rect = self.image.get_rect()
            self.rect.topleft = (0, 20)
        elif self.element == Ship.UI_SCORE:
            self.image = self.FONT.render(f"Punkte: {ship.score}",0,(255,255,255),None)
            self.rect = self.image.get_rect()
            self.rect.topleft = (0, 0)
def init():
    global hg,ship,all_game_sprites,all_hud_sprites
    hg = Hintergrund(Hintergrund.SCROLL_DOWN)
    ship = Ship()
    all_game_sprites.add((hg,ship))
    all_hud_sprites.add(UI_Element_Text(Ship.UI_HP), UI_Element_Text(Ship.UI_SCORE))
def enemy_creation():
    global all_game_sprites
    generate_new_enemy = random.randint(0,1000)
    if generate_new_enemy < 20 * ( 1 + (frame_couter // 3600)):
        all_game_sprites.add(Enemy(Enemy.ENEMY_EINS))