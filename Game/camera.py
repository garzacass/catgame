import pygame
vec = pygame.math.Vector2
from abc import ABC, abstractmethod #lets us create scroll methods

class Camera:
    def __init__(self,player):
        self.player = player
        self.offset = vec(0,0) #used to frame camera (int)
        self.offset_float = vec(0,0) #precise value
        self.DISPLAY_W, self.DISPLAY_H = 700,600
        self.CONST = vec(-self.DISPLAY_W/2 + player.rect.w/2, -550 + 20)

    def setmethod(self,method):
        self.method = method
    
    def scroll(self):
        self.method.scroll()

class CamScroll(ABC):
    def __init__(self,camera,player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass

#different scrolling methods: follow character or auto scroll
class Follow(CamScroll):
    def __init__(self,camera,player):
        CamScroll.__init__(self,camera,player)
    
    def scroll(self):
        #chase the player
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), 0


class Auto(CamScroll):
    def __init__(self,camera,player):
        CamScroll.__init__(self,camera,player)

    def scroll(self):
        self.camera.offset.x += 1