import socket
import threading
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB configuration
password = "bs91HZDXuubCNpsE"
uri = f"mongodb+srv://mostafahesham1939:{password}@games.w7y92bm.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
clientdb = MongoClient(uri, server_api=ServerApi('1'))

# Select database and collection
db = clientdb['projectgame']
collection = db['players']

print("Connected to MongoDB.")

# List to store connected clients
clients = []
clients_lock = threading.Lock()

# Game display dimensions
display_width = 1280
display_height = 720

# Lock for server socket
serverSocketLock = threading.RLock()

# Player IDs and positions
ID = 3
x = (display_width * 0.2)
x1 = ((display_width * 0.2) + 400)
x2 = ((display_width * 0.2) + 800)
y = display_height * 0.8
y1 = display_height * 0.8
y2 = display_height * 0.8
pos1 = x, y
pos2 = x1, y1
pos3 = x2, y1

pos_arr = pos1, pos2, pos3

available_IDS = [0, 1, 2]

print(pos_arr[0])
print(pos_arr[1])
print(pos_arr[2])

HEADER = 64  # how many bytes we are going to receive
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DICONNECT"
PORT = 5555

#that line of code instead of writing --> SERVER="192.168.1.6" 
# because we do not need to make it hard coded 
SERVER2 = socket.gethostbyname(socket.gethostname())
ADDR2 = (SERVER2, PORT)
#socket.SOCK_STREAM is the socket type
#AF_INET is the internet address family this tells what type of socket or type of ip address 
#for specific connection 
#socket.SOCK_STREAM we are streaming data through the socket 
server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server2.bind(ADDR2)  # bind the socket to the address
except socket.error as e:
    print(str(e))


# Database functions
def store_player_data(user_id, user_score, win_user):
    data = {
        'user_id': user_id,
        'user_score': user_score,
        'win_user': win_user
    }
    # Store data in MongoDB
    collection.update_one(
        {'user_id': user_id},
        {'$set': data},
        upsert=True
    )
    print('Data stored successfully.')


def retrieve_player_data(user_id):
    # Retrieve data from MongoDB
    data = collection.find_one({'user_id': user_id})
    if data:
        print('User ID:', data['user_id'])
        print('User Score:', data['user_score'])
        print('Win User:', data['win_user'])
    else:
        print('User not found.')


def update_player_score(user_id, new_score):
    # Update player score
    collection.update_one(
        {'user_id': user_id},
        {'$set': {'user_score': new_score}}
    )
    print('Player score updated successfully.')


def increment_player_score(user_id, increment):
    # Increment player score
    collection.update_one(
        {'user_id': user_id},
        {'$inc': {'user_score': increment}}
    )
    print('Player score incremented successfully.')


def delete_player_data(user_id):
    # Delete player data
    result = collection.delete_one({'user_id': user_id})
    if result.deleted_count > 0:
        print('Player data deleted successfully.')
    else:
        print('Player not found.')




def BuildMessage_pos(pos_arr):
    return str(x) + "," + str(x1)


def BuildMessage_block(x, x1):
    serverSocketLock.acquire()
    string = str(x) + "," + str(x1)
    serverSocketLock.release()
    return string


def ParseMessage(st):
    serverSocketLock.acquire()
    st_list = st.split(',')
    if len(st_list) < 4:
        return "badop", 0, 0
    serverSocketLock.release()
    return str(st_list[0]), str(st_list[1]), str(st_list[2]), str(st_list[3])


def Update(msg):
    global pos1
    global pos2
    global pos3

    #msg[2] stores the current x position 
    #msg[3] stores the current y position
    #pos1[0] stores the x position of the car1
    #pos1[1] stores the y position of the car1
        
    serverSocketLock.acquire()
    if msg[1] == "0":
        pos1[0] = int(msg[2])
        pos1[1] = int(msg[3])
    elif msg[1] == "1":
        pos2[0] = int(msg[2])
        pos2[1] = int(msg[3])
    elif msg[1] == "2":
        pos3[0] = int(msg[2])
        pos3[1] = int(msg[3])

    car1 = str(pos1[0]) + "," + str(pos1[1])
    car2 = str(pos2[0]) + "," + str(pos2[1])
    car3 = str(pos3[0]) + "," + str(pos3[1])

    cars = car1 + "*" + car2 + "*" + car3
    serverSocketLock.release()
    return cars


#this function will handle the communication between the client and the server
#this function will run in parallel for each client  
#conn is a socket object
def handle_Client_Server2(conn2, addr2):
    global ID
    global available_IDS
    global pos1
    global pos2
    global pos3

    print(f"[NEW CONNECTION] {addr2} connected.")
    connected = True
    while connected:
        # Wait till something is sent over the socket
        msgLen = conn2.recv(HEADER).decode(FORMAT)  # blocking line of code
        serverSocketLock.acquire() #critical section there is a lock here because that part is shared between the client threads 
                                   #for example one client is updating the position at a time

        if msgLen:
            msg_Length = int(msgLen) #first the message lenght is recieved then the actual message 
            msg = conn2.recv(msg_Length).decode(FORMAT)
            print("received")

            #msg[0] is related to the operation id 
                    
            if msg[0] == "0": #if msg[0] is equal to zero then insert the IDS into variable ID then send it --> operation zero
                if available_IDS[0] != 3:
                    ID = available_IDS[0]
                    available_IDS[0] = 3
                elif available_IDS[1] != 3:
                    ID = available_IDS[1]
                    available_IDS[1] = 3
                elif available_IDS[2] != 3:
                    ID = available_IDS[2]
                    available_IDS[2] = 3
                else:
                    ID = 3

                sent_ID = str(ID)
                conn2.send(sent_ID.encode(FORMAT))
                print("sent ID = " + sent_ID)

            elif msg[0] == "1": #if msg[0] is equal to one then update the position of the car --> operation one
                token = msg[1]
                cars = Update(msg)
                for c in clients:
                    c.send(cars.encode(FORMAT))
                print("updated positions")

            elif msg[0] == "2":#if msg[0] is equal to 2 then that is related to the block generation in a random way --> operation two
                b = random.randrange(0, display_width - 150)
                b1 = random.randrange(0, display_width - 150)
                pos = BuildMessage_block(b, b1)
                print("Sending Blocks")
                for c in clients:
                    c.send(pos.encode(FORMAT))
                print("sent block")

        if msg == DISCONNECT_MESSAGE:
            connected = False

        serverSocketLock.release()#release the lock here

    conn2.close()


def startServer2():
    server2.listen()  # listening for a new connection

    print(f"listening server 2 is listening on {SERVER2}")
    while True:
       #wait for a new connection to the server 
       #when the connection occur we store the address--> what ip address and what port it came from
       # then we store an actual object 
       # that will allow us to send information back to that connection 
        conn2, addr2 = server2.accept()  # wait for a new connection to the server (blocking line of code)

        
        clients.append(conn2)

        #when a new connection occur pass that connection to handle client  
        thread = threading.Thread(target=handle_Client_Server2, args=(conn2, addr2))  # pass the connection to handle client
        thread.start()

        print(f"[ACTIVE CONNECTION]{threading.activeCount() - 1}")


if __name__ == "__main__":
    print("[STARTING] server 2 is starting....")
    startServer2()
