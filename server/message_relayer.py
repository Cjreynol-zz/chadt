from chadt.chadt_component import ChadtComponent
from chadt.message import Message


class MessageRelayer(ChadtComponent):
    
    def __init__(self, server_out_queue, server_client_dict):
        self.server_out_queue = server_out_queue
        self.server_client_dict = server_client_dict

        super().__init__()

    def start(self):
        super().start(self.relay_messages)

    def relay_messages(self):
        if len(self.server_out_queue) > 0:
            message = self.server_out_queue.pop(0)
            self.add_message_to_client_queues(message)

    def add_message_to_client_queues(self, message):
        for key, value in self.server_client_dict.items():
            if message.recipient == Message.ALL_NAME or key in [message.sender, message.recipient]:
                value.add_message_to_out_queue(message)
