from datetime import datetime
from typing import Optional

from pydantic import UUID4

from app.schema.dao.common import CommonInput, CommonOutput
from app.schema.enum.image import ImageProcessingType

"""
database related input schema
"""


class ImageInput(CommonInput):
    original_url: str
    svg_url: Optional[str] = None
    label: Optional[str] = None


class ProcessingLogInput(CommonInput):
    status: ImageProcessingType
    description: Optional[str] = None

    def model_dump(self):
        data = super().model_dump()
        data['status'] = data['status'].value
        return data


"""
database related output schema
"""


class ProcessingLogOutput(CommonOutput):
    id: UUID4
    original_id: UUID4
    status: ImageProcessingType
    description: Optional[str] = None
    created_at: datetime

    def model_dump(self):
        data = super().model_dump()
        data['status'] = ImageProcessingType(data['status'])
        return data


class ImageOutput(CommonOutput):
    id: UUID4
    original_url: str
    svg_url: Optional[str] = None
    label: Optional[str] = None
    processing_log: list[ProcessingLogOutput] = []
    created_at: datetime
    updated_at: datetime

    def model_dump(self):
        data = super().model_dump()
        data['processing_log'] = [ProcessingLogOutput(**log).model_dump() for log in data['processing_log']]
        return data


class MixinImageProcessingLogOutput(CommonOutput):
    id: UUID4
    original_url: str
    svg_url: Optional[str] = None
    status: Optional[ImageProcessingType] = None
    created_at: datetime
    updated_at: datetime

    def model_dump(self):
        data = super().model_dump()
        data['status'] = ImageProcessingType(data['status'])
        data['processing_log'] = [ProcessingLogOutput(**log).model_dump() for log in data['processing_log']]
        return data


class ImagePaginationOutput(CommonOutput):
    total: int
    page: int
    limit: int
    items: list[MixinImageProcessingLogOutput] = []
