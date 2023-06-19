import socket 
import threading 

HEADER=64 #how many bytes we are going to recive it 
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DICONECT"
PORT = 8080
clients = []
aliases = []
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

server1chat.listen()#listening for a new connection 

def broadcast(message):
    for client in clients:
        client.send(message)




#this function will handle the communication between the client and the server
#this function will run in parallel for each client  
#conn is a socket object
def handle_Client_ServerChat(conn, addr):
    ##print(f"[NEW CONNECTION] {addr} connected.")
    connected=True
    while connected:
        
        try:#wait till something is sent over the socket 
            #msgLen=conn.recv(HEADER).decode(FORMAT) #blocking line of code

            
            #msg_Length=int(msgLen) 
            msg=conn.recv(200)
                
                #MessageList.add(msg)
                    
            print(f"[{addr}]{msg}")
            #conn.send("msg received".encode(FORMAT))
            broadcast(msg)

        except:
           index = clients.index(conn)
           clients.remove(conn)
           conn.close()
           alias = aliases[index]
           broadcast(f'{alias} has left the chat room!'.encode(FORMAT))
           aliases.remove(alias)
           break


def startServerChat():
      #server1chat.listen()#listening for a new connection 
    
      
      while True:
       print(f"listening server 1 Chat is listening on {CHATSERVER} ")
       #wait for a new connection to the server 
       #when the connection occur we store the address--> what ip address and what port it came from
       # then we store an actual object 
       # that will allow us to send information back to that connection 
       conn , addr  = server1chat.accept()
       print ("connection was established with " + str(addr))
       conn.send('alias?'.encode('utf-8'))
       alias = conn.recv(200).decode(FORMAT)
       aliases.append(alias)
       clients.append(conn)
       print (f"Client alias is: {alias}".encode(FORMAT))
       broadcast(f"{alias} has connected to the chat room ".encode(FORMAT))
       conn.send("!You are now connected!".encode(FORMAT))

       #when a new connection occur pass that connection to handle client  
       thread= threading.Thread(target=handle_Client_ServerChat, args=(conn, addr))
       thread.start()
       #how many threads are active in this python process
       ##print(f"[ACTIVE CONNECTION]{threading.activeCount() - 1}") 
       ##


if __name__ == "__main__":
    startServerChat()



   

