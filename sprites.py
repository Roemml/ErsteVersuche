#Python Imports
import pygame
import random
import os
# Globale Konstanzen
SCREEN_WIDTH:int = 800 # Breite des Spiel Fensters
SCREEN_HEIGHT:int = 600 # Höhe des Spiel Fensters
LAYER_HG:int = 0 #Hintergründe sind ganz im Hintergrund
LAYER_ENEMY:int = 1 #Enemy Layer
LAYER_SHIP:int = 2 #Schill Layer
LAYER_LASER:int = 3 #Laser layer
LAYER_UI:int = 4 #Layer User Interface
# Globale Variablen
all_sprites:pygame.sprite.LayeredUpdates = pygame.sprite.LayeredUpdates() # Alle Sprites des Spiels selbst
frame_couter:int = 0 #Framecounter
#Klassen
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
        self.image = pygame.image.load("HGTest.png")
        self.rect = self.image.get_rect()
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
    hp:int = 50 #Gesundheit des Schiffs
    speed:int = 10 #Geschwindigkeit des Schiffs
    shot_cooldown:int = 0 #Cooldown Timer für Schüsse
    score:int = 0 # Punkte
    highscore:int = 0 # Punkte 
    def __init__(self):
        """
        Initialisieren des Schiffs, image und rect setzen.
        """
        super().__init__()
        self._layer = LAYER_SHIP
        self.image = pygame.image.load("ship.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - (self.rect.height * 2))
    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        global all_sprites
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
                all_sprites.add(Laser(self.rect))
                self.shot_cooldown = 5
        # Andere Akionen
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        #Kollisionen
        for sprite in all_sprites.sprites():
            if isinstance(sprite, Enemy) or isinstance(sprite, EnemyLaser):
                if self.rect.colliderect(sprite.rect):
                    self.hp -= sprite.hp
                    Ship.score += sprite.score
                    sprite.kill()
                    if self.hp <= 0:
                        self.kill()
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'EventID': 'GameOver'}))
class Laser(pygame.sprite.Sprite):
    """
    Dies ist ein Laser des Schiffs.
    """
    hp:int = 10  #Gesundheit des Lasers
    speed:int = 15 #Geschwindigkeit des Lasers
    def __init__(self, shiprect:pygame.Rect):
        """
        Initialisieren des Lasers.
        """
        super().__init__()
        self._layer = LAYER_LASER
        self.image = pygame.image.load("Laser1.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
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
                            sprite.kill()
                        self.kill()
class Enemy(pygame.sprite.Sprite):
    """
    Hier werden alle Gegner instanziert.
    """
    ENEMY_EINS:int = 0 # Erster Gegner
    def __init__(self, gegnertyp:int):
        """
        Initialisieren des Gegners.
        """
        super().__init__()
        self._layer = LAYER_ENEMY
        self.gegnertyp = gegnertyp
        if self.gegnertyp == Enemy.ENEMY_EINS:
            self.image = pygame.image.load("Enemy1.png")
            self.image.set_colorkey((255, 255, 255))
            self.hp = 20
            self.score = 10
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
        self.bewegungs_counter = 0

    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        global all_sprites
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
            all_sprites.add(EnemyLaser(self.rect))
        if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()
class EnemyLaser(pygame.sprite.Sprite):
    """
    Dies ist ein Laser eines Gegners.
    """
    score:int = 0
    hp:int = 10  #Gesundheit des Lasers
    def __init__(self, enemyrect:pygame.Rect, speed:int = 10):
        """
        Initialisieren des Lasers.
        """
        super().__init__()
        self._layer = LAYER_LASER
        self.image = pygame.image.load("LaserE.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (enemyrect.left, enemyrect.bottom + 1)
        self.speed = speed
    def update(self) -> None:
        """
        Updatemethode für Handling über eine Sprite Gruppe.
        """
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT:
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
    global all_sprites
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
    all_sprites.add(Hintergrund(Hintergrund.SCROLL_DOWN), ship,UI_Element_Text(UI_Element_Text.UI_HP), UI_Element_Text(UI_Element_Text.UI_SCORE))
def enemy_creation() -> None:
    """
    Hier werden die Gegner erzeugt.
    """
    global all_sprites
    generate_new_enemy = random.randint(0,1000)
    if generate_new_enemy < 20 * ( 1 + (frame_couter // 600)):
        all_sprites.add(Enemy(Enemy.ENEMY_EINS))
def set_new_highscore() -> bool:
    try:
        with open("Highscore.bin", 'w') as file:
            file.write(str(Ship.score))
        print("Highscore erfolgreich geupdated")
        return True
    except Exception as e:
        print(f"Highscore nicht erfolgreich geupdated: {e}")
        return False