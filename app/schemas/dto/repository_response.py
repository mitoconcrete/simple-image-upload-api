from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel


class ImageInfoResponse(BaseModel):
    id: uuid.UUID
    original_url: str
    svg_url: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime