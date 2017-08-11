from socket import socket, SO_REUSEADDR, SOL_SOCKET, timeout
from threading import Thread
from time import sleep

from chadt.connection_status import ConnectionStatus
from chadt.message import Messsage


class ClientConnection:

    def __init__(self, username, server_message_queue):
        self.username = username

        self.server_message_queue = server_message_queue
        self.client_message_queue = []

        self.receiver = None
        self.receiver_status = ConnectionStatus.STOPPED
        self.transmitter = None
        self.transmitter_status = ConnectionStatus.STOPPED
        
    def add_socket(self, socket):
        socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        if self.receiver is None:
            self.receiver = socket
        elif self.transmitter is None:
            socket.settimeout(2)
            self.transmitter = socket
        else:
            raise RuntimeError("Excess socket connections associated with client.")

    def is_complete(self):
        return self.receiver is not None and self.transmitter is not None

    def start_transceiving(self):
        if (self.receiving_status == ConnectionStatus.STOPPED and
            self.transmitter_status == ConnectionStatus.STOPPED):

            self.receiving_status = ConnectionStatus.RUNNING
            Thread(target = receive_messages).start()

            self.transmitter_status = ConnectionStatus.RUNNING
            Thread(target = transmit_messages).start()
        elif (self.receiving_status == ConnectionStatus.STOPPING or
                self.transmitter_status == ConnectionStatus.STOPPING):
            raise RuntimeError("Receiver or Transmitter is still stopping, cannot restart yet.")
            
    def stop_transceiving(self):
        if self.receiving_status == ConnectionStatus.RUNNING:
            self.receiving_status = ConnectionStatus.STOPPING
        if self.transmitter_status == ConnectionStatus.RUNNING:
            self.transmitter_status = ConnectionStatus.STOPPING

    def shutdown(self):
        if (self.receiving_status == ConnectionStatus.RUNNING or
            self.transmitter_status == ConnectionStatus.RUNNING):
            self.stop_transceiving()
        self.receiver.close()
        self.transmitter.close()
            
    def receive_messages(self):
        while self.transmitter_status == ConnectionStatus.RUNNING:
            try:
                message = self.transmitter.recv(Message.HEADER_LENGTH)
                if self.sender_matches_username(message):
                    self.forward_message(message)
                else:
                    raise RuntimeError("Sender does not match username.")
            except timeout:
                pass
        self.transmitter_status = ConnectionStatus.STOPPED

    def sender_matches_username(self, message):
        sender = Message.get_header(message)[2].decode()
        return sender == self.username

    def forward_message(self, message):
        self.server_message_queue.append(message)

    def transmit_messages(self):
        while self.receiver_status == ConnectionStatus.RUNNING:
            if len(self.client_message_queue) > 0:
                message = self.client_message_queue.pop(0)
                self.receiver.sendall(message)
            else:
                sleep(1)
        self.receiver_status = ConnectionStatus.STOPPED

    def add_message_to_client_queue(self, message):
        self.client_message_queue.append(message)

