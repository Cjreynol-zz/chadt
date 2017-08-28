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
from chadt.constants import ALL_NAME, RECIPIENT_MAX_LENGTH, SENDER_MAX_LENGTH, SERVER_NAME
from chadt.message_type import MessageType


class Message:

    HEADER_LENGTH = 1 + 1 + 16 + 16 + 2

    def __init__(self, text, sender, recipient = ALL_NAME, message_type = MessageType.TEXT, version = 0):
        self.text = text
        self.length = len(text)
        self.sender = sender
        self.recipient = recipient
        self.version = version
        self.message_type = MessageType(message_type)

    @property
    def recipient(self):
        return self._recipient

    @recipient.setter
    def recipient(self, value):
        if len(value) > RECIPIENT_MAX_LENGTH:
            raise UsernameTooLongException()
        else:
            self._recipient = value

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, value):
        if len(value) > SENDER_MAX_LENGTH:
            raise UsernameTooLongException()
        else:
            self._sender = value

    def get_display_string(self):
        value = ""
        if self.message_type == MessageType.TEXT:
            value = self._text_to_str()
        elif self.message_type == MessageType.USER_CONNECT:
            value = self._user_connect_to_str()
        elif self.message_type == MessageType.USER_NAME_CHANGE:
            value = self._user_name_change_to_str()
        elif self.message_type == MessageType.USER_DISCONNECT:
            value = self._user_disconnect_to_str()
        elif self.message_type == MessageType.LIST_OF_USERS:
            value = self._list_of_users_to_str()
        else:
            value = self.__str__()
        return value

    def _list_of_users_to_str(self):
        user_list = self.text.replace(",", ", ")
        return "Now connected to:  " + user_list
    
    def _text_to_str(self):
        to = ""
        if self.recipient != ALL_NAME:
            to = "(to {})".format(self.recipient)
        return self.sender + to + ":  " + self.text

    def _user_connect_to_str(self):
        username = self.text
        return username + " connected"
    
    def _user_disconnect_to_str(self):
        username = self.text
        return username + " disconnected"

    def _user_name_change_to_str(self):
        old, new = self.text.split(',')
        return old + " changed username to " + new

    def __str__(self):
        return self.sender + ":" + str(self.message_type)
        

# dynamically add static constructor functions to Message based on MessageType
def add_message_func(m_type):
    def f(text, sender, recipient = ALL_NAME):
        return Message(text, sender, recipient, m_type)
    func_name = "construct_" + str(m_type).lower()
    setattr(Message, func_name, f)

for m_type in MessageType:
    add_message_func(m_type)
