# as example about Python programming skills for V****t by Tuomas Liikala 31.01.2013
# date of this code version 03.02.2013

import pygame, sys
from pygame.locals import *
from copy import copy, deepcopy

pygame.init()

SCREENWIDTH = 640
SCREENHEIGHT = 480
BITS = 8

# player get these points when hit a block
POINTSPERBRAKE = 100
LEVELCOUNT = 4 # level0, level1, level2, and level3

FPS = 20 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, BITS)
pygame.display.set_caption('Animation')
font = pygame.font.SysFont("calibri",40)

# colors and images
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
txtImg = pygame.image.load('teksti.png')
txtImgW = pygame.image.load('teksti.png')
txtImgW.fill(WHITE)

class Ball:
    def __init__(self, diameter, planeHeight):
        self.x = SCREENWIDTH/2-diameter/2
        self.y = SCREENHEIGHT-planeHeight*2-diameter
    diameter = 8
    radius = diameter/2
    x = 0
    y = 0
    prevx = x
    prevy = y
    speedx = 1
    speedy = 6
    directionx = 'right'    # direction x: 'left' or 'right'
    directiony = 'up'       #           y: 'up' or 'down'
    image = pygame.image.load('kuula.png')
    imageWhite = pygame.image.load('kuula.png')
    imageWhite.fill(WHITE)
    diff = 0                  # difference with plane or block and ball. useful for collisions
    diffx = 0
    diffy = 0

    # movement of ball
    def moveObject(self, status):

        self.prevx = self.x
        self.prevy = self.y
            
        # left or right
        if self.directionx == 'right':
            self.x += self.speedx
            if self.x >= SCREENWIDTH-self.diameter: # ball is out of play area at right
                self.directionx = 'left'
        elif self.directionx == 'left':
            self.x -= self.speedx
            if self.x <= 0: # ball is out of play area at right
                self.directionx = 'right'

        # up or down
        if self.directiony == 'up':
            self.y -= self.speedy
            if self.y <= 0: # ball is out of play area at up
                self.directiony = 'down'
        elif self.directiony == 'down':
            self.y += self.speedy
            if self.y >= SCREENHEIGHT-self.diameter: # ball is out of play area at down
                status.lifes -= 1
                if status.lifes == 0: # death
                    pygame.quit()
                    sys.exit()
                self.directiony = 'up'
                self.y = SCREENHEIGHT-plane.height*2-self.diameter
                status.pause = 'true'
                self.x = plane.x+plane.width/2-ball.radius
                    
        return
    

class Plane():
    width = 64
    height = 16
    x=SCREENWIDTH/2-width/2
    y=SCREENHEIGHT-height*2
    prevx = x
    speed = 7
    move = 'none'      # 'none', 'left' or 'right'
    image = pygame.image.load('laatta.png')
    imageWhite = pygame.image.load('laatta.png')
    imageWhite.fill(WHITE)

    # movement of plane
    def moveObject(self, status):
        self.prevx = self.x
        if self.move == 'left':
            self.x -= self.speed
            if self.x < 0: # plane at left side
                self.x = 0
        elif self.move == 'right':
            self.x += self.speed
            if self.x > SCREENWIDTH-self.width: # plane at right side
                self.x = SCREENWIDTH-self.width
        elif self.move == 'none':
            self.x += 0
                
        return

# player brakes these block
class Block:
    width = 32
    height = 16
    countx = 20     # amount of blocks is maybe 10*10 or 20*20
    county = 20
    blc1Img = pygame.image.load('laattaVihree.png')
    blc2Img = pygame.image.load('laattaKeltanen.png')
    blc3Img = pygame.image.load('laattaPunanen.png')
    blc0ImgW = pygame.image.load('laattaVihree.png')
    blc0ImgW.fill(WHITE)

class Status:
    points = 0
    lifes = 3
    curlevel = 0            # current level
    pause = 'true'
    bonuslifes = 'true' # true or false
    # speed optimization
    fullprint='true'        # prints all first time

def loadLevel(curlevel):  
    level = []
    for row in open("level" + str(curlevel) + ".txt", "r"):
        level.append(map(int, row.rstrip("\n")))
    return matrixTranspose(level)

# I like to use first index as x and second index as y. I hope you aren't mathematician
def matrixTranspose(anArray):
    
  transposed = [None]*len(anArray[0])

  for i in range(len(transposed)):
    transposed[i] = [None]*len(transposed)

  for t in range(len(anArray)):
    for tt in range(len(anArray[t])):            
        transposed[t][tt] = anArray[tt][t]
        
  return transposed

