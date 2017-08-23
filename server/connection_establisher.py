from socket import socket, SO_REUSEADDR, SOL_SOCKET, timeout

from chadt.chadt_component import ChadtComponent
from chadt.chadt_connection import ChadtConnection
from chadt.message import Message


class ConnectionEstablisher(ChadtComponent):

    DEFAULT_USERNAME_BASE = "User"
    
    def __init__(self, listening_port, server_client_dict, server_processing_queue):
        self.listening_socket = self.initialize_socket(listening_port)
        self.server_connections = []
        self.temp_id_counter = 0

        self.server_client_dict = server_client_dict
        self.server_processing_queue = server_processing_queue

        super().__init__()

    def initialize_socket(self, port):
        s = socket()
        s.settimeout(ChadtComponent.SOCKET_TIMEOUT)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(("", port))
        s.listen()
        return s

    def start(self):
        super().start(self.listen_and_process)

    def shutdown(self):
        super().shutdown(self.listening_socket)

    def listen_and_process(self):
        self.listen()
        self.process_connections()

    def listen(self):
        try:
            new_connection = self.listening_socket.accept()
            self.server_connections.append(new_connection)
        except timeout:
            pass

    def process_connections(self):
        if len(self.server_connections) > 0:
            socket, address  = self.server_connections.pop(0)
            socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            socket.settimeout(ChadtComponent.SOCKET_TIMEOUT)

            username = ConnectionEstablisher.DEFAULT_USERNAME_BASE + str(self.temp_id_counter)
            self.temp_id_counter += 1

            self.add_new_client(username, socket)

    def add_new_client(self, username, socket):
        self.server_client_dict[username] = ChadtConnection(username, socket, self.server_processing_queue)

        temp_id_message = Message.construct_temp_username_assigned(username, Message.SERVER_NAME, username)
        self.server_client_dict[username].add_message_to_out_queue(temp_id_message)
        
        self.server_client_dict[username].start()
