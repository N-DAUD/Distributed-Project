import time
import random
import threading

import pygame
import socket

#This is the main file of the game

HEADER=64 #how many bytes we are going to recive it
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DICONNECT"
server1_Flag=0
server2_Flag=1
ClientPORT=5050

serverSocketLock = threading.RLock()
pygame.init()
display_width = 1280
display_height = 720

pos1 = []
pos2 = []
pos3 = []
ID = 0
x = 0.0
y = (display_height * 0.8)
x1, x2, x3 = 0.0, 0.0, 0.0
y1 = (display_height * 0.8)
y2 = (display_height * 0.8)
y3 = (display_height * 0.8)


def UpdateServer():
    global server1_Flag
    global server2_Flag
    global ClientPORT

    if server1_Flag==1:
       ClientPORT=5050
    else:
       server2_Flag=1
       ClientPORT=5555

#if Server2Flag ==0:
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER, ClientPORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(ADDR)#establish the connection with the server

def CheckConnection():
    global ClientPORT
    global server1_Flag
    global server2_Flag
    global client
    global resultcheck
    # devicesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)  # set a timeout value of seconds for socket operations.
    # connect_ex() function in Python's socket module is a non-blocking version of the connect() function.
    # It returns an error code instead of raising an exception if the connection fails.
    #  This can be useful for asynchronous programming,
    # where you don't want your program to block while waiting for a connection to be established.
    resultcheck = client.connect_ex((SERVER, ClientPORT))  # connect_ex() function returns a socket object

    if resultcheck == 0:
        if server1_Flag == 1:
            print(str(ClientPORT) + "print listening port")
            server1_Flag = 1
            server2_Flag = 0
            return True

        if server2_Flag == 1:
            print(str(ClientPORT) + "print listening port")
            server1_Flag = 0
            server2_Flag = 1
            return True

    else:
        if server1_Flag == 1:
            print(str(ClientPORT) + " is not listening on port ")
            ClientPORT = 5555
            server1_Flag = 0
            server2_Flag = 1
            client.close()
            return False

        if server2_Flag == 1:
            print(str(ClientPORT) + " is not listening on port ")
            ClientPORT = 5050
            server1_Flag = 1
            server2_Flag = 0
            client.close()
            return False


def Send(msg):

    message=msg.encode(FORMAT)
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)

    #subtract that from 64 to know how much to pad this
    # so the total lenght is 64
    #b means the byte representation of the stringsss
    send_length +=b' ' * (HEADER -len(send_length))
    client.send(send_length)
    client.send(message)
    ##print(client.recv(2048).decode(FORMAT))


def recieve():
    msgLen = client.recv(HEADER).decode(FORMAT)  # blocking line of code

    if msgLen:
        msg_Length = int(msgLen)
        msg = client.recv(msg_Length).decode(FORMAT)
    return msg

def BuildMessage(code,ID, x, y):
    return str(code)+","+str(ID)+","+str(x)+","+str(y)

def ParseMessage_block(st):
    st_list = st.split(',')
    """if (len(st_list) < 2):
        return "badop", 0, 0"""
    return float(st_list[0]), float(st_list[1])

def ParseMessage_pos(st):
    st_list = st.split('*')
    """if (len(st_list) < 3):
        return "badop", 0, 0"""
    return st_list[0], st_list[1] , st_list[2]

def ParseMessage(st):
    st_list = st.split(',')
    """if (len(st_list) < 2):
        return "badop", 0, 0"""
    return float(st_list[0]), float(st_list[1]), float(st_list[2]), float(st_list[3]), float(st_list[4]),float(st_list[5])



black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)

bright_red =(255, 0, 0)
bright_green = (0, 255, 0)
block_color = (53, 115, 255)
car_width = 40
car_height = 70
largeText = pygame.font.Font('freesansbold.ttf', 110)         # Text Fonts
smallText = pygame.font.Font('freesansbold.ttf', 25)



gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Racing Game")
clock = pygame.time.Clock()

img1 = pygame.image.load('car_black_small_1.png')
img2 = pygame.image.load('car_blue_small_1.png')
img3 = pygame.image.load('car_red_small_1.png')


def block1(block_x, block_y, block_w, block_h, color):
    pygame.draw.rect(gameDisplay, color, [block_x, block_y, block_w, block_h])


def block2(block_x, block_y, block_w, block_h, color):
    pygame.draw.rect(gameDisplay, color, [block_x, block_y, block_w, block_h])


def block_dodged(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("score: "+str(score), True, black)
    gameDisplay.blit(text, (0,0))


def car1(x, y):
    gameDisplay.blit(img1, (x, y))


def car2(x, y):
    gameDisplay.blit(img2, (x, y))


def car3(x, y):
    gameDisplay.blit(img3, (x, y))


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text,color):
    largeText = pygame.font.Font('freesansbold.ttf', 110)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(1)


def won():
    message_display('YOU WON', green)
    time.sleep(5)
    pygame.quit()
    quit()


def exit_game():
    client.close()
    #input()
    Send(DISCONNECT_MESSAGE)
    pygame.quit()
    quit()


def button(msg, x, y, w, h, inactive, active, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if (x + w > mouse[0] > x) and (y + h > mouse[1] > y):
        pygame.draw.rect(gameDisplay, active, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(gameDisplay, inactive, (x, y, w, h))

    textsurf1, textrect1 = text_objects(msg, smallText, black)
    textrect1.center = ((x + (w / 2)), (y+ (h / 2)))
    gameDisplay.blit(textsurf1, textrect1)


def main_menu():
    global ID

    menu = True
    UpdateServer()
    if CheckConnection() == True:

        Send("0,0,0,0")
        ##input()
        data=client.recv(2048)
        result = data.decode(FORMAT)
        if result == "3.0":
            print("received ID 3")
            exit_game()
        print(result)
        ID = int(float(result))
        print(ID)

        """Send(0)
        id = client.recv((2048).decode(FORMAT))
        ID = id"""
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    client.close()
                    #input()
                    Send(DISCONNECT_MESSAGE)
                    pygame.quit()
                    quit()
            gameDisplay.fill(white)

            TextSurf, TextRect = text_objects("Racing Cars", largeText, black)
            TextRect.center = ((display_width / 2), (display_height / 4))
            gameDisplay.blit(TextSurf, TextRect)

            button("!START!", 250, 400, 160, 80, green, bright_green, game_loop)
            button("QUIT :(", 900, 400, 160, 80, red, bright_red, exit_game)



            pygame.display.update()


def game_loop():

    global ID
    global pos1
    global pos2
    global pos3
    global x1, x2, x3, y1, y2, y3
    global x, y
    """
    client asks the server for the position of the blocks
    client recieves the message from the server and updates blocks
    client send to server the updated position
    
    
    """
    x = ((display_width * 0.2) + (ID*400))
    x_change = 0
    y_change = 0
    serverSocketLock.acquire()
    Send("2,0,0,0")
    print("after send")
    temp = client.recv(2048)
    serverSocketLock.release()
    block = ParseMessage_block(temp.decode(FORMAT))
    print("recieved")
    block1_startx = (block[0]) #random.randrange(0, display_width-150)
    block2_startx = (block[1]) #random.randrange(0, display_width - 150)
    block_starty = -500.0
    block_speed = 10.0
    block_width = 150.0
    block_height = 45.0
    score = 0






    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10
                elif event.key == pygame.K_RIGHT:
                    x_change = 10
                elif event.key == pygame.K_UP:
                    y_change = -10
                elif event.key == pygame.K_DOWN:
                    y_change = 10

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0


        x += x_change
        y += y_change
        if x < 0:
            x = 0

        if x > display_width - car_width:
            x = display_width - car_width

        if y > display_height - car_height:
            y = float(display_height - car_height)

        if y < display_height * 0.4:
            y = display_height * 0.4



        update = BuildMessage(1, ID, x, y)
        print(update)
        serverSocketLock.acquire()
        Send(update)
        temp_rec = client.recv(2048)
        temp_update = temp_rec.decode(FORMAT)
        serverSocketLock.release()
        ##print(temp_update)
        print(temp_update)
        cars = ParseMessage(temp_update)
        print("printing cars")
        print(cars)
        print(cars[0])
        print(cars[1])
        print(cars[2])

        """ pos1 = ParseMessage(cars[0])
        print(pos1)
        pos2 = ParseMessage(cars[1])
        print(pos2)
        pos3 = ParseMessage(cars[2])
        print(pos3)"""
        ##updated_pos = ParseMessage(cars)
        x1, y1 = cars[0], cars[1]
        x2, y2 = cars[2], cars[3]
        x3, y3 = cars[4], cars[5]

        ##UpdateServer()
        ##if CheckConnection():
        """str1 = BuildMessage(1, x, y)
        Send(str1)
        temp = client.recv(2048)
        cars =  temp.decode(FORMAT)
        x, y = cars[0]
        x2, y2 = cars[1]
        x3, y3 = cars[2]"""
        #Send("hello everyone")
        #client.close()
        #Send(DISCONNECT_MESSAGE)


        gameDisplay.fill(white)

        block1(block1_startx, block_starty, block_width, block_height, block_color)
        block2(block2_startx, block_starty, block_width, block_height, block_color)

        block_starty += block_speed
        serverSocketLock.acquire()
        if ID == 0:
            car1(x, y)
            car2(x2, x2)
            car3(x3, y3)
        elif ID == 1:
            car1(x1, y1)
            car2(x, y)
            car3(x3, y3)
        elif ID == 2:
            car1(x1, y1)
            car2(x2, x2)
            car3(x, y)
        serverSocketLock.release()
        block_dodged(score)

        if score == 1000:
            won()

        if block_starty > display_height:
            block_starty = 0.0 - display_height
            serverSocketLock.acquire()
            Send("2,0,0,0")
            temp = client.recv(2048)
            serverSocketLock.release()
            block = ParseMessage_block(temp.decode(FORMAT))
            print("received")
            block1_startx = float(block[0])
            block2_startx = float(block[1]) #random.randrange(0, display_width)
            print("done")
            if block_speed != 20:
                block_speed += 1
            score += 100

        if y < block_starty + block_height:
            if ((x > block1_startx) and (x < block1_startx+block_width)) or ((x + car_width > block1_startx) and (x+car_width < block1_startx+block_width)):
                print("collision happened")
                if block_speed != 7:
                    block_speed += -1
                score += -100
                block_starty = 0 - display_height
                serverSocketLock.acquire()
                Send("2,0,0,0")
                temp = client.recv(2048)
                serverSocketLock.release()
                block = ParseMessage_block(temp.decode(FORMAT))
                block1_startx = float(block[0])
                block2_startx = float(block[1])
                #block1_startx = random.randrange(0, display_width-150)

        if y < block_starty + block_height:
            if ((x > block2_startx) and (x < block2_startx+block_width)) or ((x + car_width > block2_startx) and (x+car_width < block2_startx+block_width)):
                print("collision happened")
                score += -100
                block_starty = 0 - display_height
                serverSocketLock.acquire()
                Send("2,0,0,0")
                temp = client.recv(2048)
                serverSocketLock.release()
                block = ParseMessage_block(temp.decode(FORMAT))
                block2_startx = float(block[1])
                block1_startx = float(block[0])
                ##block2_startx = random.randrange(0, display_width-150)


        pygame.display.update()
        clock.tick(60)


#if __name__ == "__main__":
main_menu()
game_loop()
exit_game()


