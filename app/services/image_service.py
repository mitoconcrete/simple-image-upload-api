from app.schemas.request_dto import ImageUploadServiceRequestDto
from app.utils.image_tool import is_image_type_jpg_or_png

MAXIMUM_IMAGE_SIZE = 1024 * 1024 * 5  # 5MB


def _is_allowed_image_type(dto: ImageUploadServiceRequestDto) -> bool:
    return is_image_type_jpg_or_png(dto.image)


def _is_allowed_image_size(dto: ImageUploadServiceRequestDto) -> bool:
    return len(dto.image) < MAXIMUM_IMAGE_SIZE
