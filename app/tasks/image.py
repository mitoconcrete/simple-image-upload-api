import logging

from celery import Celery
from pydantic import UUID4

from app.config.database import get_db
from app.config.env import env
from app.model.image import Image, ProcessingLog
from app.repository.image import ImageRepository, ProcessingLogRepository
from app.schema.dao.image import ImageOutput, ProcessingLogOutput
from app.schema.dto.image import SaveLogInput
from app.schema.enum.image import ImageProcessingType
from app.service.image import ImageService
from app.util.image_util import create_save_path

celery = Celery('tasks', broker=env.MESSAGES_BROKER_URL)

@celery.task(ignore_result=True, name='이미지를 svg로 변환하는 작업')
def process_image_task(original_id: UUID4, image_bytes: bytes):
    image_repo = ImageRepository(next(get_db()), Image, ImageOutput)
    processing_log_repo = ProcessingLogRepository(next(get_db()), ProcessingLog, ProcessingLogOutput)
    service = ImageService(image_repo, processing_log_repo)

    try:
        service.save_log(SaveLogInput(original_id=original_id, status=ImageProcessingType.PROCESSING))
        processed_image = service.process(image_bytes)
        processed_filename = create_save_path('svg')
        svg_url = service.upload(processed_filename, processed_image)
        service.update(original_id, svg_url)
        service.save_log(SaveLogInput(original_id=original_id, status=ImageProcessingType.COMPLETED))
    except Exception as e:
        service.save_log(SaveLogInput(original_id=original_id, status=ImageProcessingType.FAILED))
        logging.error(str(e))