from typing import Optional
import uuid

from pydantic import BaseModel

class UploadImage(BaseModel):
    image: bytes
    label: Optional[str] = None

class UploadServiceRequestDto(BaseModel):
    images: list[UploadImage]

class UploadImageServiceRequestDto(UploadImage):
    pass

class UploadSVGServiceRequestDto(BaseModel):
    original_id: uuid.UUID
    image: bytes

class GetImageServiceResquestDto(BaseModel):
    image_id: str


class GetImageListServiceResponseDto(BaseModel):
    page: int
    limit: int  # page_size
