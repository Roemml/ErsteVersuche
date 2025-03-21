import pygame

import Global

class Ship(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.HP = Global.shipHP
        self.image = pygame.image.load("Schiffal.png")
        self.rect = self.image.get_rect()
        self.rect.center = (Global.screenWidth / 2,Global.screenHeight - (self.rect.height * 2))
        self.image.set_colorkey((255, 255, 255))

    def update(self):
        # Hier könnte die Bewegung oder andere Logik erfolgen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.x > 2:
                self.rect.x -= 2
        if keys[pygame.K_RIGHT]:
            if self.rect.x < Global.screenWidth - (self.rect.width + 2):
                self.rect.x += 2
        if keys[pygame.K_UP]:
            if self.rect.y > 2:    
                self.rect.y -= 2
        if keys[pygame.K_DOWN]:
            if self.rect.y < Global.screenHeight - (self.rect.height + 2):
                self.rect.y += 2
