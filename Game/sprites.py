# Classes for game
import pygame as pg
from settings import *

## CHARACTER ##
class Kitty(pg.sprite.Sprite):
    def __init__(self,game,w,h,img_path):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w,h))
        self.image = pg.image.load(img_path)
        self.image = pg.transform.scale(self.image, (w,h))
        self.rect = self.image.get_rect()
        
        #starting position
        self.rect.center = (350,550)
        self.score = 0
        self.on_ground = True
        self.jumping = False
        
        #animation
        self.FACING_LEFT = False
        self.animation_steps = [1,1,4,4,5,5]
        self.animation_list = []
        self.frame = 0
        self.last_update = 0
        #self.states = {'idleright':0, 'idleleft':1, 'walkright':2, 'walkleft':3, 'jumpright':4, 'jumpleft':5}
        self.state = 'idleright'
        self.load_frames()
        
        #Speed/moving
        self.vx = 0
        self.vy = 0
        
        #jumping
        self.jump_start = 0
        self.jump_duration = 200
        self.gravity = 5

    
    def load_frames(self):
        #load sprite sheets
        cat_spritesheetwalkright = Spritesheet('/Users/cass/Downloads/OOP/Catgameprogress/images/catrightwalk.png') 
        cat_spritesheetwalkleft = Spritesheet('/Users/cass/Downloads/OOP/Catgameprogress/images/catleftwalk.png')
        cat_spritesheetjumpright = Spritesheet('/Users/cass/Downloads/OOP/Catgameprogress/images/catrightjump.png')
        cat_spritesheetjumpleft = Spritesheet('/Users/cass/Downloads/OOP/Catgameprogress/images/catleftjump.png')

        for animation in self.animation_steps: 
            temp_img_list = []
            stepcounter = 0
            counter = 0
            for _ in range(animation):
                #idle right
                if counter == 0:
                    temp_img_list.append(cat_spritesheetwalkright.get_sprite(stepcounter,21,17,3.5))
                #idle right
                if counter == 1:
                    temp_img_list.append(cat_spritesheetwalkleft.get_sprite(stepcounter,21,17,3.5))
                #walk right
                if counter == 2:
                    temp_img_list.append(cat_spritesheetwalkright.get_sprite(stepcounter,21,17,3.5))
                #walk left
                elif counter == 3:
                    temp_img_list.append(cat_spritesheetwalkleft.get_sprite(stepcounter,21,17,3.5))
                #jump right
                elif counter == 4:
                    temp_img_list.append(cat_spritesheetjumpright.get_sprite(stepcounter,22,18,3.5))
                #jump left
                elif counter == 5:
                    temp_img_list.append(cat_spritesheetjumpleft.get_sprite(stepcounter,22,18,3.5))
                #next step 
                stepcounter += 1
            #add list to animation list --> 0-idleright, 1-idleleft, 2-walkright, 3-walkleft, 4-jumpright, 5-jumpleft
            self.animation_list.append(temp_img_list)
            #increment
            counter += 1
    

    def jump(self):
        #jump only if standing on a surface (no flying)
        if self.jumping and self.on_ground:
            self.on_ground = False #prevents more than one jump
            self.gravity = -10 #temp change gravity to move up instead of down
            self.jump_start = pg.time.get_ticks()
            self.jumping = False


    def update(self):
        self.vx = 0
        keys = pg.key.get_pressed()
        #horizontal motion
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            if self.rect.x > 350: #left screen limit
                self.FACING_LEFT = True
                self.state = 'walkleft'
                self.vx = -5    
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            if self.rect.x < 3700: #right screen limit
                self.FACING_LEFT = False
                self.state = 'walkright'
                self.vx = 5
        #fake gravity
        if self.rect.y < 550: 
           self.vy = self.gravity
        if pg.time.get_ticks() - self.jump_start >= self.jump_duration:
            self.gravity = 5 #return gravity to normal once jump timer is over
        
        self.rect.x += self.vx
        self.rect.y += self.vy

        self.set_state()
        self.animate()
        #slow down frames for cat movement ?
        #clock = pygame.time.Clock()
        #clock.tick(50)

    def set_state(self):
        if self.vx == 0:
            if self.FACING_LEFT:
                self.state = 'idleleft'
            else:
                self.state = 'idleright'
        if self.gravity == -10:
            if self.FACING_LEFT:
                self.state = 'jumpleft'
            else:
                self.state = 'jumpright'

    def animate(self):
        #pause = pg.time.Clock
        now = pg.time.get_ticks()
        if self.state == 'walkright' or self.state == 'walkleft':
            if now - self.last_update > 200:
                self.last_updated = now
                self.frame = (self.frame + 1) % (self.animation_steps[3]-self.frame)
                if self.state == 'walkleft':
                    self.image = self.animation_list[3][self.frame]
                    #pause.tick(6)
                elif self.state == 'walkright':
                    self.image = self.animation_list[2][self.frame]
                    #pause.tick(6)
        elif self.state == 'jumpright' or self.state == 'jumpleft':
            if now - self.last_update > 200:
                self.last_updated = now
                self.frame = (self.frame + 1) % (self.animation_steps[5]-self.frame)
                if self.state == 'jumpleft':
                    self.image = self.animation_list[5][self.frame]
                elif self.state == 'jumpright':
                    self.image = self.animation_list[4][self.frame] 
        else:
            if now - self.last_update > 100:
                self.last_updated = now
                self.frame = 0 #only one frame for idle
                if self.FACING_LEFT:
                    self.image = self.animation_list[1][0]
                elif not self.FACING_LEFT:
                    self.image = self.animation_list[0][0]

     

## SPRITES ##
class Spritesheet:
    def __init__(self,filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
   
    def get_sprite (self,frame,w,h,scale):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0,0), (frame*w,0,w,h))
        sprite = pygame.transform.scale(sprite,(w*scale,h*scale))
        return sprite


## PLATFORMS ##
class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,w,h,color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        if w == 4200: #floor
            self.image.set_colorkey((0,0,0))
        else: #actual platform
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


## TREATS ##
class Treat(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('/Users/cass/Downloads/OOP/Catgameprogress/images/treat.png')
        self.image = pygame.transform.scale(self.image,(17*2.5,9*2.5))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)


## SPIKES ##
class Fire(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('/Users/cass/Downloads/OOP/Catgameprogress/images/fire.png')
        self.image = pygame.transform.scale(self.image,(13*4,15*4))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
       

