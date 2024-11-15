import uuid

from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship

from app.db.models.base import TimeStampedModel


class Image(TimeStampedModel):
    __tablename__ = 'image'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String, nullable=True)
    url = Column(String, nullable=False)

    svg = relationship('SVG', back_populates='image', cascade='all, delete-orphan')
    processing_log = relationship(
        'ProcessingLog', back_populates='image', lazy='selectin', cascade='all, delete-orphan'
    )
