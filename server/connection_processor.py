from socket import SO_REUSEADDR, SOL_SOCKET, timeout

from chadt.chadt_component import ChadtComponent
from chadt.chadt_connection import ChadtConnection
from chadt.message import Message
from chadt.message_type import MessageType


class ConnectionProcessor(ChadtComponent):

    DEFAULT_USERNAME_BASE = "User"
    
    def __init__(self, new_connection_list, server_client_dict, server_processing_queue):
        self.temp_id_counter = 0

        self.new_connection_list = new_connection_list
        self.server_client_dict = server_client_dict
        self.server_processing_queue = server_processing_queue
        
        super().__init__()

    def start(self):
        super().start(self.process_connections)

    def process_connections(self):
        if len(self.new_connection_list) > 0:
            socket, address  = self.new_connection_list.pop(0)
            socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            socket.settimeout(2)

            username = ConnectionProcessor.DEFAULT_USERNAME_BASE + str(self.temp_id_counter)
            self.temp_id_counter += 1

            self.add_new_client(username, socket)

    def add_new_client(self, username, socket):
        self.server_client_dict[username] = ChadtConnection(username, socket, self.server_processing_queue)

        temp_id_message = Message(username, "server", MessageType.TEMP_USERNAME_ASSIGNED)
        self.server_client_dict[username].add_message_to_out_queue(temp_id_message)
        
        self.server_client_dict[username].start()
