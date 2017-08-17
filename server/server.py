import logging as log

from chadt.message_handler import MessageHandler
from chadt.message_processor import MessageProcessor

from lib.observed_key_list_dict import ObservedKeyListDict

from server.connection_processor import ConnectionProcessor
from server.listener import Listener
from server.message_relayer import MessageRelayer


class Server(MessageHandler):
    
    def __init__(self, port):
        self.clients = ObservedKeyListDict()
        self.new_connections = []
        self.server_message_queue = []
        self.message_processing_queue = []

        self.listener = Listener(self.new_connections, port)
        self.connection_processor = ConnectionProcessor(self.new_connections, self.clients, self.server_message_queue)

        self.message_relayer = MessageRelayer(self.server_message_queue, self.clients)
        self.message_processor = MessageProcessor(self.message_processing_queue, self)

        super().__init__()
        log.info("Server created listening at port {}.".format(port))

    def start_server(self):
        self.listener.start()
        self.connection_processor.start()
        self.message_relayer.start()
        log.info("Server started.")

    def stop_server(self):
        self.listener.stop()
        self.connection_processor.stop()
        self.message_relayer.stop()
        log.info("Server stopped.")

    def shutdown_server(self):
        self.listener.shutdown()
        self.connection_processor.shutdown()
        self.message_relayer.shutdown()
        for client in self.clients.values():
            client.shutdown()
        log.info("Server shut down.")
    
    def add_client_list_observer(self, observer):
        self.clients.add_observer(observer)
