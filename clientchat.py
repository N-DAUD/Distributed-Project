import socket
import threading

HEADER=64 # Number of bytes we are going to receive
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DICONNECT"

ClientPORT=8080


SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER, ClientPORT)
alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect_ex((SERVER, ClientPORT))
"""def CheckConnection():
    global resultcheck
    #devicesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5) #set a timeout value of seconds for socket operations.
    #connect_ex() function in Python's socket module is a non-blocking version of the connect() function. 
    # It returns an error code instead of raising an exception if the connection fails.
    #  This can be useful for asynchronous programming, 
    # where you don't want your program to block while waiting for a connection to be established.
    resultcheck = client.connect_ex((SERVER, ClientPORT))#connect_ex() function returns a socket object

    if resultcheck == 0:
        print(str(ClientPORT) + "print listening port")
        return True
        
    else:
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
    print(client.recv(2048).decode(FORMAT))

         
CheckConnection() """

# Receive messages from the server.
def client_receive():
    while True:
        try:
            message = client.recv(200).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break

#Send messages to the server.
def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))


# Start receiving and sending threads
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
