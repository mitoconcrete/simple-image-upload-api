from typing import Optional

from app.exception.image import (
    NotSupportedTypeException,
    OutOfAllowedCountException,
    OutOfAllowedSizeException,
    PreProcessImageException,
    ProcessImageException,
    SaveException,
    UploadException,
)
from app.model.image import Image, ProcessingLog
from app.repository.image import ImageRepository, ProcessingLogRepository
from app.schema.dao.image import ImageInput
from app.schema.dto.image import ImageServiceOutput, ImageServicePaginationOutput, SaveLogInput
from app.util.helper import exception_handler
from app.util.image_util import get_image_size, is_jpg_or_png, preprocess_image, process_image
from app.util.s3_uploder import S3Uploader

BUCKET_NAME = 'tk.asset.image'
MAXIMUM_IMAGE_SIZE = 1024 * 1024 * 5  # 5MB
MAX_ALLOWED_IMAGE_COUNT = 3


class ImageService:
    def __init__(
        self,
        image_repository: ImageRepository,
        processing_log_repository: ProcessingLogRepository,
    ):
        self.image_repository = image_repository
        self.processing_log_repository = processing_log_repository

    def validate(self, images: list[bytes]) -> bool:
        if len(images) > MAX_ALLOWED_IMAGE_COUNT:
            raise OutOfAllowedCountException('The number of images should be less than 3')

        # 이미지 중 하나라도 예외가 발생하면 바로 예외를 발생시키고, 모두 통과하면 True를 반환합니다.
        for image in images:
            if not is_jpg_or_png(image):
                raise NotSupportedTypeException('The image type should be jpg or png')

            if get_image_size(image) > MAXIMUM_IMAGE_SIZE:
                raise OutOfAllowedSizeException(f'The image size should be less than {MAXIMUM_IMAGE_SIZE} bytes')
        return True

    @exception_handler(PreProcessImageException)
    def preprocess(self, image: bytes) -> bytes:
        return preprocess_image(image)

    @exception_handler(ProcessImageException)
    def process(self, image: bytes) -> bytes:
        return process_image(image)

    @exception_handler(UploadException)
    def upload(self, name: str, image: bytes) -> str:
        s3_uploader = S3Uploader()
        s3_uploader.create_bucket(BUCKET_NAME)
        return s3_uploader.upload_file(BUCKET_NAME, name, image)

    @exception_handler(SaveException)
    def save(self, upload_url) -> ImageServiceOutput:
        new_image = Image(original_url=upload_url)
        save_result = self.image_repository.add(new_image)
        return ImageServiceOutput(**save_result.model_dump())

    @exception_handler(SaveException)
    def save_log(self, payload: SaveLogInput):
        new_log = ProcessingLog(original_id=payload.original_id, status=payload.status.value)
        self.processing_log_repository.add(new_log)

    @exception_handler(ImageServiceOutput)
    def get(self, image_id: str) -> Optional[ImageServiceOutput | None]:
        latest_image = self.image_repository.get_latest_image(image_id)
        return ImageServiceOutput(**latest_image.model_dump())

    @exception_handler(ImageServiceOutput)
    def get_all(self, limit: int, offset: int) -> ImageServicePaginationOutput:
        images = self.image_repository.get_images_with_pagination(limit, offset)
        return ImageServicePaginationOutput(**images.model_dump())

    @exception_handler(ImageServiceOutput)
    def update(self, image_id: str, svg_url: str) -> ImageServiceOutput:
        update_data = ImageInput(svg_url=svg_url)
        updated_image = self.image_repository.update(image_id, update_data)
        return ImageServiceOutput(**updated_image.model_dump())