# player can control only the plane
def controls(plane):

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN: # start moving
            if (event.key == K_LEFT):
                plane.move = 'left'
            elif (event.key == K_RIGHT):
                plane.move = 'right'
            elif (event.key == K_p):
                status.pause = 'true'

        elif event.type == KEYUP: # stop moving
            if event.key == K_LEFT and plane.move == 'left':
                plane.move = 'none'
            elif event.key == K_RIGHT and plane.move == 'right':
                plane.move = 'none'

    return (plane)

# movement of ball and plane
def moveObjects(ball, plane, status):

    ball.moveObject(status)
    plane.moveObject(status)
            
    return (ball, plane)

def checkForNewLevel(ball, plane, block, status, level):

    # check out all blocks in two for
    blocks = 0
    for x in range(0,block.countx):
        for y in range(0,block.county):
            if level[x][y] > 0:
                blocks += 1
                
    if blocks == 0: # all blocks broken
        status.curlevel += 1
        if status.bonuslifes == 'true':
            status.lifes += 1
        if status.curlevel == LEVELCOUNT: # if you complited the last level then you g-et first one
            status.curlevel = 0
        level = loadLevel(status.curlevel)

        # prepare variables for new level        
        status.pause = 'true'
        ball.x = plane.x-ball.radius+plane.width/2
        ball.y = SCREENHEIGHT-plane.height*2-ball.radius
        plane.x = SCREENWIDTH/2-plane.width/2
        ball.directiony = 'up'
        status.fullprint = 'true'

    return (ball, plane, status, level)

def ball2blockCollision(ball, plane, block, status, level):

    # speed opimization
    x1 = (block.countx*block.width+(ball.x-block.countx*block.width))/block.width
    y1 = (block.county*block.height+(ball.y-block.county*block.height))/block.height
    if x1 < 2:
        x1 = 2
    elif x1 > block.countx-2:
            x1 = block.countx-2
    if y1 < 2:
        y1 = 2
    elif y1 > block.county-2:
            y1 = block.county-2

    # check out all blocks in two for
    for x in range(x1-2,x1+2):
        for y in range(y1-2,y1+2):
            if level[x][y] >0 and (ball.x >= block.width*x-ball.diameter and ball.x <= block.width*x+block.width) and (ball.y >= block.height*y-ball.diameter and ball.y <= block.height*y+block.height):

                # my special: www.netikka.net/tuppul/boSpecial.png
                ball.diffx = (ball.x+ball.radius-(x*block.width+block.width/2))
                ball.diffy = (ball.y+ball.radius-(y*block.height+block.height/2))*block.width/block.height

                # ball hit the block
                if ball.diffy > 0 or ball.diffy < 0:
                    ball.diff = ball.diffx/ball.diffy
                    level[x][y] -= 1
                    status.points += POINTSPERBRAKE
                    if level[x][y] == 0:
                        DISPLAYSURF.blit(block.blc0ImgW, (block.width*x, block.height*y))
                    elif level[x][y] == 1:
                        DISPLAYSURF.blit(block.blc1Img, (block.width*x, block.height*y))
                    elif level[x][y] == 2:
                        DISPLAYSURF.blit(block.blc2Img, (block.width*x, block.height*y))
                    elif level[x][y] > 2:
                        DISPLAYSURF.blit(block.blc3Img, (block.width*x, block.height*y))
                    
                    if ball.diff > 0.0 or ball.diff < -1.0:
                        if ball.diffx <= 0:
                            ball.directionx = 'left'
                        elif ball.diffx > 0:
                            ball.directionx = 'right'
                    elif ball.diff <= 0 or ball.diff >= -1:
                        if ball.diffy <= 0:
                            ball.directiony = 'up'
                        elif ball.diffy > 0:
                            ball.directiony = 'down'

                    # check for new level
                    (ball, plane, status, level) = checkForNewLevel(ball, plane, block, status,level)

    return (ball, plane, block, status, level)

