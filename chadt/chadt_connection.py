from socket import timeout

from chadt.chadt_component import ChadtComponent
from chadt.chadt_exceptions import ZeroLengthMessageException
from chadt.message import Message
from chadt.message_processor import MessageProcessor

class ChadtConnection(ChadtComponent):

    def __init__(self, username, socket, processing_queue, out_queue = None):
        # username means something different depending on whether client or 
        # server is holding the connection
        self.username = username
        self.transceiver = socket

        self.processing_queue = processing_queue
        # None signifies that the out_queue is local to the connection
        if out_queue is not None:
            self.out_queue = out_queue
        else:
            self.out_queue = []

        super().__init__()

    def start(self):
        super().start(self.transceive)

    def shutdown(self):
        disconnect_message = Message.construct_disconnect("", self.username, Message.SERVER_NAME)
        self.transmit_message(disconnect_message)
        super().shutdown(self.transceiver)

    def transceive(self):
        self.receive_messages()
        self.transmit_messages()

    def transmit_messages(self):
        if len(self.out_queue) > 0:
            message = self.out_queue.pop(0)
            self.transmit_message(message)

    def transmit_message(self, message):
        bytes_message = MessageProcessor.make_bytes(message)
        self.transceiver.sendall(bytes_message)

    def receive_messages(self):
        try:
            bytes_message = MessageProcessor.receive_message_bytes(self.transceiver)
            self.add_message_to_processing_queue(bytes_message)
        except (timeout, ZeroLengthMessageException):
            pass

    def add_message_to_processing_queue(self, message):
        self.processing_queue.append(message)

    def add_message_to_out_queue(self, message):
        self.out_queue.append(message)
