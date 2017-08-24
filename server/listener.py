from socket import timeout

from chadt.chadt_component import ChadtComponent
from chadt.chadt_connection import ChadtConnection


class Listener(ChadtComponent):

    def __init__(self, listening_port, new_connections): 
        self.listening_connection = ChadtConnection(listening_port)
        self.new_connections = new_connections

        super().__init__()

    def start(self):
        self.listening_connection.start()
        super().start(self.listen)

    def shutdown(self):
        self.listening_connection.shutdown()
        super().shutdown()

    def listen(self):
        try:
            new_connection = self.listening_connection.accept_connections()
            self.process_connection(new_connection)
        except timeout:
            pass

    def process_connection(self, connection):
        new_socket, address  = connection
        connection = ChadtConnection(connected_socket = new_socket)
        self.new_connections.append(connection)
