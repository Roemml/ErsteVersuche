import pygame

import Global

class Hintergrund(pygame.sprite.Sprite):

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
        if einsOderZwei == 1:
            self.rect = (0,-self.height)
        else:
            self.rect = (0,0)

    
    def update(self):
        if self.einsOderZwei != 0:
            # Hintergrund verschieben
            liste = list(self.rect)
            liste[1] = liste[1] + Global.scrollSpeed

            # Wenn das Ende des Hintergrunds erreicht ist, beginne wieder von vorne
            if self.einsOderZwei == 1 and liste[1] >= 0:
                liste[1] = -self.height
            if self.einsOderZwei == 2 and liste[1] >= self.height:
                liste[1] = 0
            self.rect = tuple(liste)