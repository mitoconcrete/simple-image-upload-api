from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel

from app.schema.enum.image import ImageProcessingType


class ImageServiceInput(BaseModel):
    pass


class SaveLogInput(BaseModel):
    original_id: UUID4
    status: ImageProcessingType


class ImageServiceOutput(BaseModel):
    id: UUID4
    original_url: str
    svg_url: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    def model_dump(self):
        data = super().model_dump()
        data['status'] = ImageProcessingType(data['status'])
        return data


class ImageServicePaginationOutput(BaseModel):
    total: int
    limit: int
    page: int
    items: list[ImageServiceOutput]

    def model_dump(self):
        data = super().model_dump()
        data['items'] = [ImageServiceOutput(**item) for item in data['items']]
        return data
