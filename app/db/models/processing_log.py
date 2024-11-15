import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.models.base import TimeStampedModel


class ProcessingLog(TimeStampedModel):
    __tablename__ = 'processing_log'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(UUID(as_uuid=True), ForeignKey('image.id'), nullable=False)
    status = Column(String, nullable=False, default='ready')
    description = Column(String, nullable=True)

    image = relationship('Image', back_populates='processing_log')
