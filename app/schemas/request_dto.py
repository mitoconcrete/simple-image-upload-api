from typing import Optional

from pydantic import BaseModel


class ImageUploadServiceRequestDto(BaseModel):
    image: bytes
    label: Optional[str] = None

class GetImageServiceResquestDto(BaseModel):
    image_id: str

class GetImageListServiceResponseDto(BaseModel):
    page: int
    limit: int # page_size