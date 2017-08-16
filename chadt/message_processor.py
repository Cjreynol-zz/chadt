from struct import unpack

from chadt.chadt_exceptions import ZeroLengthMessageException
from chadt.message import Message
from chadt.message_type import MessageType


class MessageProcessor:

    @staticmethod
    def receive_message(socket):
        bytes_message = MessageProcessor.receive_message_bytes(socket)
        return MessageProcessor.bytes_to_message(bytes_message)

    @staticmethod
    def receive_message_bytes(socket):
        bytes_header = socket.recv(Message.HEADER_LENGTH)
        if len(bytes_header) == 0:
            raise ZeroLengthMessageException("Expecting normal length message.")
        _, _, _, length = MessageProcessor.decode_header(bytes_header)
        bytes_message_text = socket.recv(length)
        return bytes_header + bytes_message_text
    
    @staticmethod
    def bytes_to_message(byte_array):
        version, message_type, sender, length = MessageProcessor.decode_header(byte_array)
        message_text = byte_array[Message.HEADER_LENGTH:].decode()
        return Message(message_text, sender, message_type, version)

    @staticmethod
    def decode_header(byte_array):
        version, message_type, sender, length = unpack("BB" + str(Message.SENDER_MAX_LENGTH) + "sH", byte_array[:Message.HEADER_LENGTH])
        return (version, MessageType(message_type), sender.decode(), length)
    
    def __init__(self):
        pass