def ball2planeCollision(ball, plane):

    # my special: www.netikka.net/tuppul/boSpecial.png
    
    ball.diffx = (ball.x+ball.radius-(plane.x+plane.width/2))
    ball.diffy = (ball.y+ball.radius-(plane.x+plane.height/2))
    if ball.diffy > 0 or ball.diffy < 0:
        ball.diff = ball.diffx/ball.diffy

    # plane hit the ball
    if(ball.x >= plane.x-ball.radius and ball.x <= plane.x+plane.width-ball.radius) and (ball.y >= plane.y-ball.radius and ball.y <= plane.y+plane.height-ball.radius):
        ball.directiony = 'up'
        ball.speedx = (ball.diffx)/4
        if ball.x+ball.radius<plane.x+plane.width/2:
            ball.speedx = 0-ball.speedx
            ball.directionx = 'left'
        else:          
            ball.directionx = 'right'

    return (ball, plane)

def prints(ball, plane, block, status, level):

    # some color for background
    if status.fullprint == 'true':
        DISPLAYSURF.fill(WHITE)

    # some useful info to caption for player
    pygame.display.set_caption('Points: ' + str(status.points) + ' lifes: ' + str(status.lifes) + ' level: ' + str(status.curlevel+1))

    # print ball and plate
    DISPLAYSURF.blit(ball.imageWhite, (ball.prevx, ball.prevy))  
    DISPLAYSURF.blit(plane.imageWhite, (plane.prevx, plane.y))
    
    DISPLAYSURF.blit(ball.image, (ball.x, ball.y))
    DISPLAYSURF.blit(plane.image, (plane.x, plane.y))

    # speed opimization
    x1 = (block.countx*block.width+(ball.x-block.countx*block.width))/block.width-1
    y1 = (block.county*block.height+(ball.y-block.county*block.height))/block.height-1
    if x1 < 2:
        x1 = 2
    elif x1 > block.countx-3:
            x1 = block.countx-3
    if y1 < 2:
        y1 = 2
    elif y1 > block.county-3:
            y1 = block.county-3

    # print blocks
    if status.fullprint == 'false': # speed optimization
        for x in range(x1-2,x1+3):
            for y in range(y1-2,y1+3):
                if level[x][y] == 1:
                    DISPLAYSURF.blit(block.blc1Img, (block.width*x, block.height*y))
                elif level[x][y] == 2:
                    DISPLAYSURF.blit(block.blc2Img, (block.width*x, block.height*y))
                elif level[x][y] > 2:
                    DISPLAYSURF.blit(block.blc3Img, (block.width*x, block.height*y))
    else:
        for x in range(0,block.countx):
            for y in range(0,block.county):
                if level[x][y] == 1:
                    DISPLAYSURF.blit(block.blc1Img, (block.width*x, block.height*y))
                elif level[x][y] == 2:
                    DISPLAYSURF.blit(block.blc2Img, (block.width*x, block.height*y))
                elif level[x][y] > 2:
                    DISPLAYSURF.blit(block.blc3Img, (block.width*x, block.height*y))

    #refresh
    pygame.display.update()
    fpsClock.tick(FPS)

    status.fullprint='false'

    return (ball, plane, block, status, level)

def paused(status):
  
    while status.pause == 'true':

        # some text
        text = font.render('press button "p"', True,(BLACK))      
        if BITS == 32:
            DISPLAYSURF.blit(text,(SCREENWIDTH/2-16/2*16, SCREENHEIGHT/2-16/2)) # 16 = count of charasters
        else:
            DISPLAYSURF.blit(txtImg, (SCREENWIDTH/2-168/2, SCREENHEIGHT/2-40/2))

        # update display
        pygame.display.update()
        fpsClock.tick(FPS)

        # handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if (event.key == K_p):      # return when key _p_ pressed
                    status.pause = 'false'
                    plane.move = 'none'

    DISPLAYSURF.blit(txtImgW, (SCREENWIDTH/2-168/2, SCREENHEIGHT/2-40/2))
    status.fullprint='false'

    # game running on
    return (status)

#objects
plane = Plane()
ball = Ball(8, plane.height)
block = Block()
status = Status()

# get the first level for use
level = loadLevel(status.curlevel)

while True: # the main game loop

    # objects moves
    (ball, plane) = moveObjects(ball, plane, status)

    # ball-blocks -collision
    (ball, plane, block, status, level) = ball2blockCollision(ball, plane, block, status, level)
  
    # ball-plane -collision
    (ball, plane) = ball2planeCollision(ball, plane)

    # controls
    (plane) = controls(plane)

    # prints
    (ball, plane, block, status, level) = prints(ball, plane, block, status, level)

    # game paused
    (status) = paused(status)
