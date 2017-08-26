from chadt.component import Component
from chadt.system_message_type import SystemMessageType


class SystemMessageProcessor(Component):

    def __init__(self, system_message_queue, system_message_handler):
        self.system_message_queue = system_message_queue
        self.system_message_handler = system_message_handler

        self.lookup = self._create_conditional()

        super().__init__()

    def _create_conditional(self):
        ifelse = dict()

        for m_type in SystemMessageType:
            function_name = self._get_func_name(m_type)
            ifelse[m_type] = getattr(self.system_message_handler, function_name)

        return ifelse
            
    def _get_func_name(self, m_type):
        return "handle_" + str(m_type).lower()

    def start(self):
        super().start(self.process_system_messages)

    def process_system_messages(self):
        if len(self.system_message_queue) > 0:
            message = self.system_message_queue.pop(0)
            self.process_system_message(message)

    def process_system_message(self, message):
        try:
            self.lookup[message.m_type](message)
        except KeyError:
            raise RuntimeError("Unexpected system message type of {}".format(message.m_type))
