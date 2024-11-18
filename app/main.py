from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1 import images
from app.exception.common import exceptions as common_exceptions
from app.exception.image import exceptions as image_exceptions
from app.util.init_db import create_tables

@asynccontextmanager
async def lifecycle(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifecycle)

# Include routers
app.include_router(images.router, prefix='/api/v1/images', tags=['Images'])

# Include exception handlers
[app.add_exception_handler(exception, handler) for exception, handler in common_exceptions + image_exceptions]
