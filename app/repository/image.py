from typing import Optional

from pydantic import UUID4

from app.model.image import Image, ProcessingLog
from app.repository.common import BaseRepository
from app.schema.dao.image import (
    ImageInput,
    ImageOutput,
    ImagePaginationOutput,
    MixinImageProcessingLogOutput,
    ProcessingLogInput,
    ProcessingLogOutput,
)


class ImageRepository(BaseRepository[Image, ImageInput, ImageOutput]):
    def get_latest_image(self, id: UUID4) -> Optional[MixinImageProcessingLogOutput | None]:
        result = (
            self.session.query(
                self.model.id,
                self.model.original_url,
                self.model.svg_url,
                ProcessingLog.status,
                self.model.created_at,
                self.model.updated_at,
            )
            .outerjoin(ProcessingLog)
            .filter(self.model.id == id)
            .order_by(ProcessingLog.created_at.desc())
            .first()
        )
        return self._convert_to_output(result, MixinImageProcessingLogOutput) if result else None

    def get_images_with_pagination(self, limit: int, offset: int) -> ImagePaginationOutput:
        total = self.session.query(self.model).count()
        result = (
            self.session.query(
                self.model.id,
                self.model.original_url,
                self.model.svg_url,
                ProcessingLog.status,
                self.model.created_at,
                self.model.updated_at,
            )
            .outerjoin(ProcessingLog)
            .limit(limit)
            .offset(offset)
            .all()
        )
        return ImagePaginationOutput(
            total=total,
            limit=limit,
            page=offset,
            items=[self._convert_to_output(image, MixinImageProcessingLogOutput) for image in result],
        )


class ProcessingLogRepository(BaseRepository[ProcessingLog, ProcessingLogInput, ProcessingLogOutput]):
    pass
