from typing import Optional

from pydantic import UUID4
from sqlalchemy import func

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
        subquery = (
            self.session.query(
                ProcessingLog.id,
                ProcessingLog.original_id,
                ProcessingLog.status,
                func.max(ProcessingLog.created_at).label('created_at'),
            )
            .group_by(ProcessingLog.original_id)
            .subquery()
        )

        result = (
            self.session.query(
                self.model.id,
                self.model.original_url,
                self.model.svg_url,
                subquery.c.id.label('processing_log_id'),
                subquery.c.status,
                self.model.created_at,
                self.model.updated_at,
            )
            .outerjoin(subquery, subquery.c.original_id == self.model.id)
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .offset(offset * limit)
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
