import pygame as pg
import sys
from sprites import *
from camera import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        #screen
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load('/Users/cass/Downloads/OOP/Catgameprogress/images/orangecat.png')) #icon is main character
        self.background = pygame.image.load('/Users/cass/Downloads/OOP/Catgameprogress/images/city.png')
        self.background = pygame.transform.scale(self.background, (4200,600)) #scale bg image
        
        self.clock = pygame.time.Clock()
        self.running = True
        
    
    def new(self): #start a new game
        #create groups
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.treats = pg.sprite.Group()
        self.fires = pg.sprite.Group()
        #make elements
        self.player = Kitty(self,77,63,'/Users/cass/Downloads/OOP/Catgameprogress/images/orangecat.png')
        floor = Platform (0, 570, 4200,100,(0,0,0))
        p1 = Platform(700,480,150,10,(128,128,128))
        p2 = Platform(900,350,100,10,(128,128,128))
        p3 = Platform(1100,220,250,10,(128,128,128))
        p4 = Platform(1400,480,150,10,(128,128,128))
        p5 = Platform(2100,480,300,10,(128,128,128))
        p6 = Platform(2900,480,300,10,(128,128,128))
        p7 = Platform(2750,360,100,10,(128,128,128))
        t1 = Treat(950,330)
        t2 = Treat(1250,535)
        t3 = Treat(1300,200)
        t4 = Treat(1850,470)
        t5 = Treat(2300,535)
        t6 = Treat(2785,330)
        t7 = Treat(3150,435)
        t8 = Treat(3300,535)
        t9 = Treat(3500,535)
        f1 = Fire(1200,540)
        f2 = Fire(1600,540)
        f3 = Fire(1650,540)
        f4 = Fire(1700,540)
        f5 = Fire(2100,540)
        f6 = Fire(2910,540)
        f7 = Fire(3030,450)
        
        
        #add elements to groups
        self.all_sprites.add(self.player)
        self.platforms.add(floor)
        self.platforms.add(p1)
        self.platforms.add(p2)
        self.platforms.add(p3)
        self.platforms.add(p4)
        self.platforms.add(p5)
        self.platforms.add(p6)
        self.platforms.add(p7)
        self.treats.add(t1)
        self.treats.add(t2)
        self.treats.add(t3)
        self.treats.add(t4)
        self.treats.add(t5)
        self.treats.add(t6)
        self.treats.add(t7)
        self.treats.add(t8)
        self.treats.add(t9)
        self.fires.add(f1)
        self.fires.add(f2)
        self.fires.add(f3)
        self.fires.add(f4)
        self.fires.add(f5)
        self.fires.add(f6)
        self.fires.add(f7)
        


        #camera
        self.camera = Camera(self.player)
        self.follow = Follow(self.camera, self.player)
        self.camera.setmethod(self.follow)
        #run
        self.run()
   

    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    

    def update(self): #game loop updates
        self.all_sprites.update()
        self.platforms.update()
        self.treats.update()
        self.fires.update()
        
        #check if player is colliding with a platform
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.on_ground = True
            self.player.rect.bottom = hits[0].rect.top
        
        #collecting treats
        eat = pygame.sprite.spritecollide(self.player,self.treats,True)
        if eat:
            self.player.score += len(eat)*100
        
        #die if touch fire
        f = pygame.sprite.spritecollide(self.player,self.fires,False)
        if f:
            self.player.alive = False
            self.playing = False
            self.player.kill()
            self.show_end_screen()
        

    def events(self):
        #game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jumping = True
                    self.player.jump()
        

    def draw(self):
        self.camera.scroll()
        self.screen.blit(self.background, (0 - self.camera.offset.x, 0 - self.camera.offset.y))
        #self.all_sprites.draw(self.screen)
        for pf in self.platforms:
            self.screen.blit(pf.image, (pf.rect.x - self.camera.offset.x, pf.rect.y - self.camera.offset.y))
        for t in self.treats:
            self.screen.blit(t.image, (t.rect.x - self.camera.offset.x, t.rect.y - self.camera.offset.y))
        for f in self.fires:
            self.screen.blit(f.image, (f.rect.x - self.camera.offset.x, f.rect.y - self.camera.offset.y))
        

        self.screen.blit(self.player.image, (self.player.rect.x - self.camera.offset.x , self.player.rect.y - self.camera.offset.y))
        self.draw_text(str(self.player.score),22,(0,0,0),30,20)
        pg.display.flip()
        

    def show_start_screen(self):
        if not self.running:
            return
        self.screen.fill(ORANGE)
        self.draw_text("Cat Game :)",48,(255,255,255),WIDTH/2,HEIGHT/4)
        self.draw_text("Press any key to start!",22,(255,255,255),WIDTH/2,HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()

    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
                

    def show_end_screen(self):
        #game over/continue
        if not self.player.alive:
            self.screen.fill(ORANGE)
            self.draw_text("GAME OVER",48,(255,255,255),WIDTH/2,HEIGHT/4)
            self.draw_text("Press any key to play again ...",22,(255,255,255),WIDTH/2,HEIGHT*3/4)
            pg.display.flip()
            self.wait_for_key()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    self.player.alive = True
                    self.running = True

    
    def draw_text(self,text,size,color,x,y):
        font = pg.font.SysFont("monospace",size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)



g = Game()
g.show_start_screen()
while g.running:
    g.show_start_screen()
    g.new()
    g.show_end_screen()
pg.quit()
