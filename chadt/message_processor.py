from struct import pack, unpack

from chadt.component import Component
from chadt.chadt_exceptions import ZeroLengthMessageException
from chadt.message_type import MessageType


class MessageProcessor(Component):
    
    def __init__(self, message_processing_queue, message_handler):
        self.message_processing_queue = message_processing_queue
        self.message_handler = message_handler

        self.lookup = self._create_conditional()
        
        super().__init__()

    def _create_conditional(self):
        ifelse = dict()

        for m_type in MessageType:
            function_name = self._get_func_name(m_type)
            ifelse[m_type] = getattr(self.message_handler, function_name)

        return ifelse
            
    def _get_func_name(self, m_type):
        return "handle_" + str(m_type).lower()

    def start(self):
        super().start(self.process_messages)

    def process_messages(self):
        if len(self.message_processing_queue) > 0:
            message = self.message_processing_queue.pop(0)
            self.process_message(message)

    def process_message(self, message):
        try:
            self.lookup[message.message_type](message)
        except KeyError:
            raise RuntimeError("Unexpected message type of {}.".format(message.message_type))
