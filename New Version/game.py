import pygame
from network import Network
from block import Block
from player import Player
import random

pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red =(255, 0, 0)
bright_green = (0, 255, 0)
block_color = (132, 85, 85)
# Text Fonts

width = 1200
height = 600
def getrand():
    return random.randrange(0,1200)


x1 = getrand()
x2 = getrand()
y = -500
score = 0


win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

img1 = pygame.image.load('car_black_small_1.png')
img2 = pygame.image.load('car_blue_small_1.png')
img3 = pygame.image.load('car_red_small_1.png')
bg = pygame.image.load('Backgroung.jpg')

def block_dodged(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("score: "+str(score), True, bright_green)
    win.blit(text, (0,0))

def block1(block_x, block_y, block_w, block_h, color):
    pygame.draw.rect(win, color, [block_x, block_y, block_w, block_h])

def block2(block_x, block_y, block_w, block_h, color):
    pygame.draw.rect(win, color, [block_x, block_y, block_w, block_h])

def redrawWindow(win,player, player2):
    #win.fill((255,255,255))
    win.blit(bg, (0, 0))
    player.draw(win)
    player2.draw(win)

    block1(x1, y, 150, 45, block_color)
    block2(x2, y, 150, 45, block_color)
    block_dodged(score)
    pygame.display.update()


def main():
    global x1
    global x2
    global y
    global score


    run = True
    n = Network()
    p = n.getP()

    clock = pygame.time.Clock()


    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


        y += 10

        if y > 700:
            x1 = getrand()
            x2 = getrand()
            y = -500
            score += 100


        p.move()
        redrawWindow(win, p, p2)


main()