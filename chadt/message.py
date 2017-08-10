"""
fields for message format(in bytes):
version - 1
type - 1
sender - 16
length - 2
message - length
"""


from enum import Enum
from struct import pack, unpack


class Message:
    
    @staticmethod
    def bytes_to_message(array):
        version, message_type, sender, length = unpack("BB16sH", array[:20])
        message = [20:].decode("utf-8")
        return Message(message, sender, version, message_type)
    
    def __init__(self, message, sender, version=0, message_type=MessageType.TEXT):
        self.message = message
        self.length = len(message)
        self.sender = self.format_sender(sender)
        self.version = version
        self.message_type = message_type

    def make_bytes(self):
        pack_string = "BB16sH" + str(self.length) + "s"
        data = pack(pack_string, self.version, self.message_type, self.sender, self.length, self.message)
        return data

    def format_sender(self, sender):
        if len(sender) > 16:
            raise RuntimeError("Sender name is too long")
        return sender.ljust(16)


class MessageType(Enum):
    TEXT = 1
    CONNECT = 2
    DISCONNECT = 3
