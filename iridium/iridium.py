from .tcp_server import TCP_Server
from .tcp_client import TCP_Client
from .services.Messages import MT_Message, MO_Message, MT_Confirmation

from .mail_client import Mail


class Iridium:
    Mail = Mail
    TCP_Server = TCP_Server
    TCP_Client = TCP_Client

    MT_Message = MT_Message
    MO_Message = MO_Message
    MT_Confirmation = MT_Confirmation

    @staticmethod
    def serve(host: str, port: int, handler):
        server = TCP_Server(host, port)
        server.start(handler)
