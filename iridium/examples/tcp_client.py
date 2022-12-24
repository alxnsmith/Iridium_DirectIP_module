import socket


class TCP_Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.bind(('0.0.0.0', 62372))
        self.socket.connect((self.host, self.port))

    def send(self, data):
        self.socket.send(data)

    def recv(self):
        return self.socket.recv(1024)

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    # ADDR = ['directip.sbd.iridium.com', 10800] # Iridium
    # ADDR = ["79.137.133.230", 10800]  # NILLKIZZ
    ADDR = ["0.0.0.0", 62372]  # Local

    print(f"Connecting to server {ADDR[0]}:{ADDR[1]}")
    client = TCP_Client(*ADDR)
    print("Connected to server")
    MO_Message = '01004A01001CC7C8836433303032333430363930303236333000049B0000550705B303000B004422675339760000000402001A04070120A9050755300F98D40F046001F604330000C007341300'
    MT_Message = '01002E4100154D7367313330303033343031303132333435300000421346494D4549333030303334303130313233343530'

    client.send(bytes.fromhex(MO_Message))
    client.close()
