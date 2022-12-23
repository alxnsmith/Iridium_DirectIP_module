from mail_client import send_message
from tcp_server import TCP_Server


class Iridium:
    def __init__(self, config):
        self.config = config

    def mail(self, imei: str, message: bytes):
        return send_message(imei, message)

    def serve(self, handler: TCP_Server.HANDLER_TYPE):
        server = TCP_Server(self.config['host'], self.config['port'])
        server.start(handler)
