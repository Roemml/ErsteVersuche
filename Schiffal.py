import pygame

class Schiffal(pygame.sprite.Sprite):

    def __init__(self, HP, x, y):
        super().__init__()
        self.HP = HP
        self.image = pygame.image.load("Schiffal.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.image.set_colorkey((255, 255, 255))

    def update(self):
        # Hier könnte die Bewegung oder andere Logik erfolgen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5
