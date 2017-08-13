from enum import Enum


class ComponentStatus(Enum):
    STOPPED = 1
    RUNNING = 2
    STOPPING = 3
    
