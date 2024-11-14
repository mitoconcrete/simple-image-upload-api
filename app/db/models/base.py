from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TimeStampedModel(Base):
    __abstract__ = True  # 이 클래스는 테이블을 생성하지 않음
    created_at = Column(DateTime, default=datetime.now)
