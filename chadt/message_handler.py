from warnings import warn

from chadt.message import Message
from chadt.message_processor import MessageProcessor


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
        return len(username) <= Message.SENDER_MAX_LENGTH

    def raise_unhandled_warning(self):
        warn("Unhandled message type.")

    def handle_text(self, message):
        self.raise_unhandled_warning()

    def handle_disconnect(self, message):
        self.raise_unhandled_warning()
        
    def handle_username_request(self, message):
        self.raise_unhandled_warning()
        
    def handle_username_accepted(self, message):
        self.raise_unhandled_warning()

    def handle_username_rejected(self, message):
        self.raise_unhandled_warning()

    def handle_temp_username_assigned(self, message):
        self.raise_unhandled_warning()

    def handle_list_of_users(self, message):
        self.raise_unhandled_warning()

    def handle_error(self, message):
        self.raise_unhandled_warning()
