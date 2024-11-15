from datetime import datetime

from sqlalchemy import Column, DateTime

from app.config.database import Base


class TimeStampedModel(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now)
