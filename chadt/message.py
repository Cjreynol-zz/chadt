"""
fields for message format(in bytes):
version - 1
type - 1
sender - 16
length - 2
message - length
"""


from struct import pack

from chadt.chadt_exceptions import UsernameTooLongException
from chadt.message_type import MessageType


class Message:

    HEADER_LENGTH = 20
    SENDER_MAX_LENGTH = 16
    
    def __init__(self, message_text, sender, message_type = MessageType.TEXT, version = 0):
        self.message_text = message_text
        self.length = len(message_text)
        self.sender = self.format_sender(sender)
        self.version = version
        self.message_type = message_type

    def make_bytes(self):
        pack_string = "BB" + str(Message.SENDER_MAX_LENGTH) + "sH" + str(self.length) + "s"
        data = pack(pack_string, self.version, int(self.message_type), bytes(self.sender, "utf-8"), self.length, bytes(self.message_text, "utf-8"))
        return data

    def format_sender(self, value):
        if len(value) > Message.SENDER_MAX_LENGTH:
            raise UsernameTooLongException()
        else:
            return value.ljust(Message.SENDER_MAX_LENGTH)
