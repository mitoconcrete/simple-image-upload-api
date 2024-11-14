from abc import ABC
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import sessionmaker

T = TypeVar('T')


# 레포지토리 구현을 위한 기본 클래스
class BaseRepository(ABC, Generic[T]):
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def add(self, entity: T) -> None:
        with self.session_factory() as session:
            session.add(entity)
            session.commit()

    def get(self, entity_class: Type[T], entity_id: int) -> Optional[T]:
        with self.session_factory() as session:
            return session.query(entity_class).get(entity_id)

    def list(self, entity_class: Type[T]) -> List[T]:
        with self.session_factory() as session:
            return session.query(entity_class).all()

    def update(self, entity: T) -> None:
        with self.session_factory() as session:
            session.merge(entity)
            session.commit()

    def delete(self, entity: T) -> None:
        with self.session_factory() as session:
            session.delete(entity)
            session.commit()
