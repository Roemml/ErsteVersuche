#Python Imports
import pygame

# Globalle sprites Konstanzen
SCREEN_WIDTH: int = 800 # Breite des Spiel Fensters
SCREEN_HEIGHT: int = 600 # Höhe des Spiel Fensters


# globale sprites Variablen
all_game_sprites: pygame.sprite.Group = pygame.sprite.Group() # Alle Sprites des Spiels selbst
all_hud_sprites: pygame.sprite.Group = pygame.sprite.Group() # Alle Sprites für das HUD

hg: pygame.Surface = None # Hintergrund
ship: pygame.Surface = None # Schiff Sprite


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
    scrolled: int = None #Counter wie weit schon gescrollt wurde
    image_unscrolled: pygame.Surface = None #Kopie des Original Images
    def __init__(self,bg_scroll=SCROLL_NO):
        """
        Konstruktor des Hintergrunds
        """
        super().__init__()
        if not isinstance(bg_scroll, int):
            raise ValueError("bg_scroll muss ein Integer sein!")
        self.image = pygame.image.load("HGTest.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.scrolling = bg_scroll
        # Attribute, die nur für scrollende Hintergründe benötigt werden
        if not self.scrolling == Hintergrund.SCROLL_NO:
            self.scrolled = 0
            self.image_unscrolled =self.image.copy()
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
    UI_HP = 0  #Konstante für UI Element Index
    # Variablen
    image: pygame.Surface = None #Das Hintergrundbild
    rect: pygame.Rect = None #Rechteck kopierziel des Sprites
    hp: int = 500 #Gesundheit des Schiffs
    speed: int = 10 #Geschwindigkeit des Schiffs
    shot_cooldown: int = 0 #Cooldown Timer für Schüsse

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
        # Tastenaktionen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.x > self.speed:
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.rect.x < SCREEN_WIDTH - (self.rect.width + self.speed):
                self.rect.x += self.speed
        if keys[pygame.K_UP]:
            if self.rect.y > self.speed:    
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.rect.y < SCREEN_HEIGHT - (self.rect.height + self.speed):
                self.rect.y += self.speed
        if keys[pygame.K_LCTRL]:
            if self.shot_cooldown == 0:
                global all_game_sprites
                all_game_sprites.add(Laser(self.rect))
                self.shot_cooldown = 5

        if self.shot_cooldown > 0:
            self.shot_cooldown -=1

class Laser(pygame.sprite.Sprite):
    """
    Dies ist ein Laser des Schiffs

    Variablen:
    iamge - Bild wie der Laser ausschaut
    rect - Rechteck wo der Laser gezeichnet werden soll
    HP - Gesundheit
    speed - Bewegungsgeschwindigkeit
    """
    def __init__(self,shiprect: pygame.Rect):
        super().__init__()
        self.image = pygame.image.load("Laser1.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (shiprect.left, shiprect.top + 1)
        self.hp = 10
        self.speed = 15

    def update(self):
        
           # Hintergrund verschieben
           liste = list(self.rect)
           liste[1] = liste[1] - self.speed

           # Wenn das Ende des Hintergrunds erreicht ist, beginne wieder von vorne
           self.rect = tuple(liste)
           if self.rect[1] < 0:
               global all_game_sprites
               all_game_sprites.remove(self)

class UI_Element_Text(pygame.sprite.Sprite):
    """
    Hier werden alle UI Textelemente instanziert
    """
    def __init__(self,element: int):
        super().__init__()
        self.element = element
    
    def update(self):
        global ship
        font = pygame.font.Font(None,20)
        self.image = font.render(f"HP: {ship.hp}",0,(255,255,255),None)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

class Enemy(pygame.sprite.Sprite):
    ENEMY_EINS: int = 0 # Erster Gegner
    def __init__(self,element: int):
        super().__init__()


def init():
    global all_game_sprites, all_hud_sprites,ship, hg
    hg = Hintergrund(Hintergrund.SCROLL_DOWN)
    ship = Ship()
    all_game_sprites.add((hg,ship))
    all_hud_sprites.add(UI_Element_Text(Ship.UI_HP))