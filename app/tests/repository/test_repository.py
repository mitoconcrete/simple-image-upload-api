import pytest

from app.model.image import Image, ProcessingLog
from app.repository.image import ImageRepository, ProcessingLogRepository
from app.schema.dao.image import ImageInput, ImageOutput, ProcessingLogInput, ProcessingLogOutput
from app.schema.enum.image import ImageProcessingType
from app.tests.helper import get_test_db


class TestRepository:
    @pytest.fixture
    def test_session(self):
        return next(get_test_db())

    @pytest.fixture
    def image_repository(self, test_session) -> ImageRepository:
        return ImageRepository(test_session, Image, ImageOutput)

    @pytest.fixture
    def processing_log_repository(self, test_session) -> ProcessingLogRepository:
        return ProcessingLogRepository(test_session, ProcessingLog, ProcessingLogOutput)

    def test_create_image(self, image_repository: ImageRepository):
        new_image = Image(label='test', original_url='test')
        created_image = image_repository.add(new_image)

        assert created_image.id is not None

    def test_create_svg(self, image_repository: ImageRepository):
        new_image = Image(label='test', original_url='test', svg_url='test2')

        created_image = image_repository.add(new_image)

        assert created_image.svg_url == 'test2'

    def test_create_processing_log(
        self, image_repository: ImageRepository, processing_log_repository: ProcessingLogRepository
    ):
        new_image = Image(label='test', original_url='test', svg_url='test2')
        new_processing_log = ProcessingLog(status=ImageProcessingType.PROCESSING.value, description='test')

        new_image.processing_log.append(new_processing_log)

        created_image = image_repository.add(new_image)
        created_processing_log = processing_log_repository.add(new_processing_log)

        retrieved_processing_log = processing_log_repository.get(created_processing_log.id)

        assert retrieved_processing_log.original_id == created_image.id
        assert retrieved_processing_log.id == created_processing_log.id
        assert retrieved_processing_log.status == 'processing'
        assert retrieved_processing_log.description == 'test'

    def test_get_images(self, image_repository: ImageRepository):
        new_image01 = Image(label='test', original_url='test')
        new_image02 = Image(label='test2', original_url='test2')

        image_repository.add(new_image01)
        image_repository.add(new_image02)

        created_images = image_repository.get_all()
        assert len(created_images) == 2
        assert created_images[0].label == 'test'
        assert created_images[0].original_url == 'test'
        assert created_images[1].label == 'test2'
        assert created_images[1].original_url == 'test2'

    def test_update_image(self, image_repository: ImageRepository):
        new_image = Image(label='test', original_url='test')
        created_image = image_repository.add(new_image)

        created_image.svg_url = 'test2'
        update_data = ImageInput(**created_image.model_dump())
        image_repository.update(created_image.id, update_data)

        retrieved_image = image_repository.get(created_image.id)

        assert retrieved_image.svg_url == 'test2'

    def test_update_processing_log(
        self, image_repository: ImageRepository, processing_log_repository: ProcessingLogRepository
    ):
        new_image = Image(label='test', original_url='test', svg_url='test2')
        new_processing_log = ProcessingLog(status=ImageProcessingType.READY, description='test')

        new_image.processing_log.append(new_processing_log)

        image_repository.add(new_image)
        created_processing_log = processing_log_repository.add(new_processing_log)

        update_data = ProcessingLogInput(status=ImageProcessingType.COMPLETED, description='test')
        processing_log_repository.update(created_processing_log.id, update_data)

        retrieved_processing_log = processing_log_repository.get(created_processing_log.id)
        assert retrieved_processing_log.status == ImageProcessingType.COMPLETED

    def test_delete_image(self, image_repository: ImageRepository):
        new_image = Image(label='test', original_url='test')

        created_image = image_repository.add(new_image)

        image_repository.delete(created_image.id)

        retrieved_image = image_repository.get(created_image.id)
        assert retrieved_image is None

    def test_delete_processing_log(
        self, image_repository: ImageRepository, processing_log_repository: ProcessingLogRepository
    ):
        new_image = Image(label='test', original_url='test', svg_url='test2')
        new_processing_log = ProcessingLog(status='processing', description='test')

        new_image.processing_log.append(new_processing_log)

        image_repository.add(new_image)
        created_processing_log = processing_log_repository.add(new_processing_log)

        processing_log_repository.delete(created_processing_log.id)
        retrieved_processing_log = processing_log_repository.get(created_processing_log.id)
        assert retrieved_processing_log is None

    def test_delete_image_cascade(
        self,
        image_repository: ImageRepository,
        processing_log_repository: ProcessingLogRepository,
    ):
        new_image = Image(label='test', original_url='test', svg_url='test2')
        new_processing_log = ProcessingLog(status='processing', description='test')

        new_image.processing_log.append(new_processing_log)

        created_image = image_repository.add(new_image)
        created_processing_log = processing_log_repository.add(new_processing_log)

        image_repository.delete(created_image.id)

        assert image_repository.get(created_image.id) is None
        assert processing_log_repository.get(created_processing_log.id) is None

    def test_get_image_with_processing_log(
        self,
        image_repository: ImageRepository,
        processing_log_repository: ProcessingLogRepository,
    ):
        new_image = Image(label='test', original_url='test', svg_url='test2')
        new_processing_log = ProcessingLog(status=ImageProcessingType.PROCESSING.value, description='test')
        new_processing_log2 = ProcessingLog(status=ImageProcessingType.FAILED.value, description='test2')

        new_image.processing_log.append(new_processing_log)
        new_image.processing_log.append(new_processing_log2)

        created_image = image_repository.add(new_image)
        created_processing_log = processing_log_repository.add(new_processing_log)

        processing_logs = image_repository.get(created_image.id).processing_log

        assert len(processing_logs) == 2

        assert processing_logs[0].id == created_processing_log.id
        assert processing_logs[0].original_id == created_image.id
        assert processing_logs[0].status == ImageProcessingType.PROCESSING
        assert processing_logs[0].description == 'test'
        assert processing_logs[0].created_at is not None

        assert processing_logs[1].status == ImageProcessingType.FAILED
        assert processing_logs[1].description == 'test2'

    def test_get_mixin_image_processing_logs_empty(self, image_repository: ImageRepository):
        new_image = Image(label='test', original_url='test', svg_url='test2')

        created_image = image_repository.add(new_image)

        processing_logs = image_repository.get(created_image.id).processing_log

        assert len(processing_logs) == 0

    def test_get_mixin_image_processing_log(self, image_repository: ImageRepository):
        new_image = Image(label='test', original_url='test', svg_url='test2')
        new_processing_log = ProcessingLog(status=ImageProcessingType.PROCESSING.value, description='test')
        new_processing_log2 = ProcessingLog(status=ImageProcessingType.FAILED.value, description='test2')

        new_image.processing_log.append(new_processing_log)
        new_image.processing_log.append(new_processing_log2)

        created_image = image_repository.add(new_image)
        latest_image = image_repository.get_latest_image(created_image.id)

        assert latest_image.id == created_image.id
        assert latest_image.original_url == 'test'
        assert latest_image.svg_url == 'test2'
        assert latest_image.status == ImageProcessingType.FAILED
        assert latest_image.created_at is not None
        assert latest_image.updated_at is not None

    def test_pagination(self, image_repository: ImageRepository):
        new_image01 = Image(label='test', original_url='test')
        new_image02 = Image(label='test2', original_url='test2')

        image_repository.add(new_image01)
        image_repository.add(new_image02)

        created_images = image_repository.get_images_with_pagination(limit=1, offset=0)
        assert created_images.total == 2
        assert created_images.page == 0
        assert created_images.limit == 1
        assert created_images.items[0].original_url == 'test'

        created_images = image_repository.get_images_with_pagination(limit=1, offset=1)
        assert created_images.total == 2
        assert created_images.page == 1
        assert created_images.limit == 1
        assert created_images.items[0].original_url == 'test2'
