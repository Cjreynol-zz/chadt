from enum import Enum


class MessageType(Enum):
    TEXT = 1

    FIRST_CONNECTION = 10
    SECOND_CONNECTION = 11
    DISCONNECT = 12

    USERNAME_SUBMISSION = 20
    USERNAME_ACCEPTED = 21
    USERNAME_TAKEN = 22
    
    ERROR = 90

    def __int__(self):
        return self.value
