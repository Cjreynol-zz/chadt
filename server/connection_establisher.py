from socket import timeout

from chadt.chadt_component import ChadtComponent
from chadt.chadt_connection import ChadtConnection
from chadt.chadt_connection_handler import ChadtConnectionHandler
from chadt.constants import DEFAULT_USERNAME_BASE, SERVER_NAME
from chadt.message import Message


class ConnectionEstablisher(ChadtComponent):

    def __init__(self, listening_port, server_client_dict, server_processing_queue):
        self.listener = ChadtConnection(listening_port)
        self.server_connections = []
        self.temp_id_counter = 0

        self.server_client_dict = server_client_dict
        self.server_processing_queue = server_processing_queue

        super().__init__()

    def start(self):
        self.listener.start()
        super().start(self.listen_and_process)

    def shutdown(self):
        self.listener.shutdown()
        super().shutdown()

    def listen_and_process(self):
        self.listen()
        self.process_connections()

    def listen(self):
        try:
            new_connection = self.listener.accept_connections()
            self.server_connections.append(new_connection)
        except timeout:
            pass

    def process_connections(self):
        if len(self.server_connections) > 0:
            new_socket, address  = self.server_connections.pop(0)
            connection = ChadtConnection(connected_socket = new_socket)

            username = DEFAULT_USERNAME_BASE + str(self.temp_id_counter)
            self.temp_id_counter += 1

            self.add_new_client(username, connection)

    def add_new_client(self, username, connection):
        self.server_client_dict[username] = ChadtConnectionHandler(username, connection, self.server_processing_queue)

        temp_id_message = Message.construct_temp_username_assigned(username, SERVER_NAME, username)
        self.server_client_dict[username].add_message_to_out_queue(temp_id_message)
        
        self.server_client_dict[username].start()
