import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.config.database import Base


class Image(Base):
    __tablename__ = 'image'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(String, nullable=False)
    svg_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    processing_log = relationship(
        'ProcessingLog', back_populates='image', lazy='selectin', cascade='all, delete-orphan'
    )


class ProcessingLog(Base):
    __tablename__ = 'processing_log'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(UUID(as_uuid=True), ForeignKey('image.id'), nullable=False)
    status = Column(String, nullable=False, default='ready')
    created_at = Column(DateTime, default=datetime.now)

    image = relationship('Image', back_populates='processing_log')
