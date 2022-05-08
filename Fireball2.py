import pygame
import random
def collide(Sprite1, Sprite2):
    if ((Sprite1.x <  Sprite2.x  < Sprite1.x + Sprite1.width
        and   Sprite1.y < Sprite2.y < Sprite1.y + Sprite1.height)
        or   (Sprite1.x < Sprite2.x + Sprite2.width  < Sprite1.x + Sprite1.width
        and   Sprite1.y < Sprite2.y + Sprite2.height < Sprite1.y + Sprite1.height)
        or   (Sprite2.x < Sprite1.x < Sprite2.x + Sprite2.width
        and   Sprite2.y < Sprite1.y < Sprite2.y + Sprite2.height)
        or   (Sprite2.x < Sprite1.x + Sprite1.width  < Sprite2.x + Sprite2.width
        and   Sprite2.y < Sprite1.y + Sprite1.height < Sprite2.y + Sprite2.height)):
            return  True
    else:
        return False
def collideG(Sprite, Group):
    Iscollide = False
    for Spr in Group.sprites():
        if collide(Sprite.rect, Spr.rect):
            Iscollide = True
            s = Spr.rect
    return Iscollide
class Const():
    def __init__(self, value):
        self.value = value
class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(topleft = (x, y))
        #self.collider = self.rect.copy()
class Fireball(Sprite):
    def __init__(self,img,group):
        Sprite.__init__(self,random.randint(0,1100),0,'fireball.png')
        self.speedy = 1
        self.animing = img
        self.cadr = 0
        self.add(group)
    def update(self,g):
        if self.rect.y < 700:
            self.rect.y = self.rect.y + self.speedy
            self.speedy = self.speedy + g.value
        else:
            self.rect.y = 0
            self.rect.x = random.randint(0,1100)
            self.speedy = 1
        self.image = self.animing[self.cadr % 4]
        self.cadr = self.cadr + 1
class Hero(Sprite):
    def __init__(self,img,x,y,speed,GoL,GoR):
        Sprite.__init__(self,x,y,img)
        self.imgR = pygame.image.load(img)
        self.imgL = pygame.transform.flip(self.imgR, True, False)
        self.speedx = speed
        self.jumppower = -10  # cила прыжка
        self.cadr = 0
        self.animGoL = GoL
        self.animGoR = GoR
        self.dir = True
        self.game = True
    def update(self, keys, g, GroupFireBall):
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speedx
            self.image = self.animGoR[self.cadr % 5]
            self.dir = True
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speedx
            self.image = self.animGoL[self.cadr % 5]
            self.dir = False
        else:
            if self.dir:
                self.image = self.imgR
            else:
                self.image = self.imgL
        if collideG(self,GroupFireBall): # rewrite
            self.game = False
        self.cadr += 1
ImgPlayerGoR = [pygame.image.load('GoAnim/b1.png'),
               pygame.image.load('GoAnim/b2.png'),
               pygame.image.load('GoAnim/b3.png'),
               pygame.image.load('GoAnim/b4.png'),
               pygame.image.load('GoAnim/b5.png')]
ImgPlayerGoL = []
for img in ImgPlayerGoR:
    ImgPlayerGoL.append(pygame.transform.flip(img, True, False))
ImgFireBall = [pygame.image.load('fireball.png'),
                pygame.image.load('fireball1.png'),
                pygame.image.load('fireball2.png'),
                pygame.image.load('fireball3.png')]
for i in range(len(ImgFireBall)): # [0 1 2 3]
    scale = pygame.transform.scale(ImgFireBall[i],(180,65))
    ImgFireBall[i] = pygame.transform.rotate(scale,-90)
clock = pygame.time.Clock()
g = Const(1)
w = pygame.display.set_mode ((1200, 700))
GroupFireBall = pygame.sprite.Group()
Fb1 = Fireball(ImgFireBall, GroupFireBall)
player = Hero('GoAnim/b1.png',500,500,5,ImgPlayerGoL,ImgPlayerGoR)
game = True
while game:
    clock.tick(60)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            game = False
    keys = pygame.key.get_pressed()
    w.fill((0,0,0))
    GroupFireBall.update(g)
    player.update(keys,g,GroupFireBall)
    w.blit(player.image, player.rect)
    GroupFireBall.draw(w)
    pygame.display.update()
    if player.game == False:
        game = False
pygame.quit()





