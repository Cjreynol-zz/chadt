import logging as log

from client.server_connection import ServerConnection

from lib.observed_list import ObservedList


class Client:

    def __init__(self, username, server_host, server_port):
        self.username = username

        self.message_in_queue = ObservedList()
        self.message_out_queue = []

        self.server_connection = ServerConnection(self.username, server_host, server_port, self.message_in_queue, self.message_out_queue)

        log.info("Client created.")

    def start_client(self): 
        self.server_connection.start()
        log.info("Client started.")

    def stop_client(self):
        self.server_connection.stop()
        log.info("Client stopped.")

    def shutdown_client(self):
        self.server_connection.shutdown()
        log.info("Client shutdown.")

    def add_message_to_out_queue(self, message):
        self.message_out_queue.append(message)

    def add_message_in_queue_observer(self, observer):
        self.message_in_queue.add_observer(observer)
