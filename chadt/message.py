"""
fields for message format(in bytes):
version - 1
type - 1
sender - 16
length - 2
message - length
"""


from struct import pack, unpack

from chadt.message_type import MessageType


class Message:

    HEADER_LENGTH = 20
    SENDER_MAX_LENGTH = 16
    
    @staticmethod
    def bytes_to_message(byte_array):
        version, message_type, sender, length = unpack("BB" + str(Message.SENDER_MAX_LENGTH) + "sH", byte_array[:Message.HEADER_LENGTH])
        message = byte_array[Message.HEADER_LENGTH:].decode("utf-8")
        return Message(message, sender, MessageType(message_type), version)

    @staticmethod
    def get_header(byte_array):
        return unpack("BB" + str(Message.SENDER_MAX_LENGTH) + "sH", byte_array[:Message.HEADER_LENGTH])
    
    def __init__(self, message, sender, message_type = MessageType.TEXT, version = 0):
        self.message = message
        self.length = len(message)
        self.sender = self.format_sender(sender)
        self.version = version
        self.message_type = message_type

    def make_bytes(self):
        pack_string = "BB" + str(Message.SENDER_MAX_LENGTH) + "sH" + str(self.length) + "s"
        data = pack(pack_string, self.version, int(self.message_type), bytes(self.sender, "utf-8"), self.length, bytes(self.message, "utf-8"))
        return data

    def format_sender(self, value):
        if len(value) > Message.SENDER_MAX_LENGTH:
            raise RuntimeError("Tried to set sender name greater than max length(" + str(Message.SENDER_MAX_LENGTH) + ")")
        else:
            return value.ljust(Message.SENDER_MAX_LENGTH)
