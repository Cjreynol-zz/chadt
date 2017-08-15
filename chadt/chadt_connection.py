from socket import timeout

from chadt.chadt_component import ChadtComponent
from chadt.message import Message
from chadt.message_type import MessageType


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
            header = self.transceiver.recv(Message.HEADER_LENGTH)
            if len(header) > 0:
                message_length =  Message.get_header(header)[3]
                message_text = self.transceiver.recv(message_length)
                self.add_message_to_in_queue(header + message_text)
        except timeout:
            pass

    def add_message_to_in_queue(self, message):
        if self.decode:
            message = Message.bytes_to_message(message)
        self.in_queue.append(message)

    def add_message_to_out_queue(self, message):
        self.out_queue.append(message)
