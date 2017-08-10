from threading import Thread
from socket import socket
from time import sleep
import logging as log


class Client(object):

    def __init__(self, username, server_host, server_port, output_func):
        self.username = username
        self.server_host = server_host
        self.server_port = server_port

        self.message_queue = []
        self.message_output = output_func

        self.receiver = self.create_connection()
        log.info("Client receiver is connected.")
        self.transmitter = self.create_connection()
        log.info("Client transmitter is connected.")

        self.running = False
        log.info("Client created.")

    def start_client(self): 
        self.running = True
        Thread(target = self.receive).start()
        Thread(target = self.transmit).start()
        log.info("Client started.")

    def stop_client(self):
        self.running = False
        self.receiver.close()
        self.transmitter.close()

    def receive(self):
        while self.running:
            message = self.receiver.recv(4096)
            message = message.decode()
            log.debug("New message received from server: {}".format(message))
            self.message_output(message)
    
    def transmit(self):
        while self.running:
            if len(self.message_queue) > 0:
                self.transmitter.sendall(self.message_queue.pop(0))
                log.info("Message sent to server.")
            else:
                sleep(1)

    def create_connection(self):
        s = socket()
        s.connect((self.server_host, self.server_port))
        s.sendall(bytes(self.username, "utf-8"))
        return s

    def add_message_to_queue(self, message):
        self.message_queue.append(bytes(message, "utf-8"))
