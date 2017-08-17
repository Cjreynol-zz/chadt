from enum import Enum


class MessageType(Enum):
    TEXT = 1

    DISCONNECT = 11

    USERNAME_REQUEST = 20
    USERNAME_ACCEPTED = 21
    USERNAME_REJECTED = 22
    TEMP_USERNAME_ASSIGNED = 23
    
    ERROR = 90

    def __int__(self):
        return self.value

    def __str__(self):
        return self.name
