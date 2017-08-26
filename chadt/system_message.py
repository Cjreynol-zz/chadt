from chadt.system_message_type import SystemMessageType


class SystemMessage:
    
    def __init__(self, text, m_type = SystemMessageType.TEXT):
        self.text = text
        self.m_type = m_type


# dynamically add static constructor functions to SystemMessage based on 
# SystemMessageType
def add_message_func(m_type):
    def f(text):
        return SystemMessage(text, m_type)
    func_name = "construct_" + str(m_type).lower()
    setattr(SystemMessage, func_name, f)

for m_type in SystemMessageType:
    add_message_func(m_type)
