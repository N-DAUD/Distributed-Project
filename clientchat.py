import socket

HEADER=64 #how many bytes we are going to recive it 
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DICONNECT"
server1_Flag=0
server2_Flag=1
ClientPORT=8080


SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER, ClientPORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def CheckConnection():
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

         

