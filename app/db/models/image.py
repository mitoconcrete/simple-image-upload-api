import uuid

from sqlalchemy import UUID, Column, String

from app.db.models.base import TimeStampedModel


class Image(TimeStampedModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String, nullable=False)
    original_url = Column(String, nullable=False)

    __tablename__ = 'image'
