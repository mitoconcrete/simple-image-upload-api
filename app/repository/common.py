from abc import ABC
from typing import Generic, List, Optional, Type, TypeVar

from pydantic import UUID4
from sqlalchemy.orm import Session

from app.schema.dao.common import CommonInput, CommonOutput

T = TypeVar('T')
InputDAO = TypeVar('CommonInput', bound=CommonInput)
OutputDAO = TypeVar('CommonOutput', bound=CommonOutput)


class BaseRepository(ABC, Generic[T, InputDAO, OutputDAO]):
    def __init__(self, session: Session, model: Type[T], output_class: Type[OutputDAO]):
        self.session = session
        self.model = model
        self.output_class = output_class

    def _convert_to_output(self, model: T) -> OutputDAO:
        return self.output_class.model_validate(model)

    def add(self, model: T) -> OutputDAO:
        self.session.add(model)
        self.session.commit()
        return self._convert_to_output(model)

    def get(self, id: UUID4) -> Optional[OutputDAO]:
        model = self.session.query(self.model).filter_by(id=id).first()
        return self._convert_to_output(model) if model else None

    def get_all(self) -> List[OutputDAO]:
        models = self.session.query(self.model).all()
        return [self._convert_to_output(model) for model in models]

    def update(self, id: UUID4, data: InputDAO) -> Optional[OutputDAO]:
        self.session.query(self.model).filter_by(id=id).update(data.model_dump(), synchronize_session='fetch')
        self.session.commit()
        updated_model = self.session.query(self.model).filter_by(id=id).first()
        return self._convert_to_output(updated_model) if updated_model else None

    def delete(self, id: UUID4) -> None:
        deleted_model = self.session.query(self.model).filter_by(id=id).first()
        if deleted_model:
            self.session.delete(deleted_model)
            self.session.commit()

    def delete_all(self) -> None:
        self.session.query(self.model).delete()
        self.session.commit()
