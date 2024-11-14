from app.db.repositories.image import ImageRepository
from app.db.repositories.processing_log import ProcessingLogRepository
from app.db.repositories.svg_image import SvgImageRepository
from app.db.services.session import session

image_repository = ImageRepository(session)
svg_image_repository = SvgImageRepository(session)
processing_log_repository = ProcessingLogRepository(session)

__all__ = ['image_repository', 'svg_image_repository', 'processing_log_repository']
