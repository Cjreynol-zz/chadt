from socket import timeout

from chadt.chadt_component import ChadtComponent
from chadt.chadt_exceptions import ZeroLengthMessageException
from chadt.message_processor import MessageProcessor

class ChadtConnection(ChadtComponent):

    def __init__(self, username, socket, in_queue, out_queue = None, decode = False):
        self.username = username
        self.transceiver = socket

        self.in_queue = in_queue
        if out_queue is not None:
            self.out_queue = out_queue
        else:
            self.out_queue = []

        self.decode = decode

        super().__init__()

    def start(self):
        super().start(self.transceive)

    def shutdown(self):
        super().shutdown(self.transceiver)

    def transceive(self):
        self.receive_messages()
        self.transmit_messages()

    def transmit_messages(self):
        if len(self.out_queue) > 0:
            message = self.out_queue.pop(0)
            self.transceiver.sendall(message)

    def receive_messages(self):
        try:
            bytes_message = MessageProcessor.receive_message_bytes(self.transceiver)

            if not self.decode:
                self.add_message_to_in_queue(bytes_message)
            else:
                self.add_message_to_in_queue(MessageProcessor.bytes_to_message(bytes_message))

        except (timeout, ZeroLengthMessageException):
            pass

    def add_message_to_in_queue(self, message):
        self.in_queue.append(message)

    def add_message_to_out_queue(self, message):
        self.out_queue.append(message)
