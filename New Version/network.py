import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p



    def connect(self):
        try:
            self.client.connect(self.addr)

            #B1 = pickle.loads(self.client.recv(2048))
            #B2 = pickle.loads(self.client.recv(2048))

            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            p = pickle.loads(self.client.recv(2048))
            #b1 = pickle.loads(self.client.recv(2048))
            #b2 = pickle.loads(self.client.recv(2048))
            return p
        except socket.error as e:
            print(e)