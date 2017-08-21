"""
fields for message format(in bytes):
version - 1
type - 1
sender - 16
recipient - 16
length - 2
message - length
"""


from chadt.chadt_exceptions import UsernameTooLongException
from chadt.message_type import MessageType


class Message:

    HEADER_LENGTH = 1 + 1 + 16 + 16 + 2
    SENDER_MAX_LENGTH = 16
    RECIPIENT_MAX_LENGTH = SENDER_MAX_LENGTH

    SERVER_NAME = "SERVER_NAME_____"
    ALL_NAME = "TARGET_ALL_USERS"
     
    def __init__(self, message_text, sender, recipient = ALL_NAME, message_type = MessageType.TEXT, version = 0):
        self.message_text = message_text
        self.length = len(message_text)
        self.sender = sender
        self.recipient = recipient
        self.version = version
        self.message_type = message_type

    def display_string(self):
        to = ""
        if self.recipient != Message.ALL_NAME:
            to = "(to {})".format(self.recipient)
        return self.sender + ":  " + self.message_text

    def __str__(self):
        return self.sender + ":" + str(self.message_type)

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, value):
        if len(value) > Message.SENDER_MAX_LENGTH:
            raise UsernameTooLongException()
        else:
            self._sender = value

    @property
    def recipient(self):
        return self._recipient

    @recipient.setter
    def recipient(self, value):
        if len(value) > Message.RECIPIENT_MAX_LENGTH:
            raise UsernameTooLongException()
        else:
            self._recipient = value
        

# dynamically add static constructor functions to Message based on MessageType
def add_message_func(m_type):
    def f(message_text, sender, recipient = Message.ALL_NAME):
        return Message(message_text, sender, recipient, m_type)
    func_name = "construct_" + str(m_type).lower()
    setattr(Message, func_name, f)

for m_type in MessageType:
    add_message_func(m_type)
