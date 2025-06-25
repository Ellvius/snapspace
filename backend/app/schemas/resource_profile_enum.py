from enum import Enum

class ResourceProfile(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"