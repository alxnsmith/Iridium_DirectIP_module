from .tcp_server import TCP_Server

from .mail_client import Mail


class Iridium:
    Mail = Mail
    TCP_Server = TCP_Server

    @staticmethod
    def serve(host: str, port: int,  handler: TCP_Server.HANDLER_TYPE):
        server = TCP_Server(host, port)
        server.start(handler)
