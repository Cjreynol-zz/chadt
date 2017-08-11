import logging as log
from socket import socket
from threading import Thread
from time import sleep

from chadt.message import Message
from lib.observed_key_list_dict import ObservedKeyListDict
from server.client_connection import ClientConnection
from server.listener import Listener


class Server(object):
    
    def __init__(self, port = 50000):
        self.clients = ObservedKeyListDict()
        self.new_connections = []
        self.listener = Listener(self.new_connections, port)

        self.running = False
        log.info("Server created listening at port {}.".format(port))

    def start_server(self):
        self.running = True
        Thread(target = self.process_connections).start()
        Thread(target = self.relay_messages).start()
        self.listener.start_listening()
        log.info("Server started.")

    def stop_server(self):
        self.running = False
        self.listener.stop_listening()

    def relay_messages(self):
        log.info("Message relaying started.")
        while self.running:
            for identifier, client in self.clients.items():
                if client.complete:
                    try:
                        message = client.get_message_from()
                        if len(message) > 0:
                            log.info("Message received.")
                            log.debug("Received message from {}: {}".format(identifier, message))
                            self.relay_message(message, identifier)

                    except BlockingIOError:
                        pass
            sleep(1)

    def relay_message(self, message, sender):
        for identifier, client in self.clients.items():
            sender_username = sender[0]
            labelled_message = bytes(sender_username + ":  ", "utf-8") + message
            client.send_message_to(labelled_message)
            log.info("Message sent.")
            log.debug("Sent message to {}.".format(identifier))

    def process_connections(self):
        while self.running:
            if len(self.new_connections) > 0:
                self.process_connection(self.new_connections.pop(0))
            sleep(1)

    def process_connection(self, connection):
        new_socket = connection[0]
        address = connection[1]
        host, port = address

        username = new_socket.recv(ClientConnection.MESSAGE_BUFFER_SIZE).decode()
        identifier = (username, host)

        if identifier not in self.clients:
            self.add_client_connection(username, address, identifier, new_socket)
        else:
            self.update_client_connection(username, address, identifier, new_socket)

    def add_client_connection(self, username, address, identifier, socket):
        self.clients[identifier] = ClientConnection(username, address, socket)
        log.debug("Connection is new client {} at address {}.".format(username, address))

    def update_client_connection(self, username, address, identifier, socket):
        socket.setblocking(False)
        self.clients[identifier].client_transmitter = socket
        self.clients[identifier].complete = True
        log.debug("Connection is existing client {} at address {}.".format(username, address))
    
    def add_client_list_observer(self, observer):
        self.clients.add_observer(observer)
