from .tcp_server import TCP_Server

from .mail_client import Mail


class Iridium:
    Mail = Mail
    TCP_Server = TCP_Server

    def __init__(self, config):
        self.config = config

    def serve(self, handler: TCP_Server.HANDLER_TYPE):
        server = TCP_Server(self.config['host'], self.config['port'])
        server.start(handler)
