import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

all_game_sprites = pygame.sprite.Group()

class Hintergrund(pygame.sprite.Sprite):
    """
    Der Hintergrund bzw doppelt Hintergrund 1 und zwei wenn scrollend
    
    Variablen:
    image - Hintergrundbild selbst
    rect - Rechteck wo der Hintergrund gezeichnet werden soll
    einsOderZwei - 0 wenn fixer Hintergrund, ansonsten 1 und 2 für die beiden Hintergründe zum scrollen
    Variablen bei einsOderZwei != 0:
    height - die Höhe des Sprites
    speed - Scrollspeed
    """
    #init für einen fixen Sprite
    def __init__(self): 
        super().__init__()
        self.image = pygame.image.load("HGTest.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.einsOderZwei = 0

    #Scroll Hintergrund muss zwei mal erzeigt werden damit es mit der Methode klappt    
    def __init__(self,einsOderZwei):
        super().__init__()
        if einsOderZwei != 1 and einsOderZwei != 2:
            raise ValueError("einsOderZwei darf auch nur eins oder zwei sein!")
        self.einsOderZwei = einsOderZwei
        self.image = pygame.image.load("HGTest.png")
        self.height = self.image.get_height()
        self.speed = 15
        if einsOderZwei == 1:
            self.rect = (0,-self.height)
        else:
            self.rect = (0,0)
    
    def update(self):
        if self.einsOderZwei != 0:
            # Hintergrund verschieben
            # liste = list(self.rect)
            # liste[1] = liste[1] + self.speed

            # # Wenn das Ende des Hintergrunds erreicht ist, beginne wieder von vorne
            # if self.einsOderZwei == 1 and liste[1] >= 0:
            #     liste[1] = -self.height
            # if self.einsOderZwei == 2 and liste[1] >= self.height:
            #     liste[1] = 0
            # self.rect = tuple(liste)
            x, y = self.rect
            y += self.speed
            if self.einsOderZwei == 1 and y >= 0:
                 y = -self.height
            if self.einsOderZwei == 2 and y >= self.height:
                y = 0
            self.rect = (x, y)

class Ship(pygame.sprite.Sprite):
    """
    Dies ist ein Schiff

    Variablen:
    iamge - Bild wie das Schiff ausschaut
    rect - Rechteck wo das Schiff gezeichnet werden soll
    HP - Gesundheit
    speed - Bewegungsgeschwindigkeit
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ship.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - (self.rect.height * 2))
        self.HP = 500
        self.speed = 10
        self.shot_cooldown = 0

        global all_game_sprites
        #all_sprites.add(self)
        

    def update(self):
        # Hier könnte die Bewegung oder andere Logik erfolgen
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
            #else:
             #   print("Pause")

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
        self.HP = 10
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

def init():
    global all_game_sprites
    all_game_sprites.add((Hintergrund(1), Hintergrund(2), Ship()))