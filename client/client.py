import logging as log
from socket import socket, SO_REUSEADDR, SOL_SOCKET, timeout

from chadt.chadt_connection import ChadtConnection
from chadt.chadt_exceptions import UsernameCurrentlyUnstableException, UsernameTooLongException
from chadt.message import Message
from chadt.message_handler import MessageHandler

from lib.observed_list import ObservedList


class Client(MessageHandler):

    def __init__(self, server_host, server_port):
        super().__init__()

        self.username = ""
        self.username_stable = False

        self.message_in_queue = ObservedList()
        self.message_out_queue = []
        self.connected_users = ObservedList()

        socket = self.initialize_connection(server_host, server_port)
        self.server_connection = ChadtConnection(self.username, socket, self.message_processing_queue, self.message_out_queue)

        self.shutdown_observer = None
        self.username_rejected_observer = None

        log.info("Client created.")

    def start_client(self): 
        self.server_connection.start()
        super().start()
        log.info("Client started.")

    def stop_client(self):
        self.server_connection.stop()
        super().stop()
        log.info("Client stopped.")

    def shutdown_client(self):
        self.server_connection.shutdown()
        super().shutdown()
        log.info("Client shut down.")

    def add_message_to_out_queue(self, message_text, recipient, message_constructor = Message.construct_text):
        if self.username_stable:
            message = message_constructor(message_text, self.username, recipient)
            self.message_out_queue.append(message)
        else:
            raise UsernameCurrentlyUnstableException()

    def add_message_in_queue_observer(self, observer):
        self.message_in_queue.add_observer(observer)

    def add_connected_users_observer(self, observer):
        self.connected_users.add_observer(observer)

    def initialize_connection(self, server_host, server_port):
        socket = self.create_socket()
        self.connect_socket(socket, server_host, server_port)
        return socket

    def create_socket(self):
        s = socket()
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.settimeout(ChadtConnection.SOCKET_TIMEOUT)
        return s

    def connect_socket(self, socket, server_host, server_port):
        socket.connect((server_host, server_port))

    def handle_text(self, message):
        self.message_in_queue.append(message)

    def handle_disconnect(self, message):
        if self.shutdown_observer is not None:
            self.shutdown_observer()
        else:
            self.shutdown_client()

    def handle_username_accepted(self, message):
        username = message.message_text
        if self.is_username_valid_length(username):
            self.username = username
            self.server_connection.username = username
            self.username_stable = True
        else:
            raise UsernameTooLongException()

    def handle_username_rejected(self, message):
        self.username_stable = True
        if self.username_rejected_observer is not None:
            self.username_rejected_observer()

    def handle_temp_username_assigned(self, message):
        self.handle_username_accepted(message)

    def handle_list_of_users(self, message):
        self.connected_users.clear()
        for user in message.message_text.split(','):
            self.connected_users.append(user)

    def send_username_request(self, username):
        if self.is_username_valid_length(username):
            self.add_message_to_out_queue(username, Message.SERVER_NAME, Message.construct_username_request)
            self.username_stable = False
        else:
            raise UsernameTooLongException()

    def set_username_rejected_observer(self, observer):
        self.username_rejected_observer = observer

    def set_shutdown_observer(self, observer):
        self.shutdown_observer = observer
