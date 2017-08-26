from warnings import warn

from chadt.system_message_processor import SystemMessageProcessor
from chadt.system_message_type import SystemMessageType


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

    def raise_unhandled_warning(self, message):
        warn("Unhandled message type {}.".format(message.message_type))


def add_method(m_type):
    method_name = "handle_" + str(m_type).lower()
    def f(cls, message):
        SystemMessageHandler.raise_unhandled_warning(message)
        
    setattr(SystemMessageHandler, method_name, classmethod(f))

for m_type in SystemMessageType:
    add_method(m_type)
