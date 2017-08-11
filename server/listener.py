from socket import socket, SO_REUSEADDR, SOL_SOCKET, timeout
from threading import Thread

from chadt.connection_status import ConnectionStatus

class Listener:
    
    def __init__(self, server_connections, listening_port):
        self.server_connections = server_connections
        self.listening_socket = self.initialize_socket(listening_port)
        self.status = ConnectionStatus.STOPPED

    def initialize_socket(self, port):
        s = socket()
        s.settimeout(2)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(("", port))
        s.listen()
        return s

    def start_listening(self):
        if self.status == ConnectionStatus.STOPPED:
            self.status = ConnectionStatus.RUNNING
            Thread(target = self.listen).start()
        elif self.status == ConnectionStatus.STOPPING:
            raise RuntimeError("Listener is still stopping, cannot restart yet.")

    def stop_listening(self):
        if self.status == ConnectionStatus.RUNNING:
            self.status = ConnectionStatus.STOPPING

    def shutdown(self):
        if self.status == ConnectionStatus.RUNNING:
            self.stop_listening()
        self.listening_socket.close()

    def listen(self):
        while self.status == ConnectionStatus.RUNNING:
            try:
                new_connection = self.listening_socket.accept()
                self.forward_connection(new_connection)
            except timeout:
                pass
        self.status = ConnectionStatus.STOPPED

    def forward_connection(self, new_connection):
        self.server_connections.append(new_connection)
