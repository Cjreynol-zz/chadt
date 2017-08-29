from chadt.chadt_exceptions import UsernameTooLongException
from chadt.constants import ALL_NAME, RECIPIENT_MAX_LENGTH, SENDER_MAX_LENGTH, SERVER_NAME
from chadt.message_type import MessageType


class Message:
    """Datatype for chat messages and the associated header fields.

    The Message class aids in the generation of the header data sent to the 
    server along with chat messages.  The fields for the transmitted format 
    of a chat message are (sizes in bytes):
        version - 1
        message_type - 1
        sender - 16
        recipient - 16
        length - 2
        text - length

    """

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
        """Manages the recipient field, ensuring the length is within bounds."""
        return self._recipient

    @recipient.setter
    def recipient(self, value):
        if len(value) > RECIPIENT_MAX_LENGTH:
            raise UsernameTooLongException()
        else:
            self._recipient = value

    @property
    def sender(self):
        """Manages the sender field, ensuring the length is within bounds."""
        return self._sender

    @sender.setter
    def sender(self, value):
        if len(value) > SENDER_MAX_LENGTH:
            raise UsernameTooLongException()
        else:
            self._sender = value

    def get_display_string(self):
        """Calls the appropriate to_str method based on message type."""
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
        """Converts list_of_users message into a display string."""
        user_list = self.text.replace(",", ", ")
        return "Now connected to:  " + user_list
    
    def _text_to_str(self):
        """Converts text message into a display string."""
        user_list = self.text.replace(",", ", ")
        to = ""
        if self.recipient != ALL_NAME:
            to = "(to {})".format(self.recipient)
        return self.sender + to + ":  " + self.text

    def _user_connect_to_str(self):
        """Converts user_connect message into a display string."""
        username = self.text
        return username + " connected"
    
    def _user_disconnect_to_str(self):
        """Converts user_disconnect message into a display string."""
        username = self.text
        return username + " disconnected"

    def _user_name_change_to_str(self):
        """Converts user_name_change message into a display string."""
        old, new = self.text.split(',')
        return old + " changed username to " + new

    def __str__(self):
        return self.sender + ":" + str(self.message_type)
        

def add_message_func(m_type):
    """Adds static constructor to Message based on m_type passed."""
    def f(text, sender, recipient = ALL_NAME):
        return Message(text, sender, recipient, m_type)
    func_name = "construct_" + str(m_type).lower()
    setattr(Message, func_name, f)

# Run on import
for m_type in MessageType:
    add_message_func(m_type)
