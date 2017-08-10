from socket import socket, SO_REUSEADDR, SOL_SOCKET, timeout
from threading import Thread

from chadt.connection_status import ConnectionStatus

class Listener:
    
    def __init__(self, connections, listening_port):
        self.connections = connections
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

    def stop_listening(self):
        if self.status == ConnectionStatus.RUNNING:
            self.status = ConnectionStatus.STOPPING

    def shutdown(self):
        if self.status == ConnectionStatus.RUNNING:
            self.stop_listening()
        
        self.listen_socket.shutdown() # is this useful?
        self.listening_socket.close()

    def listen(self):
        while self.status == ConnectionStatus.RUNNING:
            try:
                new_connection = self.listening_socket.accept()
                self.return_connection(new_connection)
            except timeout:
                pass
        self.status = ConnectionStatus.STOPPED

    def return_connection(self, new_connection):
        self.connections.append(new_connection)
