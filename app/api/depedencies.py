from fastapi import Depends
from pytest import Session

from app.config.database import get_db
from app.model.image import Image, ProcessingLog
from app.repository.image import ImageRepository, ProcessingLogRepository
from app.schema.dao.image import ImageOutput, ProcessingLogOutput
from app.service.image import ImageService


def get_image_repository(db: Session = Depends(get_db)):
    return ImageRepository(db, Image, ImageOutput)


def get_processing_log_repository(db: Session = Depends(get_db)):
    return ProcessingLogRepository(db, ProcessingLog, ProcessingLogOutput)


def get_image_service(
    image_repository: ImageRepository = Depends(get_image_repository),
    processing_log_repository: ProcessingLogRepository = Depends(get_processing_log_repository),
):
    return ImageService(image_repository, processing_log_repository)
