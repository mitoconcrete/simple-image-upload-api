from app.db.repositories.image import ImageRepository
from app.db.repositories.processing_log import ProcessingLogRepository
from app.db.repositories.svg import SVGRepository
from app.db.session import session

image_repository = ImageRepository(session)
svg_repository = SVGRepository(session)
processing_log_repository = ProcessingLogRepository(session)

__all__ = ['image_repository', 'svg_repository', 'processing_log_repository']
