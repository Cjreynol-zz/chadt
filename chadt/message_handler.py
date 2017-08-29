from types import MethodType
from warnings import warn

from chadt.constants import SENDER_MAX_LENGTH
from chadt.message_processor import MessageProcessor


class MessageHandler:
    
    def __init__(self, type_enum):

        self.message_processing_queue = []

        for m_type in type_enum:
            self._add_method(m_type)

        self.message_processor = MessageProcessor(self.message_processing_queue, self, type_enum)

    def start(self):
        self.message_processor.start()

    def stop(self):
        self.message_processor.stop()

    def shutdown(self):
        self.message_processor.shutdown()

    def is_username_valid_length(self, username):
        return len(username) <= SENDER_MAX_LENGTH

    def raise_unhandled_warning(self, message):
        warn("Unhandled message type {}.".format(str(message)))

    def _add_method(self, m_type):
        method_name = "handle_" + str(m_type).lower()
        def f(self, message):
            self.raise_unhandled_warning(message)
            
        # these default methods are added in the init, which sub-classes call 
        # after their definitions are already in place.  This check keeps 
        # these from shadowing a sub-class' implementation
        if not hasattr(self, method_name):
            setattr(self, method_name, MethodType(f, self))
