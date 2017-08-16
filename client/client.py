import logging as log
from socket import socket, SO_REUSEADDR, SOL_SOCKET, timeout

from chadt.chadt_connection import ChadtConnection
from chadt.message import Message
from chadt.message_processor import MessageProcessor
from chadt.message_type import MessageType

from lib.observed_list import ObservedList


class Client:

    SOCKET_TIMEOUT = 0.5

    def __init__(self, username, server_host, server_port):
        self.username = username

        self.message_in_queue = ObservedList()
        self.message_out_queue = []

        socket = self.initialize_connection(self.username, server_host, server_port)
        self.server_connection = ChadtConnection(self.username, socket, self.message_in_queue, self.message_out_queue, True)

        log.info("Client created.")

    def start_client(self): 
        self.server_connection.start()
        log.info("Client started.")

    def stop_client(self):
        self.server_connection.stop()
        log.info("Client stopped.")

    def shutdown_client(self):
        self.server_connection.shutdown()
        log.info("Client shut down.")

    def add_message_to_out_queue(self, message):
        self.message_out_queue.append(Message(message, self.username).make_bytes())

    def add_message_in_queue_observer(self, observer):
        self.message_in_queue.add_observer(observer)

    def initialize_connection(self, username, server_host, server_port):
        socket = self.create_socket()
        self.connect_socket(socket, server_host, server_port)
        self.request_username(socket, username)
        return socket

    def create_socket(self):
        s = socket()
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        return s

    def connect_socket(self, socket, server_host, server_port):
        socket.connect((server_host, server_port))

    def request_username(self, socket, username):
        username_request = Message("", username, MessageType.USERNAME_REQUEST)
        socket.sendall(username_request.make_bytes())

        message = MessageProcessor.receive_message(socket)

        if message.message_type == MessageType.USERNAME_REJECTED:
            raise RuntimeError("Username rejected, try again.")
        elif message.message_type == MessageType.USERNAME_ACCEPTED:
            pass
        else:
            raise RuntimeError("Unexpected message type.")
        socket.settimeout(Client.SOCKET_TIMEOUT)
