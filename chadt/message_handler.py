from warnings import warn


class MessageHandler:
    
    def __init__(self):
        pass

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

    def handle_error(self, message):
        self.raise_unhandled_warning()
