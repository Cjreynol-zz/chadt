from socket import timeout

from chadt.component import Component
from chadt.connection import Connection


class Listener(Component):

    def __init__(self, listening_port, new_connections): 
        self.listening_connection = Connection(listening_port)
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
        connection = Connection(connected_socket = new_socket)
        self.new_connections.append(connection)
