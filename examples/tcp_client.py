import socket


class TCP_Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', 62372))
        self.socket.connect((self.host, self.port))

    def send(self, data):
        self.socket.send(data)

    def recv(self):
        return self.socket.recv(1024)

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    # ADDR = ['directip.sbd.iridium.com', 10800] # Iridium
    ADDR = ["79.137.133.230", 10800]  # NILLKIZZ

    print(f"Connecting to server {ADDR[0]}:{ADDR[1]}")
    client = TCP_Client(*ADDR)
    print("Connected to server")
    client.send(
        b"01002E4100154D7367313330303033343031303132333435300000421346494D4549333030303334303130313233343530")
    # print("Received: ", client.recv())
    client.close()
