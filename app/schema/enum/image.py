from enum import Enum


class ImageProcessingType(str, Enum):
    READY = 'ready'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
