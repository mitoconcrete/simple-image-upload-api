from app.db.engine import engine
from app.db.models.base import Base
from app.db.models.image import Image
from app.db.models.processing_log import ProcessingLog
from app.db.models.svg_image import SVGImage

Base.metadata.create_all(bind=engine, tables=[Image.__table__, SVGImage.__table__, ProcessingLog.__table__])

__all__ = ['Image', 'SVGImage', 'ProcessingLog']
