from enum import Enum


class ConnectionStatus(Enum):
    STOPPED = 1
    RUNNING = 2
    STOPPING = 3
    
