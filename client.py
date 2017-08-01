from threading import Thread
from socket import socket
from time import sleep
import logging as log


class Client(object):

    SERVER_ADDRESS = ("localhost", 36000)

    def __init__(self, username, host, receive_port, transmit_port):
        self.username = username
        self.host = host
        self.receive_port = receive_port
        self.transmit_port = transmit_port
        self.message_queue = []

        self.receiver = self.create_connection((host, receive_port))
        log.info("Client receiver is connected.")
        self.transmitter = self.create_connection((host, transmit_port))
        log.info("Client transmitter is connected.")

        self.running = False
        self.receiver_thread = self.create_thread(self.receive)
        self.transmitter_thread = self.create_thread(self.transmit)
        log.info("Client created with host({}), receive_port({}), transmit_port({})".format(self.host, self.receive_port, self.transmit_port))

    def start_client(self): 
        self.running = True
        self.receiver_thread.start()
        self.transmitter_thread.start()

        log.info("Client started.")
        while self.running:
            message = input(">>>")
            self.message_queue.append(bytes(message, "utf-8"))
            log.debug("New message added to queue: {}".format(message))

    def receive(self):
        while self.running:
            message = self.receiver.recv(4096)
            message = message.decode()
            log.debug("New message received from server: {}".format(message))
            print("\n" + message + "\n>>>")

    def transmit(self):
        while self.running:
            if len(self.message_queue) > 0:
                log.info("Message sent to server.")
                self.transmitter.sendall(self.message_queue.pop(0))
            else:
                sleep(1)

    def create_connection(self, address):
        s = socket()
        s.bind(address)
        s.connect(Client.SERVER_ADDRESS)
        s.sendall(bytes(self.username, "utf-8"))
        return s

    def create_thread(self, target_func):
        return Thread(target = target_func)

