import pygame
import random
pygame.init()

#global variables necessary
player = 1
steve = pygame.image.load('standing.png')
tony = pygame.image.load('tonkystanding.png')
timerCount = 0
winner = None
gameOver = False
pause = False
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,128,0)
spaceCount = 0
count = 0
guns = []
gunCount = 0
bullets = pygame.sprite.Group()
bulletCount = 0
captainWalkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), \
pygame.image.load('L3.png')]
captainWalkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), \
pygame.image.load('R3.png')]
ironWalkLeft = [pygame.image.load('TSL1.png'), pygame.image.load('TSL2.png'), \
pygame.image.load('TSL3.png')]
ironWalkRight = [pygame.image.load('TSR1.png'), pygame.image.load('TSR2.png'), \
pygame.image.load('TSR3.png')]
#image from https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-animation/
bg = None
normal = pygame.image.load('bgsmall.png')
okami = pygame.image.load('okamismall.png')
dark = pygame.image.load('darksmall.png')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((850, 480))
gameDisplay = pygame.display.set_mode((850, 480))

#Character class template from: 
#https://techwithtim.net/tutorials/game-development-with-python/
#pygame-tutorial/optimization/
#original: x, y, width, height, isJump, left, right, walkCount, jumpCount
transparent = (0, 0, 0, 0)
#bullet class template: http://programarcadegames.com/python_examples/f.php?file=bullets.py
class Bullet(pygame.sprite.Sprite): #initializes the bullets from the gun
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 4])
        self.image.fill(black)
        self.rect = self.image.get_rect()
 
    def update(self, other):
        surface = pygame.image.tostring(other.img, "RGBA")
        if surface == pygame.image.tostring(\
        pygame.image.load('capwithgun.png'), "RGBA"):
            self.rect.x += 3
        elif surface == pygame.image.tostring(\
        pygame.image.load('capwithgunL.png'), "RGBA"):
            self.rect.x -=3
        else:
            self.rect.x = -3
            
