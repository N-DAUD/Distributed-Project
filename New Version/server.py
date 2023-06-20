import random
import socket
from _thread import *
from player import Player
from block import Block
import pickle
import random
import pygame

server = socket.gethostbyname(socket.gethostname())    #put the ip of the host
port = 5050

x1 = random.randrange(0,1200)
x2 = random.randrange(0,1200)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


players = [Player(300,400,40,80,(255,0,0), 0), Player(700,400, 40,80, (0,0,255), 0)]
blocks = [Block(x1, 200, 150, 50, (132, 85, 85)), Block(x2, 200, 150, 50, (132, 85, 85))]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    #conn.send(pickle.dumps(blocks[0]))
    #conn.send(pickle.dumps(blocks[1]))
    reply1 = ""
    reply2 = ""
    reply3 = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply1 = players[0]

                else:
                    reply1 = players[1]


                print("Received: ", data)
                print("Sending : ", reply1)


            conn.sendall(pickle.dumps(reply1))
            #conn.sendall(pickle.dumps(reply2))
            #conn.sendall(pickle.dumps(reply3))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1