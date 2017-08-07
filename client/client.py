from threading import Thread
from socket import socket
from time import sleep
import logging as log


class Client(object):

    CLIENT_HOST = "localhost"

    def __init__(self, username, server_host, server_port, console_input_mode = True):
        self.username = username
        self.console_input_mode = console_input_mode
        self.server_host = server_host
        self.server_port = server_port

        self.message_queue = []
        self.message_output = self.console_output

        self.receiver = self.create_connection()
        log.info("Client receiver is connected.")
        self.transmitter = self.create_connection()
        log.info("Client transmitter is connected.")

        self.running = False
        self.receiver_thread = self.create_thread(self.receive)
        self.transmitter_thread = self.create_thread(self.transmit)
        log.info("Client created.")

    def start_client(self): 
        self.running = True
        self.receiver_thread.start()
        self.transmitter_thread.start()

        log.info("Client started.")
        if self.console_input_mode:
            self.console_input()

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
    
    def console_output(self, message):
        print("\n" + message + "\n>>> ", end='')

    def console_input(self):
        while self.running:
            message = input(">>> ")
            self.message_queue.append(bytes(message, "utf-8"))
            log.debug("New message added to queue: {}".format(message))

    def transmit(self):
        while self.running:
            if len(self.message_queue) > 0:
                log.info("Message sent to server.")
                self.transmitter.sendall(self.message_queue.pop(0))
            else:
                sleep(1)

    def create_connection(self):
        s = socket()
        s.connect((self.server_host, self.server_port))
        s.sendall(bytes(self.username, "utf-8"))
        return s

    def create_thread(self, target_func):
        return Thread(target = target_func)

