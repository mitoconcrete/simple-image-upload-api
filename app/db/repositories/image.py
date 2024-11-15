from typing import List, Optional
from app.db.models.image import Image
from app.db.models.processing_log import ProcessingLog
from app.db.repositories.base import BaseRepository


class ImageRepository(BaseRepository[Image]):
    def get_processing_logs(self, entity: Image, entity_id: str) -> Optional[List[ProcessingLog] | None]:
        return self.get(entity, entity_id).processing_log
