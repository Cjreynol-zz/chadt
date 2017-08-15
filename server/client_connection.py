from socket import timeout

from chadt.chadt_component import ChadtComponent
from chadt.message import Message


class ClientConnection(ChadtComponent):

    def __init__(self, username, socket, server_message_queue):
        self.username = username
        self.transceiver = socket

        self.server_message_queue = server_message_queue
        self.client_message_queue = []
        
        super().__init__()

    def start(self):
        super().start(self.transceive)

    def shutdown(self):
        super().shutdown(self.transceiver)

    def transceive(self):
        self.receive_messages()
        self.transmit_messages()
            
    def receive_messages(self):
        try:
            header = self.transceiver.recv(Message.HEADER_LENGTH)
            if len(header) > 0:
                unpacked_header = Message.get_header(header)
                if self.sender_matches_username(unpacked_header):
                    message_length = unpacked_header[3]
                    message = self.transceiver.recv(message_length)
                    self.forward_message(header+message)
                else:
                    raise RuntimeError("Sender does not match username.")
        except timeout:
            pass

    def sender_matches_username(self, header):
        sender = header[2].decode()
        return sender == self.username

    def forward_message(self, message):
        self.server_message_queue.append(message)

    def transmit_messages(self):
        if len(self.client_message_queue) > 0:
            message = self.client_message_queue.pop(0)
            self.transceiver.sendall(message)

    def add_message_to_client_queue(self, message):
        self.client_message_queue.append(message)
