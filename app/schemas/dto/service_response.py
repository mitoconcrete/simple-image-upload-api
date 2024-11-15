import uuid
from datetime import datetime

from pydantic import BaseModel

from app.schemas.enum import ImageProcessingType


class ImageSimpleResponse(BaseModel):
    id: uuid.UUID
    original_url: str
    status: ImageProcessingType


class ImageDetailResponse(BaseModel):
    id: uuid.UUID
    original_url: str
    svg_url: str
    status: ImageProcessingType
    created_at: datetime


class UploadImage(BaseModel):
    id: uuid.UUID
    original_url: str
    image: bytes


class UploadServiceResponseDto(BaseModel):
    images: list[ImageSimpleResponse]


class UploadImageServiceResponseDto(BaseModel):
    id: uuid.UUID
    original_url: str
    image: bytes


class UploadSVGServiceResponseDto(BaseModel):
    id: uuid.UUID


class GetImageServiceResponseDto(BaseModel):
    id: uuid.UUID
    original_url: str
    svg_url: str
    status: ImageProcessingType
    created_at: datetime


class GetImageListServiceResponseDto(BaseModel):
    items: list[GetImageServiceResponseDto]
    total: int
    page: int
    limit: int
