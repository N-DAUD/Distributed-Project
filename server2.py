import socket
import threading 
import random

clients = set()
clients_lock = threading.Lock()

display_width = 1280
HEADER=64 #how many bytes we are going to recive it 
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DICONNECT"
PORT = 5555

#def Server2NewConnection():
#that line of code instead of writing --> SERVER="192.168.1.6" 
# because we do not need to make it hard coded 
SERVER2=socket.gethostbyname(socket.gethostname())
ADDR2=(SERVER2, PORT)
server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
 server2.bind(ADDR2) #bind the socket to the address 

except socket.error as e:
  print(str(e))



#this function will handle the communication between the client and the server
#this function will run in parallel for each client  
#conn is a socket object


def BuildMessage_block(x ,x1 ):
    return str(x)+","+str(x1)
def ParseMessage(st):
    st_list = st.split(',')
    if (len(st_list)<3):
        return "badop",0,0
    return str(st_list[0]), str(st_list[1]), str(st_list[2])




def handle_Client_Server2(conn2, addr2):

    print(f"[NEW CONNECTION] {addr2} connected.")
    connected=True
    while connected:
        #wait till something is sent over the socket 
        msgLen=conn2.recv(HEADER).decode(FORMAT) #blocking line of code
        
        if msgLen: 
         msg_Length=int(msgLen) 
         msg=conn2.recv(msg_Length).decode(FORMAT)
         print("received")
        if msg[0] == "0":
          x="0"
          print("Sending")
          conn2.send(x.encode(FORMAT))
          print("sent")
        elif msg[0] == "1":
          x=1
        elif msg[0] == "2":
          x = random.randrange(0, display_width-150)
          x1 = random.randrange(0, display_width-150)
          pos =BuildMessage_block(x,x1)
          print ("Sending Blocks")
          with clients_lock:
                    for c in clients:
                        c.sendall(pos.encode(FORMAT))
                        print("sent block")

        if msg ==DISCONNECT_MESSAGE:
          connected=False
            
         #print(f"[{addr2}]{msg}")
         #conn2.send("msg received".encode(FORMAT))
    conn2.close()

def startServer2():
      server2.listen()#listening for a new connection 
    
      print(f"listening server 2 is listening on {SERVER2} ")
      while True:
       #wait for a new connection to the server 
       #when the connection occur we store the address--> what ip address and what port it came from
       # then we store an actual object 
       # that will allow us to send information back to that connection 
       conn2 , addr2  = server2.accept()
       with clients_lock:
          clients.add(conn2)

       #when a new connection occur pass that connection to handle client  
       thread= threading.Thread(target=handle_Client_Server2, args=(conn2, addr2))
       thread.start()
       #how many threads are active in this python process
       print(f"[ACTIVE CONNECTION]{threading.activeCount() - 1}") 


print("[STARTING] server 2 is starting....")
startServer2()


