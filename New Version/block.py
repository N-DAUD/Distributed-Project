import pygame
import random

class Block():
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.speed = 3
        self.m_speed = 15


    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)



    def new_pos(self):
        if self.y > 600:
            self.x = random.randrange(0, 1200)
            self.y = -500
        else:
            self.y += self.speed
            if self.speed < self.m_speed:
                self.speed += 1

        self.update()

    def collide(self):
        self.x = random.randrange(0, 1200)
        self.y = -500
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)