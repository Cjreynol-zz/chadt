from warnings import warn

from chadt.constants import SENDER_MAX_LENGTH
from chadt.message_processor import MessageProcessor
from chadt.message_type import MessageType


class MessageHandler:
    
    def __init__(self):
        self.message_processing_queue = []
        self.message_processor = MessageProcessor(self.message_processing_queue, self)

    def start(self):
        self.message_processor.start()

    def stop(self):
        self.message_processor.stop()

    def shutdown(self):
        self.message_processor.shutdown()

    def is_username_valid_length(self, username):
        return len(username) <= SENDER_MAX_LENGTH

    @staticmethod
    def raise_unhandled_warning():
        warn("Unhandled message type.")


def add_method(m_type):
    method_name = "handle_" + str(m_type).lower()
    def f(cls, message):
        MessageHandler.raise_unhandled_warning()
        
    setattr(MessageHandler, method_name, classmethod(f))

for m_type in MessageType:
    add_method(m_type)
