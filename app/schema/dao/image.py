from datetime import datetime
from typing import Optional
from pydantic import UUID4
from app.schema.dao.common import CommonInput, CommonOutput
from app.schema.enum.image import ImageProcessingType

"""
database related input schema
"""
class ImageInput(CommonInput):
    url: str
    label: Optional[str] = None

class SVGInput(CommonInput):
    url: str

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
class ImageOutput(CommonOutput):
    id : UUID4
    url: str
    label: Optional[str] = None
    created_at: datetime

class SVGOutput(CommonOutput):
    id: UUID4
    original_id: UUID4
    url: str
    created_at: datetime

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

