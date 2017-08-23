from enum import Enum


class ConnectionStatus(Enum):
    UNINITIALIZED = 1
    CONNECTED = 2
    CLOSED = 3
