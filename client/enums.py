from enum import Enum

class AggregatedStatus(Enum):
    INITIATED = "INITIATED"
    INACTIVATED = "INACTIVATED"
    IDLE = "IDLE"
    DELETED = "DELETED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ERROR = "ERROR"
    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)

class PipelineStatus(Enum):
    INITIATED = "INITIATED"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ERROR = "ERROR"
    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)