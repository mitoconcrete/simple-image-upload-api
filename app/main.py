from fastapi import FastAPI

from app.api.v1 import images
from app.exception.common import exceptions as common_exceptions
from app.exception.image import exceptions as image_exceptions
from app.util.init_db import create_tables

app = FastAPI()

# Include routers
app.include_router(images.router, prefix='/api/v1/images', tags=['Images'])

# create_tables
create_tables()

# Include exception handlers
[app.add_exception_handler(exception, handler) for exception, handler in common_exceptions + image_exceptions]
