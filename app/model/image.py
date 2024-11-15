import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.model.common import TimeStampedModel


class Image(TimeStampedModel):
    __tablename__ = 'image'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String, nullable=True)
    url = Column(String, nullable=False)

    svg = relationship('SVG', back_populates='image', cascade='all, delete-orphan')
    processing_log = relationship(
        'ProcessingLog', back_populates='image', lazy='selectin', cascade='all, delete-orphan'
    )

class SVG(TimeStampedModel):
    __tablename__ = 'svg'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(UUID(as_uuid=True), ForeignKey('image.id'), nullable=False)
    url = Column(String, nullable=False)

    image = relationship('Image', back_populates='svg', lazy='joined')


class ProcessingLog(TimeStampedModel):
    __tablename__ = 'processing_log'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(UUID(as_uuid=True), ForeignKey('image.id'), nullable=False)
    status = Column(String, nullable=False, default='ready')
    description = Column(String, nullable=True)

    image = relationship('Image', back_populates='processing_log')
