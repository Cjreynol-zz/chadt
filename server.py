from threading import Thread
from socket import socket
from time import sleep
import logging as log

from observed_key_list_dict import ObservedKeyListDict


class Server(object):
    
    def __init__(self, port = 50000):
        self.port = port
        self.clients = ObservedKeyListDict()
        self.listener = self.create_listen_socket(("localhost", self.port))

        self.running = False
        self.receiver_thread = self.create_thread(self.listen)
        self.relay_thread = self.create_thread(self.relay_messages)
        log.info("Server created with port {}.".format(self.port))

    def start_server(self):
        self.running = True
        self.receiver_thread.start()
        self.relay_thread.start()

        log.info("Server started.")

    def stop_server(self):
        self.running = False
        self.listener.close()

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
                        #log.debug("No message from {}.".format(identifier))
            sleep(1)

    def relay_message(self, message, sender):
        for identifier, client in self.clients.items():
            sender_username = sender[0]
            labelled_message = bytes(sender_username + ":  ", "utf-8") + message
            client.send_message_to(labelled_message)
            log.info("Message sent.")
            log.debug("Sent message to {}.".format(identifier))

    def listen(self):
        log.info("Connection listening started.")
        while self.running:
            connection = self.listener.accept()
            log.info("New Connection.")
            self.process_connection(connection)

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

    def create_listen_socket(self, address):
        s = socket()
        s.bind(address)
        s.listen()
        return s
    
    def create_thread(self, target_func):
        return Thread(target = target_func)
    

class ClientConnection(object):

    MESSAGE_BUFFER_SIZE = 4096

    def __init__(self, username, address, receiver_socket, transmitter_socket=None):
        self.username = username
        self.address = address
        self.client_receiver = receiver_socket
        self.client_transmitter = transmitter_socket
        self.complete = False

    def get_message_from(self):
        return self.client_transmitter.recv(ClientConnection.MESSAGE_BUFFER_SIZE)

    def send_message_to(self, message):
        self.client_receiver.sendall(message)

