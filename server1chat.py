import socket 
import threading 

HEADER=64 #how many bytes we are going to recive it 
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DICONNECT"
PORT = 8080

#def Server2NewConnection():
#that line of code instead of writing --> SERVER="192.168.1.6" 
# because we do not need to make it hard coded 
CHATSERVER=socket.gethostbyname(socket.gethostname())
ADDR=(CHATSERVER, PORT)
server1chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
 server1chat.bind(ADDR) #bind the socket to the address 

except socket.error as e:
  print(str(e))


def BuildMessage_block(x ,x1 ):
    return str(x)+","+str(x1)
def ParseMessage(st):
    st_list = st.split(',')
    if (len(st_list)<3):
        return "badop",0,0
    return str(st_list[0]), str(st_list[1]), str(st_list[2])

#this function will handle the communication between the client and the server
#this function will run in parallel for each client  
#conn is a socket object
def handle_Client_ServerChat(conn, addr):
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


def startServerChat():
      server1chat.listen()#listening for a new connection 
    
      print(f"listening server 1 Chat is listening on {CHATSERVER} ")
      while True:
       #wait for a new connection to the server 
       #when the connection occur we store the address--> what ip address and what port it came from
       # then we store an actual object 
       # that will allow us to send information back to that connection 
       conn , addr  = server1chat.accept()

       #when a new connection occur pass that connection to handle client  
       thread= threading.Thread(target=handle_Client_ServerChat, args=(conn, addr))
       thread.start()
       #how many threads are active in this python process
       print(f"[ACTIVE CONNECTION]{threading.activeCount() - 1}") 



class Message:
       def __init__(self, text):
        self.text = text
        self.nextMessage = None
 
class MessageList:
       def __init__(self):
        self.frontMessage = None

       def add(self, text):
         newMessage = Message(text)

        # if the front message is empty add the front message to it 
         if self.frontMessage is None:
            self.frontMessage = newMessage

         else:
            newMessage.nextMessage = self.frontMessage
            self.frontMessage = newMessage



   

