from struct import pack, unpack

from chadt.chadt_component import ChadtComponent
from chadt.chadt_exceptions import ZeroLengthMessageException
from chadt.message_type import MessageType


class MessageProcessor(ChadtComponent):

    
    def __init__(self, message_processing_queue, message_handler):
        self.message_processing_queue = message_processing_queue
        self.message_handler = message_handler
        
        super().__init__()

    def start(self):
        super().start(self.process_messages)

    def process_messages(self):
        if len(self.message_processing_queue) > 0:
            message = self.message_processing_queue.pop(0)
            self.process_message(message)

    def process_message(self, message):
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
        elif message.message_type == MessageType.LIST_OF_USERS:
            self.message_handler.handle_list_of_users(message)
        elif message.message_type == MessageType.ERROR:
            self.message_handler.handle_error(message)
        else:
            raise RuntimeError("Unexpected message type of {}.".format(message.message_type))
