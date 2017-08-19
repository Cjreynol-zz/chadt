from struct import pack, unpack

from chadt.chadt_component import ChadtComponent
from chadt.chadt_exceptions import ZeroLengthMessageException
from chadt.message import Message
from chadt.message_type import MessageType


class MessageProcessor(ChadtComponent):

    @staticmethod
    def receive_message(socket):
        bytes_message = MessageProcessor.receive_message_bytes(socket)
        return MessageProcessor.bytes_to_message(bytes_message)

    @staticmethod
    def receive_message_bytes(socket):
        bytes_header = socket.recv(Message.HEADER_LENGTH)
        if len(bytes_header) == 0:
            raise ZeroLengthMessageException()
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
        return (version, MessageType(message_type), sender.decode().rstrip(), length)

    @staticmethod
    def make_bytes(message):
        pack_string = "BB" + str(Message.SENDER_MAX_LENGTH) + "sH" + str(message.length) + "s"
        data = pack(pack_string, message.version, int(message.message_type), bytes(message.sender.ljust(Message.SENDER_MAX_LENGTH), "utf-8"), message.length, bytes(message.message_text, "utf-8"))
        return data
    
    def __init__(self, message_processing_queue, message_handler):
        self.message_processing_queue = message_processing_queue
        self.message_handler = message_handler
        
        super().__init__()

    def start(self):
        super().start(self.process_messages)

    def process_messages(self):
        if len(self.message_processing_queue) > 0:
            bytes_message = self.message_processing_queue.pop(0)
            self.process_message(bytes_message)

    def process_message(self, bytes_message):
        message = MessageProcessor.bytes_to_message(bytes_message)

        if message.message_type == MessageType.TEXT:
            self.message_handler.handle_text(message)
        elif message.message_type == MessageType.DISCONNECT:
            self.message_handler.handle_disconnect(message)
        elif message.message_type == MessageType.USERNAME_REQUEST:
            self.message_handler.handle_username_request(message)
        elif message.message_type == MessageType.USERNAME_ACCEPTED:
            self.message_handler.handle_username_accepted(message)
        elif message.message_type == MessageType.USERNAME_REJECTED:
            self.message_handler.handle_username_rejected(message)
        elif message.message_type == MessageType.TEMP_USERNAME_ASSIGNED:
            self.message_handler.handle_temp_username_assigned(message)
        elif message.message_type == MessageType.ERROR:
            self.message_handler.handle_error(message)
        else:
            raise RuntimeError("Unexpected message type.")
