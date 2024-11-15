import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.models.base import TimeStampedModel


class ProcessingLog(TimeStampedModel):
    __tablename__ = 'processing_log'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = Column(UUID(as_uuid=True), ForeignKey('svg_image.id'), nullable=False)
    status = Column(String, nullable=False, default='processing')
    description = Column(String, nullable=True)

    svg_image = relationship('SVGImage', back_populates='processing_log')
