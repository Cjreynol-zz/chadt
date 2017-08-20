import logging as log

from chadt.message import Message
from chadt.message_handler import MessageHandler
from chadt.message_type import MessageType

from lib.observed_key_list_dict import ObservedKeyListDict
from lib.observed_list import ObservedList

from server.connection_processor import ConnectionProcessor
from server.listener import Listener
from server.message_relayer import MessageRelayer


class Server(MessageHandler):
    
    def __init__(self, port):
        super().__init__()

        self.clients = ObservedKeyListDict()
        self.new_connections = []
        self.message_out_queue = []
        self.message_in_queue = ObservedList()

        self.listener = Listener(self.new_connections, port)
        self.connection_processor = ConnectionProcessor(self.new_connections, self.clients, self.message_processing_queue)
        self.message_relayer = MessageRelayer(self.message_out_queue, self.clients)

        log.info("Server created listening at port {}.".format(port))

    def start_server(self):
        self.listener.start()
        self.connection_processor.start()
        self.message_relayer.start()
        super().start()
        log.info("Server started.")

    def stop_server(self):
        self.listener.stop()
        self.connection_processor.stop()
        self.message_relayer.stop()
        super().stop()
        log.info("Server stopped.")

    def shutdown_server(self):
        self.listener.shutdown()
        self.connection_processor.shutdown()
        self.message_relayer.shutdown()
        for client_connection in self.clients.values():
            client_connection.shutdown()
        super().shutdown()
        log.info("Server shut down.")
    
    def add_client_list_observer(self, observer):
        self.clients.add_observer(observer)

    def handle_text(self, message):
        self.message_in_queue.append(message)
        self.message_out_queue.append(message)

    def handle_disconnect(self, message):
        self.clients[message.sender].shutdown()
        del self.clients[message.sender]

    def handle_username_request(self, message):
        username = message.message_text
        message_type = MessageType.USERNAME_ACCEPTED
        recipient = username

        if username not in self.clients:
            self.clients[username] = self.clients.pop(message.sender)
            self.clients[username].username = username
        else:
            message_type = MessageType.USERNAME_REJECTED
            recipient = message.sender

        response_message = Message(username, "server", message_type)
        self.clients[recipient].add_message_to_out_queue(response_message)

    def add_message_in_queue_observer(self, observer):
        self.message_in_queue.add_observer(observer)
