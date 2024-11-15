from datetime import datetime

from pydantic import BaseModel

from .enum import ImageProcessingType


class ImageUploadServiceResponseDto(BaseModel):
    id: str
    original_url: str
    status: ImageProcessingType

class GetImageServiceResponseDto(BaseModel):
    id: str
    original_url: str
    svg_url: str
    status: ImageProcessingType
    created_at: datetime

class GetImageListServiceResponseDto(BaseModel):
    items: list[GetImageServiceResponseDto]
    total: int
    page: int
    limit: int