from chadt.chadt_component import ChadtComponent


class MessageRelayer(ChadtComponent):
    
    def __init__(self, server_message_queue, server_client_dict):
        self.server_message_queue = server_message_queue
        self.server_client_dict = server_client_dict

        super().__init__()

    def start(self):
        super().start(relay_messages)

    def relay_messages(self):
        if len(self.server_message_queue) > 0:
            message = self.server_message_queue.pop(0)
            self.add_message_to_client_queues(message)

    def add_message_to_client_queues(self, message):
        for key, value in self.server_client_dict.items():
            value.add_message_to_client_queue(message)
