from socket import timeout

from chadt.component import Component
from chadt.chadt_exceptions import ZeroLengthMessageException


class ConnectionHandler(Component):

    def __init__(self, username, connection, processing_queue, out_queue = None, is_server_connection = False):
        self.username = username
        self.transceiver = connection
        self.processing_queue = processing_queue
        self.is_server_connection = is_server_connection

        # None signifies that the out_queue is local to the connection
        if out_queue is not None:
            self.out_queue = out_queue
        else:
            self.out_queue = []

        super().__init__()

    def start(self):
        self.transceiver.start()
        super().start(self.transceive)

    def shutdown(self, disconnect_message = None):
        if disconnect_message is not None:
            self.transceiver.transmit_message(disconnect_message)
        self.transceiver.shutdown()
        super().shutdown()

    def transceive(self):
        self.receive_messages()
        self.transmit_messages()

    def transmit_messages(self):
        if len(self.out_queue) > 0:
            message = self.out_queue.pop(0)
            self.transceiver.transmit_message(message)

    def receive_messages(self):
        try:
            message = self.transceiver.receive_message()
            # represents the server checking that usernames match senders
            if not self.is_server_connection or message.sender == self.username:
                self.add_message_to_processing_queue(message)
        except (timeout, ZeroLengthMessageException, OSError):
            pass

    def add_message_to_processing_queue(self, message):
        self.processing_queue.append(message)

    def add_message_to_out_queue(self, message):
        self.out_queue.append(message)
