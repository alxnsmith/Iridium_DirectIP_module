import socket
from datetime import datetime


class TCP_Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

    def accept(self):
        return self.socket.accept()

    def close(self):
        self.socket.close()

    def start(self, handler):
        while True:
            client, address = self.accept()
            with client:
                print("Connected to: ", address)
                print("Waiting for data...")

                try:
                    data = self._accept_data(client)
                    if data != b'':
                        handler(data, address, client)
                except Exception as e:
                    print("Error: ", e)

            print("Connection closed")

    @staticmethod
    def _accept_data(client: socket.SocketType, size: int = 1024, empty_to_close: int = 3) -> bytes:
        empty_counter = 0
        data = b''

        while True:
            received = client.recv(size)
            if received != b'':
                empty_counter = 0
                data += received
                print('Received: ', received)
            else:
                empty_counter += 1
                if empty_counter >= empty_to_close:
                    print(
                        f'Closing connection, no data received for {empty_to_close} times')
                    break
        return data


if __name__ == "__main__":
    def test_handler(data: bytes, address: tuple, _):
        # Filename with datetime as prefix
        with open('data.log', 'ab') as f:
            to_write = ('='*80 + '\n').encode()
            to_write += datetime.now().strftime("%Y.%m.%d_%H:%M:%S").encode()
            to_write += b'\n'
            to_write += ("IP: " + address[0] + '\n').encode()
            to_write += b'\n'
            to_write += data
            to_write += b'\n'
            f.write(to_write)
            _.sendall(b'OK')

    TCP_Server("", 62372).start(test_handler)
