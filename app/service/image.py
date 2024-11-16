from app.util.image_util import is_jpg_or_png, get_image_size
from app.exception.common import NotSupportedTypeException, OutOfAllowedCountException, OutOfAllowedSizeException
from app.repository.image import ImageRepository, ProcessingLogRepository

MAXIMUM_IMAGE_SIZE = 1024 * 1024 * 5 # 5MB
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
            raise OutOfAllowedCountException("The number of images should be less than 3")
        
        # 이미지 중 하나라도 예외가 발생하면 바로 예외를 발생시키고, 모두 통과하면 True를 반환합니다.
        for image in images:
            if not is_jpg_or_png(image):
                raise NotSupportedTypeException("The image type should be jpg or png")

            if get_image_size(image) > MAXIMUM_IMAGE_SIZE:
                raise OutOfAllowedSizeException(f"The image size should be less than {MAXIMUM_IMAGE_SIZE} bytes")
        return True

    
        
    # def create(self, image):
    #     return self.image_repository.create(image)

    # def get(self, image_id):
    #     return self.image_repository.get(image_id)

    # def update(self, image_id, image):
    #     return self.image_repository.update(image_id, image)

    # def delete(self, image_id):
    #     return self.image_repository.delete(image_id)
