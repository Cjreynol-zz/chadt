from chadt.message_handler import MessageHandler
from chadt.system_message_type import SystemMessageType


class ViewController(MessageHandler):

    MIN_PORT = 0
    MAX_PORT = 65535
    
    def __init__(self):
        super().__init__(SystemMessageType)
        self.view = None

    def is_valid_port_num(self, num):
        return_value = True
        try:
            num = int(num)
            if num < self.MIN_PORT or num > self.MAX_PORT:
                return_value = False
        except ValueError:
            return_value = False

        return return_value

    def quit(self):
        self.view.quit()
        self.shutdown()

    def handle_text(self, message):
        self.view.display_new_text_message(message.text)
