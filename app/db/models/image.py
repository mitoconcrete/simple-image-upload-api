import uuid

from sqlalchemy.orm import relationship
from sqlalchemy import UUID, Column, String

from app.db.models.base import TimeStampedModel


class Image(TimeStampedModel):
    __tablename__ = 'image'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String, nullable=False)
    url = Column(String, nullable=False)

    svg_image = relationship("SVGImage", back_populates="image", cascade="all, delete-orphan")

