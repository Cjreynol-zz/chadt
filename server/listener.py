from socket import socket, SO_REUSEADDR, SOL_SOCKET, timeout

from chadt.chadt_component import ChadtComponent


class Listener(ChadtComponent):
    
    def __init__(self, server_connections, listening_port):
        self.server_connections = server_connections
        self.listening_socket = self.initialize_socket(listening_port)

        super().__init__()

    def initialize_socket(self, port):
        s = socket()
        s.settimeout(2)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(("", port))
        s.listen()
        return s

    def start(self):
        super().start(self.listen)

    def shutdown(self):
        super().shutdown(self.listening_socket)

    def listen(self):
        try:
            new_connection = self.listening_socket.accept()
            self.forward_connection(new_connection)
        except timeout:
            pass

    def forward_connection(self, new_connection):
        self.server_connections.append(new_connection)
