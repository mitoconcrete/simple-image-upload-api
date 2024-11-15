class ImageUploaderError(Exception):
    def __init__(self, message):
        super().__init__(message)

class UploadServiceError(Exception):
    def __init__(self, message):
        super().__init__(message)

class UploadServiceValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)