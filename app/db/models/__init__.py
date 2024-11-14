from app.db.models.base import Base
from app.db.models.image import Image
from app.db.models.processing_log import ProcessingLog
from app.db.models.svg_image import SVGImage
from app.db.services.engine import engine

Base.metadata.create_all(bind=engine, tables=[Image.__table__, SVGImage.__table__, ProcessingLog.__table__])

__all__ = ['Image', 'SVGImage', 'ProcessingLog']