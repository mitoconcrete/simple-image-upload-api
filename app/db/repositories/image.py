from typing import List, Optional
import uuid

from app.db.models.image import Image
from app.db.models.processing_log import ProcessingLog
from app.db.repositories.base import BaseRepository

from app.schemas.dto.repository_response import ImageInfoResponse

class ImageRepository(BaseRepository[Image]):
    def get_info_with_latest_log(self, entity: Image, entity_id: str) -> Optional[ImageInfoResponse | None]:
        image = self.get(entity, entity_id)
        latest_log = self.get_latest_processing_log(entity, entity_id)
        
        if image is None:
            return None
        
        if latest_log is None:
            return ImageInfoResponse(id=image.id, original_url=image.url, created_at=image.created_at)

        return ImageInfoResponse(id=image.id,  original_url=image.url, svg_url=image.svg.url, created_at=latest_log.created_at, status=latest_log.status)

    def get_latest_processing_log(self, entity: Image, entity_id: str) -> Optional[ProcessingLog | None]:
        return self.get(entity, entity_id).processing_log.order_by(ProcessingLog.created_at.desc()).first()

    def get_processing_logs(self, entity: Image, entity_id: str) -> Optional[List[ProcessingLog] | None]:
        return self.get(entity, entity_id).processing_log.order_by(ProcessingLog.created_at.desc()).all()

    def add_processing_log(self, entity_id: uuid.UUID, processing_log: ProcessingLog) -> None:
        entity = self.get(Image, entity_id)
        
        with self.session_factory() as session:
            entity.processing_log.append(processing_log)
            session.merge(entity)
            session.commit()

