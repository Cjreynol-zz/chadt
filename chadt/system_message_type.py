from enum import Enum


class SystemMessageType(Enum):
    """Represents different messages sent from client/server to controllers.

    Each grouping is a class of related messages that are used to provide 
    certain functionality to the clients or server.

    """

    TEXT = 1

    USER_LIST_UPDATE = 10
    USERNAME_REJECTED = 11

    SHUTDOWN = 20

    def __int__(self):
        return self.value
    
    def __str__(self):
        return self.name
