import logging as log

from chadt.constants import SERVER_NAME
from chadt.message import Message
from chadt.message_handler import MessageHandler

from lib.observed_key_list_dict import ObservedKeyListDict
from lib.observed_list import ObservedList

from server.connection_establisher import ConnectionEstablisher
from server.message_relayer import MessageRelayer


class Server(MessageHandler):
    
    def __init__(self, port):
        super().__init__()

        self.clients = ObservedKeyListDict()
        self.message_out_queue = []
        self.message_in_queue = ObservedList()

        self.connection_establisher = ConnectionEstablisher(port, self.clients, self.message_processing_queue)
        self.message_relayer = MessageRelayer(self.message_out_queue, self.clients)

        log.info("Server created listening at port {}.".format(port))

    def start_server(self):
        self.connection_establisher.start()
        self.message_relayer.start()
        super().start()

        self.add_client_list_observer(self.update_clients_user_list)
        log.info("Server started.")

    def stop_server(self):
        self.connection_establisher.stop()
        self.message_relayer.stop()
        super().stop()
        log.info("Server stopped.")

    def shutdown_server(self):
        self.connection_establisher.shutdown()
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
        message_constructor = Message.construct_username_accepted
        recipient = username

        if username not in self.clients and self.is_username_valid_length(username):
            self.clients[username] = self.clients.pop(message.sender)
            self.clients[username].username = username
            self.send_username_change(message.sender, username)
        else:
            message_constructor = Message.construct_username_rejected
            recipient = message.sender

        response_message = message_constructor(username, SERVER_NAME, recipient)
        self.clients[recipient].add_message_to_out_queue(response_message)

    def add_message_in_queue_observer(self, observer):
        self.message_in_queue.add_observer(observer)

    def update_clients_user_list(self):
        user_list_string = ','.join(self.clients.keys())
        user_list_message = Message.construct_list_of_users(user_list_string, SERVER_NAME)
        self.message_out_queue.append(user_list_message)

    def send_username_change(self, old_username, new_username):
        message_text = old_username + " changed username to " + new_username
        username_change_message = Message.construct_text(message_text, SERVER_NAME)
        self.message_in_queue.append(username_change_message)
        self.message_out_queue.append(username_change_message)
