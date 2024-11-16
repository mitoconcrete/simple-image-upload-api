from app.repository.image import ImageRepository, ProcessingLogRepository, SVGRepository


class ImageService:
    def __init__(
        self,
        image_repository: ImageRepository,
        svg_repository: SVGRepository,
        processing_log_repository: ProcessingLogRepository,
    ):
        self.image_repository = image_repository
        self.svg_repository = svg_repository
        self.processing_log_repository = processing_log_repository

    def create(self, image):
        return self.image_repository.create(image)

    def get(self, image_id):
        return self.image_repository.get(image_id)

    def update(self, image_id, image):
        return self.image_repository.update(image_id, image)

    def delete(self, image_id):
        return self.image_repository.delete(image_id)
