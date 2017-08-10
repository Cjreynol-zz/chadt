

class ClientConnection(object):

    MESSAGE_BUFFER_SIZE = 4096

    def __init__(self, username, address, receiver_socket, transmitter_socket=None):
        self.username = username
        self.address = address
        self.client_receiver = receiver_socket
        self.client_transmitter = transmitter_socket
        self.complete = False

    def get_message_from(self):
        return self.client_transmitter.recv(ClientConnection.MESSAGE_BUFFER_SIZE)

    def send_message_to(self, message):
        self.client_receiver.sendall(message)
