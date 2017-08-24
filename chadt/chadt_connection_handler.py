from socket import timeout

from chadt.chadt_connection import ChadtConnection
from chadt.constants import SERVER_NAME
from chadt.chadt_component import ChadtComponent
from chadt.chadt_exceptions import ZeroLengthMessageException
from chadt.message import Message


class ChadtConnectionHandler(ChadtComponent):

    def __init__(self, username, connection, processing_queue, out_queue = None):
        self.username = username
        self.transceiver = connection
        self.processing_queue = processing_queue

        # None signifies that the out_queue is local to the connection
        if out_queue is not None:
            self.out_queue = out_queue
        else:
            self.out_queue = []

        super().__init__()

    def start(self):
        self.transceiver.start()
        super().start(self.transceive)

    def shutdown(self):
        # this is not always the case, if the connection is on the server-side
        disconnect_message = Message.construct_disconnect("", self.username, SERVER_NAME)
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
            self.add_message_to_processing_queue(message)
        except (timeout, ZeroLengthMessageException):
            pass

    def add_message_to_processing_queue(self, message):
        self.processing_queue.append(message)

    def add_message_to_out_queue(self, message):
        self.out_queue.append(message)
