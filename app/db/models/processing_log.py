import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.models.base import TimeStampedModel


class ProcessingLog(TimeStampedModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = Column(UUID(as_uuid=True), ForeignKey('svg_images.id'), nullable=False)
    status = Column(String, nullable=False, default='processing')
    description = Column(String, nullable=True)

    svg_image = relationship('SvgImage', back_populates='processing_logs')

    __tablename__ = 'processing_logs'
