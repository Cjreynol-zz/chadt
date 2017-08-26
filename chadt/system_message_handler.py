from warnings import warn

from chadt.system_message_processor import SystemMessageProcessor


class SystemMessageHandler:

    def __init__(self):
        self.system_message_queue = []
        self.processor = SystemMessageProcessor(self.system_message_queue, self)

    def start(self):
        self.processor.start()

    def stop(self):
        self.processor.stop()

    def shutdown(self):
        self.processor.shutdown()

    def raise_unhandled_warning(self):
        warn("Unhandled message type.")
    
    def handle_text(self, message):
        self.raise_unhandled_warning()

    def handle_user_list_update(self, message):
        self.raise_unhandled_warning()
        
    def handle_username_rejected(self, message):
        self.raise_unhandled_warning()
    
    def handle_shutdown(self, message):
        self.raise_unhandled_warning()
