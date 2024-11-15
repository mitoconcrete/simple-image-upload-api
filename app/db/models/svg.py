import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.models.base import TimeStampedModel


class SVG(TimeStampedModel):
    __tablename__ = 'svg'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(UUID(as_uuid=True), ForeignKey('image.id'), nullable=False)
    url = Column(String, nullable=False)

    image = relationship('Image', back_populates='svg', lazy='joined')
