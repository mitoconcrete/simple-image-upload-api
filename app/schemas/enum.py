from enum import Enum


class ImageProcessingType(Enum):
    READY = 'ready'
    PROCESSING = "processing"
    COMPLETED = 'completed'
    FAILED = 'failed'
    