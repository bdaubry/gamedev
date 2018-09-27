import pygame
import math
import pymunk
from pymunk import Vec2d

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("4.png")
        self.rect = self.image.get_rect()

class Ball(pygame.sprite.Sprite):
    def __init__(self, loc, space):
        pygame.sprite.Sprite.__init__(self)
        #self.name = name
        self.sizex = 25
        self.sizey = 25
        #self.image = pygame.transform.scale(pygame.image.load('ball.png'), (self.sizex,self.sizey))
        #self.rect = self.image.get_rect()
        self.image = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
        pygame.draw.circle(self.image, pygame.Color('steelblue2'), (self.sizex, self.sizey), 29)
        self.rect = self.image.get_rect(center=loc)
        self.orig_image = self.image
        #self.rect.inflate(-30,-30)
        self.rect.x = loc[0]
        self.rect.y = loc[1]
        self.body = pymunk.Body()
        self.shape = pymunk.Circle(self.body, radius=30)
        self.shape.density = .0001
        self.shape.friction = .1
        self.shape.elasticity = .99
        self.body.position = loc
        self.space = space
        self.space.add(self.body, self.shape)

    # def update(self):
    #     newpos = self.calcnewpos(self.rect,self.loc)
    #     self.rect = newpos

    def grow(self, growbool):
        if growbool == True:
            self.rect.inflate_ip(2, 2)
            self.sizex +=2
            self.sizey +=2
            self.image = pygame.transform.scale(pygame.image.load('ball.png'), (self.sizex,self.sizey))
        else:
            self.image = pygame.transform.scale(pygame.image.load('ball.png'), (self.sizex,self.sizey))





    # def calcnewpos(self,rect,vector):
    #     (angle,z) = vector
    #     (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
    #     return rect.move(dx,dy)
        
