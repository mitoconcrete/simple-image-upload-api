import uuid
import random
from functools import wraps
from typing import Optional
from datetime import datetime

from app.db.models.image import Image
from app.db.models.processing_log import ProcessingLog
from app.db.repositories import image_repository

from app.schemas.dto.service_response import GetImageServiceResponseDto, ImageDetailResponse, ImageSimpleResponse, UploadServiceResponseDto
from app.schemas.enum import ImageProcessingType
from app.schemas.dto.service_request import UploadImage, UploadImageServiceRequestDto, UploadSVGServiceRequestDto, UploadServiceRequestDto
from app.schemas.dto.service_response import UploadImageServiceResponseDto, UploadSVGServiceResponseDto

from app.utils.exception import UploadServiceError, UploadServiceValidationError
from app.utils.image_tool import is_image_type_jpg_or_png, basic_image_preprocessor, get_image_type, _svg_optimizer, process_image_to_svg
from app.utils.image_uploader import upload

MAXIMUM_IMAGE_COUNT = 3
MAXIMUM_IMAGE_SIZE = 1024 * 1024 * 5  # 5MB
BUCKET_NAME = 'tk.asset.image'

def _is_allowed_image_type(image: UploadImage) -> bool:
    return is_image_type_jpg_or_png(image.image)

def _is_allowed_image_size(image: UploadImage) -> bool:
    return len(image.image) < MAXIMUM_IMAGE_SIZE

def _is_allowed_image_count(images: list[UploadImage]) -> bool:
    return len(images) <= MAXIMUM_IMAGE_COUNT

def _get_image_type(image: bytes) -> str:
    return get_image_type(image)

def _get_save_path(image_type: str) -> str:
    # 이미지타입/날짜/타입스탬프-난수(5자리)-난수(3자리)-난수(1자리).확장자
    file_name = f'{datetime.now().strftime("%Y%m%d%H%M%S")}-{random.randint(10000, 99999)}-{random.randint(100, 999)}-{random.randint(0, 9)}'
    return f'{image_type.upper()}/{datetime.now().strftime("%Y%m%d")}/{file_name}.{image_type}'

def _save_processing_log(original_id: uuid.UUID, status: ImageProcessingType, description: str) -> None:
    image_repository.add_processing_log(original_id, ProcessingLog(status=status, description=description))

def _upload_image(bucket_name: str, save_path: str, image: bytes, label: Optional[str] = None) -> UploadImageServiceResponseDto:
    original_url = upload(bucket_name=bucket_name, save_path=save_path, image=image)
    original_id = image_repository.add(Image(label=label, url=original_url))

    return UploadImageServiceResponseDto(
        id=original_id,
        original_url=original_url,
        image=image
    )

def _upload_svg(bucket_name: str, save_path: str, image: bytes) -> UploadSVGServiceResponseDto:
    processed_url = upload(bucket_name=bucket_name, save_path=save_path, image=image)
    processed_id = image_repository.add(Image(label=None, url=processed_url))
    return UploadSVGServiceResponseDto(
        id=processed_id,
        proccessed_url=processed_url
    )

def _upload_image_service(dto: UploadImageServiceRequestDto) -> UploadImageServiceResponseDto:
    save_path = _get_save_path(_get_image_type(dto.image))
    preprocessed = basic_image_preprocessor(dto.image)
    return _upload_image(BUCKET_NAME, save_path, preprocessed)

def _upload_svg_service(dto: UploadSVGServiceRequestDto) -> UploadSVGServiceResponseDto:
    save_path = _get_save_path("svg")
    processed = process_image_to_svg(dto.image)
    optimized = _svg_optimizer(processed)
    return _upload_svg(BUCKET_NAME, save_path, optimized)

def validate(dto: UploadServiceRequestDto) -> None:
    if not _is_allowed_image_count([dto.images]):
        raise UploadServiceValidationError('Maximum image count exceeded.')
    if not all(_is_allowed_image_size(image) for image in dto.images):
        raise UploadServiceValidationError('Maximum image size exceeded.')
    if not all(_is_allowed_image_type(image) for image in dto.images):
        raise UploadServiceValidationError('Invalid image type.')
    
def get_image_info(image_id: uuid.UUID) -> Optional[GetImageServiceResponseDto | None]:
    info = image_repository.get_info_with_latest_log(Image, image_id)
    return GetImageServiceResponseDto(**info.model_dump()) if info else None

def log_processing(original_id_attr: str, start_status: ImageProcessingType, end_status: ImageProcessingType):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            dto = args[0]
            original_id = getattr(dto, original_id_attr)
            try:
                _save_processing_log(original_id, start_status, f'{original_id} processing started.')
                result = func(*args, **kwargs)
                _save_processing_log(original_id, end_status, f'{original_id} processing completed.')
                return result
            except Exception as e:
                _save_processing_log(original_id, ImageProcessingType.FAILED, f'{original_id} processing failed.')
                raise UploadServiceError(f'{original_id} processing failed.') from e
        return wrapper
    return decorator

def error_handling_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
    return wrapper

@log_processing('id', ImageProcessingType.READY, ImageProcessingType.PROCESSING)
def upload_image_service_with_logging(dto: UploadImageServiceRequestDto) -> UploadImageServiceResponseDto:
    return _upload_image_service(dto)

@log_processing('original_id', ImageProcessingType.PROCESSING, ImageProcessingType.COMPLETED)
def upload_svg_service_with_logging(dto: UploadSVGServiceRequestDto) -> UploadSVGServiceResponseDto:
    return _upload_svg_service(dto)

@error_handling_decorator
def upload_service(dto: UploadServiceRequestDto) -> UploadServiceResponseDto:
    validate(dto)
    responses = []
    for image in dto.images:
        image_dto = UploadImageServiceRequestDto(**image.model_dump())
        image_response = upload_image_service_with_logging(image_dto)
        svg_dto = UploadSVGServiceRequestDto(**image_response.model_dump())
        svg_response = upload_svg_service_with_logging(svg_dto)
        result = ImageSimpleResponse(**get_image_info(svg_response.id)) if get_image_info(svg_response.id) else None
        responses.append(result)
    return UploadServiceResponseDto(images=[response for response in responses if response is not None])


def get_image_list(page: int, limit: int) -> UploadServiceResponseDto:
    images = image_repository.list(Image, page, limit)
    responses = []
    for image in images:
        info = image_repository.get_info_with_latest_log(Image, image.id)
        responses.append(ImageDetailResponse(**info.model_dump()))
    return UploadServiceResponseDto(images=[response for response in responses if response is not None])