from fastapi import FastAPI

from app.api.v1 import images
from app.exception.image import (
    ImageServiceException,
    NotSupportedTypeException,
    OutOfAllowedCountException,
    OutOfAllowedSizeException,
    not_supperted_type_exception_handler,
    out_of_allowed_count_exception_handler,
    out_of_allowed_size_exception_handler,
    unknown_exception_handler,
)

app = FastAPI()

# Include routers
app.include_router(images.router, prefix='/api/v1/images', tags=['Images'])

# Include exception handlers
app.add_exception_handler(NotSupportedTypeException, not_supperted_type_exception_handler)
app.add_exception_handler(OutOfAllowedSizeException, out_of_allowed_size_exception_handler)
app.add_exception_handler(OutOfAllowedCountException, out_of_allowed_count_exception_handler)
app.add_exception_handler(ImageServiceException, unknown_exception_handler)
