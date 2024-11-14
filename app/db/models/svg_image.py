import uuid

from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models.base import TimeStampedModel


class SvgImage(TimeStampedModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    optimized_url = Column(UUID(as_uuid=True), ForeignKey('images.id'), nullable=False)

    image = relationship('Image', back_populates='svg_image', uselist=False)

    __tablename__ = 'svg_images'
