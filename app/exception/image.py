from fastapi.responses import JSONResponse

from app.util.contants import MAX_ALLOWED_IMAGE_COUNT, MAXIMUM_IMAGE_SIZE


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


# response for controller
async def not_supperted_type_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={'message': 'The image type should be jpg or png'},
    )


async def out_of_allowed_size_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={'message': f'The image size should be less than {MAXIMUM_IMAGE_SIZE} bytes'},
    )


async def out_of_allowed_count_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={'message': f'The number of images should be less than {MAX_ALLOWED_IMAGE_COUNT}'},
    )


async def unknown_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={'message': 'Internal server error', 'detail': str(exc)},
    )
