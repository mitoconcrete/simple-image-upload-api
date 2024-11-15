from app.config.database import get_db
from app.model.image import SVG, Image, ProcessingLog
from app.repository.image import ImageRepository, ProcessingLogRepository, SVGRepository
from app.schema.dao.image import ImageInput, ImageOutput, ProcessingLogInput, ProcessingLogOutput, SVGInput, SVGOutput

session = next(get_db())

kwargs = [
    (Image, ImageOutput),
    (SVG, SVGOutput),
    (ProcessingLog, ProcessingLogOutput),
]

image_repository = ImageRepository(session, *kwargs[0])
svg_repository = SVGRepository(session, *kwargs[1])
processing_log_repository = ProcessingLogRepository(session, *kwargs[2])

__all__ = ["image_repository", "svg_repository", "processing_log_repository"]