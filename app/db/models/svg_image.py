import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.models.base import TimeStampedModel


class SVGImage(TimeStampedModel):
    __tablename__ = 'svg_image'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(UUID(as_uuid=True), ForeignKey('image.id'), nullable=False)
    url = Column(String, nullable=False)

    image = relationship('Image', back_populates='svg_image', lazy='joined')
    processing_log = relationship(
        'ProcessingLog', back_populates='svg_image', lazy='selectin', cascade='all, delete-orphan'
    )
