from chadt.chadt_component import ChadtComponent
from chadt.message import Message
from chadt.message_type import MessageType

from server.client_connection import ClientConnection


class ConnectionProcessor(ChadtComponent):
    
    def __init__(self, new_connection_list, server_client_dict, server_message_queue):
        self.new_connection_list = new_connection_list
        self.server_client_dict = server_client_dict
        self.server_message_queue = server_message_queue
        
        super().__init__()

    def start(self):
        super().start(self.process_connections)

    def process_connections(self):
        if len(self.new_connection_list) > 0:
            new_connection = self.new_connection_list.pop(0)[0]
            username = self.negotiate_username(new_connection)
            self.add_new_client(username, new_connection)

    def negotiate_username(self, socket):
        header = socket.recv(Message.HEADER_LENGTH)
        version, message_type, sender, length = Message.get_header(header)
        string_sender = sender.decode()
        
        while (message_type == MessageType.USERNAME_REQUEST and 
                string_sender in self.server_client_dict):
            rejection = Message("", "server", MessageType.USERNAME_REJECTED)
            socket.sendall(rejection.makebytes())
            header = socket.recv(Message.HEADER_LENGTH)
            version, message_type, sender, length = Message.get_header(header)
            string_sender = sender.decode()

        acceptance = Message("", "server", MessageType.USERNAME_ACCEPTED)
        socket.sendall(acceptance.make_bytes())
        return string_sender

    def add_new_client(self, username, new_connection):
        self.server_client_dict[username] = ClientConnection(username, new_connection, self.server_message_queue)
        self.server_client_dict[username].start()
