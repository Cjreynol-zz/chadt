from chadt.component import Component
from chadt.system_message_type import SystemMessageType


class SystemMessageProcessor(Component):

    def __init__(self, system_message_queue, system_message_handler):
        self.system_message_queue = system_message_queue
        self.system_message_handler = system_message_handler

        super().__init__()

    def start(self):
        super().start(self.process_system_messages)

    def process_system_messages(self):
        if len(self.system_message_queue) > 0:
            message = self.system_message_queue.pop(0)
            self.process_system_message(message)

    def process_system_message(self, message):
        if message.m_type == SystemMessageType.TEXT:
            self.system_message_handler.handle_text(message)
        elif message.m_type == SystemMessageType.USER_LIST_UPDATE:
            self.system_message_handler.handle_user_list_update(message)
        elif message.m_type == SystemMessageType.USERNAME_REJECTED:
            self.system_message_handler.handle_username_rejected(message)
        elif message.m_type == SystemMessageType.SHUTDOWN:
            self.system_message_handler.handle_shutdown(message)
        else:
            raise RuntimeError("Unexpected system message type of {}".format(message.m_type))
