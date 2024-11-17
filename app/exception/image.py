class ImageServiceException(Exception):
    pass


class NotSupportedTypeException(ImageServiceException):
    pass


class OutOfAllowedSizeException(ImageServiceException):
    pass


class OutOfAllowedCountException(ImageServiceException):
    pass


class PreProcessImageException(ImageServiceException):
    pass


class ProcessImageException(ImageServiceException):
    pass


class UploadException(ImageServiceException):
    pass


class SaveException(ImageServiceException):
    pass
