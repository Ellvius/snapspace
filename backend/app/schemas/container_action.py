from enum import Enum

class ContainerAction(str, Enum):
    PAUSE = "pause"
    UNPAUSE = "unpause"
    STOP = "stop"
    RESTART = "restart"