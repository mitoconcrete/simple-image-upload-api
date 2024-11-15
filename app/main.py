# FastAPI app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import images

app = FastAPI()

app.include_router(images.router, prefix='/api/v1/images', tags=['Images'])

# CORS
app.add_middleware(  # type: ignore
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
