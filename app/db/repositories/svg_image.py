from typing import List, Optional

from app.db.models.processing_log import ProcessingLog
from app.db.models.svg_image import SVGImage
from app.db.repositories.base import BaseRepository


class SVGImageRepository(BaseRepository[SVGImage]):
    def get_processing_logs(self, entity: SVGImage, entity_id: str) -> Optional[List[ProcessingLog] | None]:
        return self.get(entity, entity_id).processing_log
