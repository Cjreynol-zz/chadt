"""
fields for message format(in bytes):
version - 1
type - 1
sender - 16
length - 2
message - length
"""


from chadt.chadt_exceptions import UsernameTooLongException
from chadt.message_type import MessageType


class Message:

    HEADER_LENGTH = 20
    SENDER_MAX_LENGTH = 16
    
    def __init__(self, message_text, sender, message_type = MessageType.TEXT, version = 0):
        self.message_text = message_text
        self.length = len(message_text)
        self.sender = sender
        self.version = version
        self.message_type = message_type

    def display_string(self):
        return self.sender + ":  " + self.message_text

    def __str__(self):
        return self.sender + ":" + str(self.message_type)

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, value):
        if len(value) > Message.SENDER_MAX_LENGTH:
            raise UsernameTooLongException()
        else:
            self._sender = value
