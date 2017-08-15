from enum import Enum


class ComponentStatus(Enum):
    RUNNING = 1
    STOPPED = 2
    STOPPING = 3
    SHUTTING_DOWN = 4
    SHUT_DOWN = 5
