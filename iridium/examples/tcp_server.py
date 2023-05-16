import socket
from datetime import datetime


class TCP_Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

    def accept(self):
        return self.socket.accept()

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    server = TCP_Server("", 62372)
    # Accept data and print it
    while True:
        client, address = server.accept()
        print("Connected to: ", address)
        print("Waiting for data...")

        try:
            empty_counter = 0
            data = b''
            while True:
                received = client.recv(1024)
                if received == b'':
                    empty_counter += 1
                    if empty_counter == 3:
                        print('Closing connection, no data received for 3 times')
                        break
                else:
                    empty_counter = 0
                    data += received
                    print('Received: ', received)

            if data != b'':
                # Filename with datetime as prefix
                with open('data_log.txt', 'ab') as f:
                    to_write = b'=' * 80 + b'\n'
                    to_write += datetime.now().strftime("%Y.%m.%d_%H:%M:%S").encode()
                    to_write += b'\n'
                    to_write += ("IP: " + address[0] + '\n').encode()
                    to_write += b'\n'
                    to_write += data
                    to_write += b'\n'
                    f.write(to_write)
        except Exception:
            client.close()
            print("Connection closed")
        finally:
            client.close()
            print("Connection closed")
