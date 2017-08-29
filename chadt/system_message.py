from chadt.system_message_type import SystemMessageType


class SystemMessage:
    """Represents the information client/server send to their controllers.

    """
    
    def __init__(self, text, message_type = SystemMessageType.TEXT):
        self.text = text
        self.message_type = message_type


def add_message_func(m_type):
    """Adds static constructor to SystemMessage based on m_type passed."""
    def f(text):
        return SystemMessage(text, m_type)
    func_name = "construct_" + str(m_type).lower()
    setattr(SystemMessage, func_name, f)

# Run on import
for m_type in SystemMessageType:
    add_message_func(m_type)
