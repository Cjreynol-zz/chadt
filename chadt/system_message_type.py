from enum import Enum


class SystemMessageType(Enum):
    TEXT = 1

    USER_LIST_UPDATE = 10
    USERNAME_REJECTED = 11

    SHUTDOWN = 20

    def __int__(self):
        return self.value
    
    def __str__(self):
        return self.name
