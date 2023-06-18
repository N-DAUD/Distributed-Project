import socket

HEADER=64 #how many bytes we are going to recive it 
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DICONNECT"
server1_Flag=0
server2_Flag=1
ClientPORT=5050


#that line of code instead of writing --> SERVER="192.168.1.6" 
# because we do not need to make it hard coded 
#so we get the IPV4 in a dynamic way 

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
    #devicesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5) #set a timeout value of seconds for socket operations.
    #connect_ex() function in Python's socket module is a non-blocking version of the connect() function. 
    # It returns an error code instead of raising an exception if the connection fails.
    #  This can be useful for asynchronous programming, 
    # where you don't want your program to block while waiting for a connection to be established.
    resultcheck = client.connect_ex((SERVER, ClientPORT))#connect_ex() function returns a socket object

    if resultcheck == 0:
        if server1_Flag==1:
         print(str(ClientPORT) + "print listening port")
         server1_Flag=1
         server2_Flag=0
         return True
        
        if server2_Flag==1:
         print(str(ClientPORT) + "print listening port")
         server1_Flag=0
         server2_Flag=1
         return True

    else:
         if server1_Flag==1:
          print(str(ClientPORT) + " is not listening on port ")
          ClientPORT=5555
          server1_Flag=0
          server2_Flag=1
          client.close()  
          return False
         
         if server2_Flag==1: 
          print(str(ClientPORT) + " is not listening on port ")
          ClientPORT=5050
          server1_Flag=1
          server2_Flag=0
          client.close()
          return False
  
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


flag=True
while flag==True:
 UpdateServer()  

 if True==CheckConnection():
   Send("hello") 
   Send("hello everyone")
   client.close()
   input()
   Send(DISCONNECT_MESSAGE)
   


       

    


         

         
         


 