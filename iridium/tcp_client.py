import socket


class TCP_Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send(self, data):
        self.socket.send(data)

    def recv(self):
        return self.socket.recv(1024)

    def close(self):
        self.socket.close()