class Weapon(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
 
#images from https://marketplacecdn.yoyogames.com/images/assets/1684/icon/1427428321_large.jpg?1427428321       
class Gun(Weapon): #initializes and draws the gun cap will retrieve
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.img = pygame.image.load('gun.png')
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collided = False
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
    def collide(self, other):
        col = self.rect.colliderect(other.rect)
        if col and isinstance(other, CaptainAmerica):
            if self.collided == False:
                self.img.fill(transparent)
                self.collided = True

#images from https://s1.piq.land/2015/09/17/tDJaYsG347vi6BWpLAWHxcpN_400x400.png
class Kit(object): #health kits to gain back points
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.img = pygame.image.load('health.png')
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.collided = True
    def draw(self, screen):
        screen.blit(self.img, (self.x,self.y))
    def collide(self, other):
        col = self.rect.colliderect(other.rect)
        if self.collided == True and col == True and isinstance(other, IronMan) or \
        self.collided == True and col == True and isinstance(other, CaptainAmerica):
            self.img.fill(transparent)
            self.collided = False

class Character(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
#images from https://tinyurl.com/y4abltzk
class Sif(Character): #AI character Sif
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.img = pygame.image.load('sifwalk.png')
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lives = 3
        self.vel = 20
        self.punch = False
        self.charHealth = 100
        self.walkCount = 0
        self.isJump = False
        self.left = False
        self.right = False
        self.collideCount = 0
        self.collided = False
        self.jumpCount = 0
        self.side = None
    #draw and move template from:
    #https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-collision/
    def draw(self, screen): #walking and punching and jumping
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        elif self.punch and self.right:
            self.img = pygame.image.load('sifpunch.png')
            screen.blit(self.img, (self.x,self.y))
        elif self.right:
            self.img = pygame.image.load('sifwalk.png')
            screen.blit(self.img, (self.x,self.y))
            self.walkCount += 1
        elif self.punch and self.left:
            self.img = pygame.image.load('sifpunchL.png')
            screen.blit(self.img, (self.x,self.y))
        elif self.isJump:
            self.img = pygame.image.load('sifjump.png')
            screen.blit(self.img, (self.x,self.y))
        elif self.left:
            self.img = pygame.image.load('sifwalkL.png')
            screen.blit(self.img, (self.x,self.y))
            self.walkCount += 1
        else:
            screen.blit(self.img, (self.x,self.y))
                
    def moveLeft(self):
        self.left = True
        self.right = False
        self.punch = False
        self.x -= self.vel
        self.rect.x = self.x
        self.rect.y = self.y
    
    def moveRight(self):
        self.right = True
        self.left = False
        self.punch = False
        self.x += self.vel
        self.rect.x = self.x
        self.rect.y = self.y
    
    def punchRight(self):
        self.punch = True
        self.right = True
        self.left = False
        self.x += self.vel
        self.rect.x = self.x
    
    def punchLeft(self):
        self.punch = True
        self.right = False
        self.left = True
        self.x -= self.vel
        self.rect.x = self.x
    
    def jumpUp(self):
        self.isJump = True
        self.punch = False
        self.right = False
        self.left = False
        self.y -= self.vel
        self.rect.y = self.y
    
    def fall(self):
        self.y += self.vel
        self.rect.y = self.y
        if self.y > 300:
            self.isJump = False
     
    def collide(self, other):
        col = self.rect.colliderect(other.rect)
        if col and isinstance(other, CaptainAmerica):
            cSurface = pygame.image.tostring(other.img, "RGBA")
            tSurface = pygame.image.tostring(self.img, "RGBA")
            if tSurface == pygame.image.tostring(pygame.image.load('sifpunch.png'), "RGBA")\
            or tSurface == pygame.image.tostring(pygame.image.load('sifpunchL.png'), "RGBA"):
                self.charHealth += 0
            elif cSurface == pygame.image.tostring(\
            pygame.image.load('Lcappunch.png'), "RGBA") and other.strength != 5:
                other.strength +=1
                self.charHealth -= 5
                self.x -= 10
                self.rect.x -=10
                screen.blit(self.img, (self.x,self.y))
            elif cSurface == pygame.image.tostring(\
            pygame.image.load('cappunch.png'), "RGBA") and other.strength != 5:
                other.strength +=1
                self.charHealth -= 5
                self.x += 10
                self.rect.x +=10
                screen.blit(self.img, (self.x,self.y))
            else:
                self.charHealth -=  3
            if self.charHealth <= 1:
                self.lives -=1
                print("hello")
                self.charHealth = 100
            if self.lives == 0:
                self.charHealth = -1

#images from https://i.pinimg.com/originals/9b/8f/29/9b8f290cc38b47aefdda68504a3d5c4c.png
class CaptainAmerica(Character):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vel = 20
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.charHealth = 100
        self.img = pygame.image.load('standing.png')
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lives = 3
        self.positioned = False
        self.shield = False
        self.punch = False
        self.strength = 0
        self.gun = False
        self.collided = False
        self.defeated = False
    #draw function template from: 
    #https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/optimization/
    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.left and self.shield:
            self.img = pygame.image.load('rshield.png')
            screen.blit(self.img, (self.x,self.y))
        elif self.left and self.punch:
            self.img = pygame.image.load('Lcappunch.png')
            screen.blit(self.img, (self.x, self.y))
        elif self.positioned and self.left:
            self.img = pygame.image.load('capwithgunL.png')
            screen.blit(self.img, (self.x, self.y))
        elif self.left:
            self.img = captainWalkLeft[self.walkCount%3]
            screen.blit(self.img, (self.x,self.y))
            self.walkCount += 1
        elif self.right and self.shield:
            self.img = pygame.image.load('shield.png')
            screen.blit(self.img, (self.x,self.y))
        elif self.right and self.punch:
            self.img = pygame.image.load('cappunch.png')
            screen.blit(self.img, (self.x, self.y))
        elif self.positioned and self.right:
            self.img = pygame.image.load('capwithgun.png')
            screen.blit(self.img, (self.x, self.y))
        elif self.right:
            self.img = captainWalkRight[self.walkCount%3]
            screen.blit(self.img, (self.x,self.y))
            self.walkCount +=1
        elif self.isJump:
            self.img = pygame.image.load('capjump.png')
            screen.blit(self.img, (self.x, self.y))
        else:
            screen.blit(self.img, (self.x,self.y))
    def push(self, other):
        if other.left:
            self.x -= 100
            self.rect.x = self.x
            self.img = pygame.image.load('stevefalling.png')
            screen.blit(self.img, (self.x,self.y))
        elif other.right:
            self.x += 100
            self.rect.x = self.x
            self.img = pygame.image.load('stevefalling.png')
            screen.blit(self.img, (self.x,self.y))
    def collide(self, other): #this is 100% my own code
        col = self.rect.colliderect(other.rect)
        if col == True and isinstance(other, IronMan): #reacts based on 
        #collision with iron man
            self.collided = True
            surface = pygame.image.tostring(self.img, "RGBA")
            tSurface = pygame.image.tostring(other.img, "RGBA")
            if surface == pygame.image.tostring(pygame.image.load('rshield.png'), "RGBA")\
            or surface == pygame.image.tostring(pygame.image.load('shield.png'), "RGBA")\
            or surface == pygame.image.tostring(pygame.image.load('cappunch.png'), "RGBA"):
                    self.charHealth -= 0
            elif tSurface == pygame.image.tostring(pygame.image.load('tonypunch.png'), "RGBA") or \
            tSurface == pygame.image.tostring(pygame.image.load('tonypunchL.png'), "RGBA"):
                self.charHealth -= 5
            elif tSurface == pygame.image.tostring(pygame.image.load('lasers.png'), "RGBA")\
            or tSurface == pygame.image.tostring(pygame.image.load('lasersL.png'), "RGBA")\
            and other.strength != 5:
                other.strength +=1
                self.charHealth -= 7
                self.x += 10
                self.rect.x +=10
                screen.blit(self.img, (self.x,self.y))
            else:
                self.charHealth -=1 
        if col == True and isinstance(other, Sif):
                surface = pygame.image.tostring(self.img, "RGBA")
                tSurface = pygame.image.tostring(other.img, "RGBA")
                if surface == pygame.image.tostring(pygame.image.load('rshield.png'), "RGBA")\
                or surface == pygame.image.tostring(pygame.image.load('shield.png'), "RGBA")\
                or surface == pygame.image.tostring(pygame.image.load('cappunch.png'), "RGBA"):
                        self.charHealth -= 0
                elif tSurface == pygame.image.tostring(pygame.image.load('sifpunch.png'), "RGBA") or \
                tSurface == pygame.image.tostring(pygame.image.load('sifpunchL.png'), "RGBA"):
                    self.charHealth -= 10
                else:
                        self.charHealth -=1 
        elif col == True and isinstance(other, Kit) and other.collided == True and self.charHealth < 100:
            self.charHealth += 10
        elif col == True and isinstance(other, Gun):
            self.gun = True
        if self.charHealth <= 0:
            self.lives -=1
            self.charHealth = 100
        if self.lives == 0:
            self.charHealth = -1
    def fall(self):
        self.y += self.vel
        self.rect.y = self.y
        screen.blit(self.img, (self.x,self.y))
        if self.y > 300:
            self.isJump = False
            self.img = pygame.image.load('standing.png')
    def update(self): #when he's knocked off screen, he comes back to life
        self.img = pygame.image.load('standing.png')
        self.y += self.vel
        self.rect.y = self.y
        self.rect.x = self.x
        screen.blit(self.img, (self.x,self.y))
        if self.y > 300:
            self.defeated = False
            self.colllided = False

#template code for iron man from same place as captain america class
#images from https://i.pinimg.com/originals/22/90/83/229083d9549d05c7d8821732dcca5606.gif
class IronMan(Character):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vel = 20
        self.left = False
        self.right = False
        self.walkCount = 0
        self.charHealth = 100
        self.img = pygame.image.load('tonkystanding.png')
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lives = 3
        self.blast = False
        self.fly = False
        self.jumpCount = 10
        self.punch = False
        self.defeated = False
        self.collided = False
        self.strength = 0
    def draw(self, screen): #walking, punching, blasting, flying
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        elif self.punch and self.left:
            self.img = pygame.image.load('tonypunchL.png')
            screen.blit(self.img, (self.x, self.y))
        elif self.blast and self.left:
            self.img = pygame.image.load('lasersL.png')
            screen.blit(self.img, (self.x, self.y))
        elif self.left:
            self.img = ironWalkLeft[self.walkCount%3]
            screen.blit(self.img, (self.x,self.y))
            self.walkCount += 1
        elif self.blast and self.right:
            self.img = pygame.image.load('lasers.png')
            screen.blit(self.img, (self.x, self.y))
        elif self.punch and self.right:
            self.img = pygame.image.load('tonypunch.png')
            screen.blit(self.img, (self.x, self.y))
        elif self.right:
            self.img = ironWalkRight[self.walkCount%3]
            screen.blit(self.img, (self.x,self.y))
            self.walkCount +=1
        elif self.fly:
            self.img = pygame.image.load('imjump.png')
            screen.blit(self.img, (self.x, self.y))
        else:
            screen.blit(self.img, (self.x,self.y))
            
    def update(self):
        self.img = pygame.image.load('tonkystanding.png')
        self.y += self.vel
        self.rect.y = self.y
        self.rect.x = self.x
        screen.blit(self.img, (self.x,self.y))
        if self.y > 300:
            self.defeated = False
            self.colllided = False
    def push(self, other):
        if other.left:
            self.x -= 100
            self.rect.x = self.x
            self.img = pygame.image.load('tonkyfalling.png')
            screen.blit(self.img, (self.x,self.y))
        elif other.right:
            self.x += 100
            self.rect.x = self.x
            self.img = pygame.image.load('tonkyfalling.png')
            screen.blit(self.img, (self.x,self.y))
    def flying(self):
        self.y -= self.vel
        self.rect.y -= self.y
        self.rect.x = self.x
        screen.blit(self.img, (self.x,self.y))
    def fall(self):
        self.img = pygame.image.load('tonkystanding.png')
        self.y += self.vel
        self.rect.y = self.y
        self.rect.x = self.x
        screen.blit(self.img, (self.x,self.y))
        if self.y > 300:
            self.fly = False
            screen.blit(self.img, (self.x,self.y))
    def collide(self, other):
        col = self.rect.colliderect(other.rect)
        if col == True and isinstance(other, CaptainAmerica): #reaction based 
        #on collision with captain america
            self.collided = True
            cSurface = pygame.image.tostring(other.img, "RGBA")
            tSurface = pygame.image.tostring(self.img, "RGBA")
            if cSurface == pygame.image.tostring(pygame.image.load('Lcappunch.png'), "RGBA"):
                other.strength +=1
                self.charHealth -= 5
                self.x -= 10
                self.rect.x -=10
                screen.blit(self.img, (self.x,self.y))
            elif cSurface == pygame.image.tostring(pygame.image.load('cappunch.png'), "RGBA"):
                other.strength +=1
                self.charHealth -= 5
                self.x += 10
                self.rect.x +=10
                screen.blit(self.img, (self.x,self.y))
                screen.blit(pygame.image.load('questions.png'), (self.x, self.y +5))
            elif tSurface == pygame.image.tostring(pygame.image.load('lasers.png'), "RGBA")\
            or tSurface == pygame.image.tostring(pygame.image.load('lasersL.png'), "RGBA"):
                self.charHealth -= 0
            else:
                self.charHealth -=  3
        elif col == True and isinstance(other, Kit) and \
        other.collided == True and self.charHealth < 100:
            self.charHealth += 10
        elif col and isinstance(other, Bullet):
            self.charHealth -= 10
        if self.charHealth <= 0:
                self.lives -=1
                self.charHealth = 100
        if self.lives == 0:
                self.charHealth = -1
            
font = pygame.font.Font('freesansbold.ttf', 20)
cap = CaptainAmerica(200, 300, 10, 10)
tonky = IronMan(100, 300, 10, 10)
newKit = Kit(random.randint(1, 300), random.randint(1, 300), 5, 5)
newKit2 = Kit(random.randint(1, 300), random.randint(1, 300), 10, 10)
newKit3 = Kit(random.randint(1, 300), random.randint(1, 300), 10, 10)
newKit4 = Kit(random.randint(1, 300), random.randint(1, 300), 10, 10)
sif = Sif(100, 300, 10, 10)

def redrawGameWindowAI():
    screen.blit(bg, (0,0))
    text1 = font.render('Cap score: ' + str(cap.charHealth), 1, (0,0,0))
    text = font.render('Sif score: ' + str(sif.charHealth), 1, (0,0,0))
    screen.blit(text, (50, 10))
    screen.blit(text1, (300, 10))
    sif.draw(screen)
    cap.draw(screen)
    pygame.display.update()
    
def redrawGameWindow():
    screen.blit(bg, (0,0))
    text = font.render('Cap score: ' + str(cap.charHealth), 1, (0,0,0))
    text1 = font.render('Ironman score: ' + str(tonky.charHealth), 1, (0,0,0))
    screen.blit(text, (50, 10))
    screen.blit(text1, (300, 10))
    cap.draw(screen)
    tonky.draw(screen)
    newKit.draw(screen)
    newKit2.draw(screen)
    newKit3.draw(screen)
    newKit4.draw(screen)
    for gun in guns:
        gun.draw(screen)
    bullets.draw(screen)
    pygame.display.update()

#button code from:
#https://pythonprogramming.net/pygame-button-function-events/?completed=/pygame-button-function/

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def charactersIntro(): #description of powersets for each char.
    global font
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        gameDisplay.blit(pygame.image.load('standing.png'), (100, 200))
        gameDisplay.blit(pygame.image.load('tonkystanding.png'), (450, 200))
        text1 = font.render('Captain America', 1, (0,0,0))
        text2 = font.render('Powers:', 1, (0, 0, 0))
        text3 = font.render('-Punch', 1, (0, 0, 0))
        text4 = font.render('-Shield', 1, (0, 0, 0))
        gameDisplay.blit(text1, (50, 10))
        gameDisplay.blit(text2, (100, 40))
        gameDisplay.blit(text3, (100, 70))
        gameDisplay.blit(text4, (100, 100))
        text5 = font.render('Iron Man', 1, (0,0,0))
        text6 = font.render('Powers:', 1, (0, 0, 0))
        text7 = font.render('-Punch', 1, (0, 0, 0))
        text8 = font.render('-Lasers', 1, (0, 0, 0))
        gameDisplay.blit(text5, (400, 10))
        gameDisplay.blit(text6, (400, 40))
        gameDisplay.blit(text7, (400, 70))
        gameDisplay.blit(text8, (400, 100))
        button("choose player mode",100,400,250,50,green,choosePlayerMode)
        pygame.display.update()
        

def choosePlayerMode():
    choose = True
    global bg
    global okami
    global dark
    global normal
    while choose:
        gameDisplay.fill(white)
        gameDisplay.blit(normal, (0, 50))
        gameDisplay.blit(okami, (180, 50))
        gameDisplay.blit(dark, (450, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if normal.get_rect(topleft=(0, 50)).collidepoint(pygame.mouse.get_pos()):
                    bg = pygame.image.load('bg.jpg')
                elif okami.get_rect(topleft=(180, 50)).collidepoint(pygame.mouse.get_pos()):
                    bg = pygame.image.load('okami.png')
                elif dark.get_rect(topleft=(450, 50)).collidepoint(pygame.mouse.get_pos()):
                    bg = pygame.image.load('dark.png')
        smallText = pygame.font.Font("freesansbold.ttf",20)
        button("Single player",50,300,250,50,green,howToPlay)
        button("Multiplayer",450,300,100,50,red,multiPlayer)
        pygame.display.update()
        clock.tick(15)

def multiPlayer(): #lets people choose their characters and start game
    global steve
    global tony
    global player
    playing = True
    while playing:
        gameDisplay.fill(white)
        gameDisplay.blit(steve, (100, 200))
        gameDisplay.blit(tony, (450, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if steve.get_rect(\
                topleft=(100, 200)).collidepoint(pygame.mouse.get_pos()) \
                and player == 1:
                    text1 = font.render('Player 1', 1, (0,0,0))
                    gameDisplay.blit(text1, (100, 300))
                    player +=1
                elif tony.get_rect(\
                topleft=(450, 200)).collidepoint(pygame.mouse.get_pos()) \
                and player == 1:
                    text1 = font.render('Player 1', 1, (0,0,0))
                    gameDisplay.blit(text1, (450, 300))
                    player +=1
                elif steve.get_rect(\
                topleft=(100, 200)).collidepoint(pygame.mouse.get_pos()) and \
                player == 2:
                    text2 = font.render('Player 2', 1, (0,0,0))
                    gameDisplay.blit(text2, (100, 300))
                elif tony.get_rect(\
                topleft=(450, 200)).collidepoint(pygame.mouse.get_pos()) and \
                player == 2:
                    text2 = font.render('Player 2', 1, (0,0,0))
                    gameDisplay.blit(text2, (450, 300))
        smallText = pygame.font.Font("freesansbold.ttf",20)
        button("directions",50,400,250,50,green,howToPlay)
        button("start!",450,400,100,50,red,gamePlay)
        pygame.display.update()
        clock.tick(15)

def howToPlay(): #instructions on how to play
    global font
    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        gameDisplay.blit(pygame.image.load('standing.png'), (100, 300))
        gameDisplay.blit(pygame.image.load('tonkystanding.png'), (450, 300))
        text1 = font.render('Captain America', 1, (0,0,0))
        text2 = font.render('Directions:', 1, (0, 0, 0))
        text3 = font.render('Up and left/right: shield defense', 1, (0, 0, 0))
        text4 = font.render('left/right: walking', 1, (0, 0, 0))
        text5 = font.render('Down and left/right: punch', 1, (0, 0, 0))
        text6 = font.render('return and left/right: shoot bullets', 1, (0, 0, 0))
        text7 = font.render('space bar: jump', 1, (0, 0, 0))
        gameDisplay.blit(text1, (0, 70))
        gameDisplay.blit(text2, (50, 100))
        gameDisplay.blit(text3, (50, 130))
        gameDisplay.blit(text4, (50, 160))
        gameDisplay.blit(text5, (50, 190))
        gameDisplay.blit(text6, (50, 220))
        gameDisplay.blit(text7, (50, 250))
        text8 = font.render('Iron Man', 1, (0,0,0))
        text9 = font.render('Directions:', 1, (0, 0, 0))
        text10 = font.render('a and d: left and right walking', 1, (0, 0, 0))
        text11 = font.render('s: flying', 1, (0, 0, 0))
        text12 = font.render('w and a/d: punch', 1, (0, 0, 0))
        gameDisplay.blit(text8, (400, 70))
        gameDisplay.blit(text9, (400, 100))
        gameDisplay.blit(text10, (400, 130))
        gameDisplay.blit(text11, (400, 150))
        gameDisplay.blit(text12, (400, 190))
        text13 = font.render('P: pause', 1, (0, 0, 0))
        gameDisplay.blit(text13, (400, 400))
        button("start single!",100,0,250,50,green,gameAI)
        button("start multiplayer!",500,0,250,50,red,gamePlay)
        pygame.display.update()

#template code: 
#https://pythonprogramming.net/pygame-button-function-events/?completed=/pygame-button-function/
def game_intro(): #intro page
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        text1 = font.render('Marvel Battle', 1, (0, 0, 0))
        text2 = font.render('Let your favorite Marvel characters fight!', 1, (0, 0, 0))
        gameDisplay.blit(text1, (300, 100))
        gameDisplay.blit(text2, (300, 150))
        smallText = pygame.font.Font("freesansbold.ttf",20)
        button("Character descriptions",50,200,250,50,green,charactersIntro)
        button("Player mode",450,200,100,50,red,choosePlayerMode)
        pygame.display.update()
        clock.tick(15)
        
#code for pause/unpause:
#https://pythonprogramming.net/pause-game-pygame/
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def paused(): #pause function
    pygame.mixer.music.pause()
    largeText = pygame.font.SysFont("freesansbold.ttf",115)
    gameDisplay.fill(white)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((250),(250))
    gameDisplay.blit(TextSurf, TextRect)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Continue",150,350,100,50,green,unpause)
        button("Quit",550,350,100,50,red,quit)
        pygame.display.update()
        clock.tick(15)   
        
#run template from: https://techwithtim.net/tutorials/
#game-development-with-python/pygame-tutorial/optimization/
def gamePlay():
    global count
    global gunCount
    global guns
    global bulletCount
    global bullets
    global spaceCount
    global pause
    global winner
    global gameOver
    run = True
    #pygame.mixer.music.load('fighting.wav')
    #pygame.mixer.music.play(-1)
    while run and not pause:
        count+=1
        if count % 100 == 0 and gunCount < 4:
            guns.append(Gun(random.randint(1, 300), random.randint(1, 300), 10, 10))
            gunCount +=1
        clock.tick(27)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            pause = True
            paused()
    
        if keys[pygame.K_LEFT] and cap.x > cap.vel:
            if keys[pygame.K_UP]:
                cap.x -= cap.vel
                cap.rect.x -= cap.vel
                cap.left = True
                cap.right = False
                cap.shield = True
                cap.punch = False
                cap.positioned = False
            elif keys[pygame.K_DOWN]:
                cap.punch = True
                cap.x -= cap.vel
                cap.rect.x -= cap.vel
                cap.left = True
                cap.right = False
                cap.shield = False
                cap.positioned = False
            else:
                cap.x -= cap.vel
                cap.rect.x -= cap.vel
                cap.left = True
                cap.right = False
                cap.shield = False
                cap.punch = False
                cap.positioned = False
        elif keys[pygame.K_RIGHT] and cap.x < 850 - cap.width - cap.vel:
            if keys[pygame.K_UP]:
                cap.x += cap.vel
                cap.rect.x += cap.vel
                cap.left = False
                cap.right = True
                cap.shield = True
                cap.punch = False
                cap.positioned = False
            elif keys[pygame.K_DOWN]:
                cap.punch = True
                cap.x += cap.vel
                cap.rect.x += cap.vel
                cap.left = False
                cap.right = True
                cap.shield = False
                cap.positioned = False
            else: 
                cap.x += cap.vel
                cap.rect.x += cap.vel
                cap.right = True
                cap.left = False
                cap.shield = False
                cap.punch = False
                cap.positioned = False
        else:
            cap.right = False
            cap.left = False
            cap.walkCount = 0
        if cap.strength == 5 and tonky.collided:
            tonky.push(cap)
            if tonky.x < 0 or tonky. x > 850:
                tonky.y = 0
                tonky.rect.y = 0
                tonky.charHealth = 0
                tonky.defeated = True
                tonky.collided = False
                cap.strength = 0
        if tonky.strength == 5 and cap.collided:
            cap.push(tonky)
            if cap.x < 0 or cap. x > 850:
                cap.y = 0
                cap.rect.y = 0
                cap.charHealth = 0
                cap.defeated = True
                cap.collided = False
                tonky.strength = 0
        if keys[pygame.K_SPACE] and spaceCount < 1 and cap.rect.y > 100:
            cap.isJump = True
            spaceCount = 1
            cap.right = False
            cap.left = False
            cap.walkCount = 0
            cap.rect.y -= 200
            cap.y = cap.rect.y
            cap.positioned = False
        if cap.isJump and not keys[pygame.K_SPACE]:
            cap.fall()
            spaceCount -=1
            cap.positioned = False
        if keys[pygame.K_a] and tonky.x > tonky.vel:
            if keys[pygame.K_w]:
                tonky.x -= tonky.vel
                tonky.rect.x -= cap.vel
                tonky.left = True
                tonky.right = False
                tonky.punch = True
                tonky.blast = False
            elif keys[pygame.K_q]:
                tonky.x -= tonky.vel
                tonky.rect.x -= cap.vel
                tonky.left = True
                tonky.right = False
                tonky.punch = False
                tonky.blast = True
            else:
                tonky.x -= tonky.vel
                tonky.rect.x -= tonky.vel
                tonky.left = True
                tonky.right = False
                tonky.punch = False
                tonky.blast = False
        elif keys[pygame.K_d] and tonky.x < 850 - tonky.width - tonky.vel:
            if keys[pygame.K_w]:
                tonky.x += tonky.vel
                tonky.rect.x += tonky.vel
                tonky.right = True
                tonky.punch = True
                tonky.left = False
                tonky.blast = False
            elif keys[pygame.K_e]:
                tonky.x += tonky.vel
                tonky.rect.x += cap.vel
                tonky.left = False
                tonky.right = True
                tonky.punch = False
                tonky.blast = True
            else:
                tonky.x += tonky.vel
                tonky.rect.x += tonky.vel
                tonky.right = True
                tonky.punch = False
                tonky.left = False
                tonky.blast = False
        else:
            tonky.right = False
            tonky.left = False
            tonky.walkCount = 0
    # below is 100% my own code
        if keys[pygame.K_s]:
            tonky.right = False
            tonky.left = False
            tonky.walkCount = 0
            tonky.fly = True
            tonky.flying()
            if tonky.y < 0:
                tonky.fall()
        if tonky.fly and not keys[pygame.K_s]:
            tonky.fall()
        cap.collide(tonky)
        if cap.strength < 5:
            tonky.collide(cap)
        tonky.collide(newKit)
        tonky.collide(newKit2)
        tonky.collide(newKit3)
        tonky.collide(newKit4)
        cap.collide(newKit)
        cap.collide(newKit2)
        cap.collide(newKit3)
        cap.collide(newKit4)
        if newKit.collided == True:
            newKit.collide(cap)
            newKit.collide(tonky)
        if newKit2.collided == True:
            newKit2.collide(cap)
            newKit2.collide(tonky)
        if newKit3.collided == True:
            newKit3.collide(cap)
            newKit3.collide(tonky)
        if newKit4.collided == True:
            newKit4.collide(cap)
            newKit4.collide(tonky)
        for gun in guns:
            gun.collide(cap)
            cap.collide(gun)
        if tonky.defeated:
            tonky.update()
            tonky.x = 100
        if cap.defeated:
            cap.update()
            cap.x = 300
        if keys[pygame.K_RETURN] and cap.gun == True and cap.positioned == False:
            cap.positioned = True
            if keys[pygame.K_LEFT]:
                cap.left = True
            elif keys[pygame.K_RIGHT]:
                cap.right = True
        if keys[pygame.K_RETURN] and cap.gun and cap.positioned:
            newBullet = Bullet()
            # Set the bullet so it is where the player is
            newBullet.rect.x = cap.rect.x
            newBullet.rect.y = cap.rect.y
            # Add the bullet to the lists
            if bulletCount < 10:
                bullets.add(newBullet)
                bulletCount +=1
            else:
                cap.gun = False
        bullets.update(cap)
        for bullet in bullets:
            tonky.collide(bullet)
            if bullet.rect.x < 0 or bullet.rect.x > 850:
                bullets.remove(bullet)
        if cap.lives <= 0 or tonky.lives <= 0:
            pygame.mixer.music.stop()
            if tonky.lives <= 0:
                winner = "Captain America"
            elif cap.lives <= 0:
                winner = "Iron Man"
            gameOver = True
            gameOvers()
        redrawGameWindow()

def gameOvers(): #gameover page
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        text1 = font.render('Game over! Winner:' + str(winner), 1, (0,0,0))
        screen.blit(text1, (50, 10))
        button("Play again?",50,200,100,50,green,game_intro)
        button("Quit",200,200,100,50,red,quit)
        pygame.display.update()
        clock.tick(15)

def gameAI():
    global spaceCount
    global timerCount
    global winner
    global pause
    #pygame.mixer.music.load('fighting.wav')
    #pygame.mixer.music.play(-1)
    run = True
    while run and not pause:
        timerCount +=1
        clock.tick(27)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if sif.x - cap.x > 200 and sif.collideCount == 0:
            sif.moveLeft()
        elif cap.x - sif.x > 200 and sif.collideCount == 0:
            sif.moveRight()
        elif cap.x - sif.x <= 200 and cap.x - sif.x >= 0 and sif.collideCount == 0 \
        and 100 < timerCount < 200:
            sif.moveRight()
            if sif.rect.colliderect(cap.rect):
                sif.collide(cap)
                sif.collideCount = 1
                sif.collided = True
                sif.side = "right"
        elif cap.x - sif.x <= 200 and cap.x - sif.x >= 0 and sif.collideCount == 0 \
        and 300 < timerCount < 350 and sif.jumpCount == 0:
            sif.jumpUp()
            if sif.y < 20:
                while sif.y < 400 and sif.isJump:
                    sif.fall()
                    sif.jumpCount = 1
        elif cap.x - sif.x <= 200 and cap.x - sif.x >= 0 and sif.collideCount == 0:
            sif.punchRight()
            if sif.rect.colliderect(cap.rect):
                sif.collide(cap)
                sif.collideCount = 1
                sif.collided = True
                sif.side = "right"
        cap.collide(sif)
        if not sif.isJump:
            sif.y = 300
            sif.rect.y = sif.y
        if cap.x - sif.x > 200 and sif.collideCount == 0:
            sif.moveRight()
        elif sif.x - cap.x > 200 and sif.collideCount == 0:
            sif.moveLeft()
        elif sif.x - cap.x <= 200 and sif.x - cap.x >= 0 and sif.collideCount == 0 \
        and 100 < timerCount < 200:
            sif.moveLeft()
            if sif.rect.colliderect(cap.rect):
                sif.collide(cap)
                sif.collideCount = 1
                sif.collided = True
                sif.side = "left"
        elif sif.x - cap.x <= 200 and sif.x - cap.x >= 0 and sif.collideCount == 0:
            sif.punchLeft()
            if sif.rect.colliderect(cap.rect):
                sif.collide(cap)
                sif.collideCount = 1
                sif.collided = True
                sif.side = "left"
        if sif.collided:
            if sif.side == "right":
                sif.moveLeft()
                if sif.x < 50:
                    sif.moveRight()
                    sif.collideCount = 0
                    sif.collided = False
            elif sif.side == "left":
                sif.moveRight()
                if sif.x > 350:
                    sif.moveLeft()
                    sif.collideCount = 0
                    sif.collided = False
        if sif.charHealth <= -1 or cap.charHealth <= -1:
            run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            pause = True
            paused()
        if keys[pygame.K_LEFT] and cap.x > cap.vel:
            if keys[pygame.K_UP]:
                    cap.x -= cap.vel
                    cap.rect.x -= cap.vel
                    cap.left = True
                    cap.right = False
                    cap.shield = True
                    cap.punch = False
                    cap.positioned = False
            elif keys[pygame.K_DOWN]:
                    cap.punch = True
                    cap.x -= cap.vel
                    cap.rect.x -= cap.vel
                    cap.left = True
                    cap.right = False
                    cap.shield = False
                    cap.positioned = False
            else:
                    cap.x -= cap.vel
                    cap.rect.x -= cap.vel
                    cap.left = True
                    cap.right = False
                    cap.shield = False
                    cap.punch = False
                    cap.positioned = False
        elif keys[pygame.K_RIGHT] and cap.x < 850 - cap.width - cap.vel:
            if keys[pygame.K_UP]:
                    cap.x += cap.vel
                    cap.rect.x += cap.vel
                    cap.left = False
                    cap.right = True
                    cap.shield = True
                    cap.punch = False
                    cap.positioned = False
            elif keys[pygame.K_DOWN]:
                    cap.punch = True
                    cap.x += cap.vel
                    cap.rect.x += cap.vel
                    cap.left = False
                    cap.right = True
                    cap.shield = False
                    cap.positioned = False
            else: 
                    cap.x += cap.vel
                    cap.rect.x += cap.vel
                    cap.right = True
                    cap.left = False
                    cap.shield = False
                    cap.punch = False
                    cap.positioned = False
        else:
            cap.right = False
            cap.left = False
            cap.walkCount = 0
        if keys[pygame.K_SPACE] and spaceCount < 1 and cap.rect.y > 100:
            cap.isJump = True
            spaceCount = 1
            cap.right = False
            cap.left = False
            cap.walkCount = 0
            cap.rect.y -= 200
            cap.y = cap.rect.y
            cap.positioned = False
        if cap.isJump and not keys[pygame.K_SPACE]:
            cap.fall()
            spaceCount -=1
            cap.positioned = False
        if cap.lives <= 0 or sif.lives <= 0:
            pygame.mixer.music.stop()
            if sif.lives <= 0:
                winner = "Captain America"
            elif cap.lives <= 0:
                winner = "Sif"
            gameOver = True
            gameOvers()
        redrawGameWindowAI()

game_intro()
pygame.quit()
quit()