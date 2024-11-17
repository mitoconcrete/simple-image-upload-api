from enum import Enum

from app.util.contants import MAX_ALLOWED_IMAGE_COUNT, MAXIMUM_IMAGE_SIZE


class ErrorType(tuple, Enum):
    INVALID_IMAGE_TYPE = (40001, 'The image type should be jpg or png')
    INVALID_IMAGE_SIZE = (40002, f'The image size should be less than {MAXIMUM_IMAGE_SIZE} bytes')
    OUT_OF_ALLOWED_MAXIMUM_COUNT = (40004, f'The number of images should be less than {MAX_ALLOWED_IMAGE_COUNT}')
    OUT_OF_ALLOWED_MINIMUM_COUNT = (40005, 'At least one image is required')
    CONTENTS_NOT_FOUND = (40401, 'The contents not found')
