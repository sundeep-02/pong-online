import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_id = "192.168.1.7"
        self.port = 5555
        self.pos = self.connect_and_recv()

    def getPos(self):
        return self.pos

    def connect_and_recv(self):
        self.client.connect((self.server_id, self.port))
        return self.client.recv(2048).decode()

    def send_and_recv(self, data):
        self.client.send(str.encode(data))
        return self.client.recv(2048).decode()