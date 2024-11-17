from fastapi.responses import JSONResponse

from app.schema.enum.exception import ErrorType


class ImageServiceException(Exception):
    pass


class PreProcessImageException(ImageServiceException):
    pass


class ProcessImageException(ImageServiceException):
    pass


class UploadException(ImageServiceException):
    pass


class SaveException(ImageServiceException):
    pass


class ImageServiceCustomException(ImageServiceException):
    def __init__(self, error_code: ErrorType):
        _error_code, _message = error_code
        self.error_code = _error_code
        self.message = _message


class NotSupportedTypeException(ImageServiceCustomException):
    pass


class OutOfAllowedSizeException(ImageServiceCustomException):
    pass


class OutOfAllowedCountException(ImageServiceCustomException):
    pass


class ContentsNotFoundException(ImageServiceCustomException):
    pass


# response for controller
async def not_supperted_type_exception_handler(request, exc: NotSupportedTypeException):
    return JSONResponse(
        status_code=400,
        content={'message': exc.message, 'error_code': exc.error_code},
    )


async def out_of_allowed_size_exception_handler(request, exc: OutOfAllowedSizeException):
    return JSONResponse(
        status_code=400,
        content={'message': exc.message, 'error_code': exc.error_code},
    )


async def out_of_allowed_count_exception_handler(request, exc: OutOfAllowedCountException):
    return JSONResponse(
        status_code=400,
        content={'message': exc.message, 'error_code': exc.error_code},
    )


async def contents_not_found_exception_handler(request, exc: ContentsNotFoundException):
    return JSONResponse(
        status_code=404,
        content={'message': exc.message, 'error_code': exc.error_code},
    )


exceptions = [
    (NotSupportedTypeException, not_supperted_type_exception_handler),
    (OutOfAllowedSizeException, out_of_allowed_size_exception_handler),
    (OutOfAllowedCountException, out_of_allowed_count_exception_handler),
    (ContentsNotFoundException, contents_not_found_exception_handler),
]
