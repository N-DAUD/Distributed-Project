import socket
import threading 
#from server2 import*


HEADER=64 #how many bytes we are going to recive it 
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DICONNECT"
PORT = 5050
#that line of code instead of writing --> SERVER="192.168.1.6" 
# because we do not need to make it hard coded 
#socket.SOCK_STREAM is the socket type
#AF_INET is the internet address family 
 
#SERVER="192.168.0.0"
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
 server.bind(ADDR) #bind the socket to the address 

except socket.error as e:
     print(str(e))
 

#this function will handle the communication between the client and the server
#this function will run in parallel for each client  
#conn is a socket object
def handle_Client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected=True
    while connected:
        #wait till something is sent over the socket 
        msgLen=conn.recv(HEADER).decode(FORMAT) #blocking line of code

        if msgLen: 
         msg_Length=int(msgLen) 
         msg=conn.recv(msg_Length).decode(FORMAT)

         if msg ==DISCONNECT_MESSAGE:
            connected=False
            
         print(f"[{addr}]{msg}")
         conn.send("msg received".encode(FORMAT))
    conn.close()


def start():
    server.listen()#listening for a new connection from client 

    print(f"listening server is listening on {SERVER} ")
    while True:
       #wait for a new connection to the server 
       #when the connection occur we store the address--> what ip address and what port it came from
       # then we store an actual object 
       # that will allow us to send information back to that connection 
       conn , addr  = server.accept()

       #when a new connection occur pass that connection to handle client  
       thread= threading.Thread(target=handle_Client, args=(conn, addr))
       thread.start()
       #how many threads are active in this python process
       print(f"[ACTIVE CONNECTION]{threading.activeCount() - 1}") 


       

print("[STARTING] server 1 is starting....")
start()


