import pytest

from app.exception.common import NotSupportedTypeException, OutOfAllowedCountException, OutOfAllowedSizeException
from app.model.image import Image, ProcessingLog
from app.repository.image import ImageRepository, ProcessingLogRepository
from app.schema.dao.image import ImageOutput, ProcessingLogOutput
from app.service.image import ImageService
from app.tests.helper import create_test_image, create_test_svg, create_test_text, delete_test_image, delete_test_text, get_test_db


class TestImageService:
    @pytest.fixture(scope='class', autouse=True)
    def setup_and_teardown(self):
        # 테스트 파일 생성
        create_test_image('app/tests/util/test_image.jpg', 'JPEG')
        create_test_svg('app/tests/util/test_image.svg')
        create_test_text('app/tests/util/test_text.txt')
        yield
        # 테스트 파일 삭제
        delete_test_image('app/tests/util/test_image.jpg')
        delete_test_image('app/tests/util/test_image.svg')
        delete_test_text('app/tests/util/test_text.txt')
     
    @pytest.fixture
    def test_session(self):
        return next(get_test_db())
    
    @pytest.fixture
    def image_repository(self, test_session) -> ImageRepository:
        return ImageRepository(test_session, Image, ImageOutput)

    @pytest.fixture
    def processing_log_repository(self, test_session) -> ProcessingLogRepository:
        return ProcessingLogRepository(test_session, ProcessingLog, ProcessingLogOutput)
    
    @pytest.fixture
    def image_service(self, image_repository, processing_log_repository) -> ImageService:
        return ImageService(image_repository, processing_log_repository)

    def test_check_image_type_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = [bytes_image]
            assert image_service.validate(payload)
        
    def test_check_image_type_fail(self, image_service: ImageService):
        with open('app/tests/util/test_text.txt', 'rb') as f:
            bytes_image = f.read()
            payload = [bytes_image]
            with pytest.raises(NotSupportedTypeException):
                image_service.validate(payload)

    def test_check_image_size_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = [bytes_image]
            assert image_service.validate(payload)

    def test_check_image_size_fail(self, image_service: ImageService, monkeypatch):
        monkeypatch.setattr('app.service.image.MAXIMUM_IMAGE_SIZE', 1024)
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = [bytes_image]
            with pytest.raises(OutOfAllowedSizeException):
                image_service.validate(payload)

    def test_check_image_count_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = [bytes_image, bytes_image, bytes_image]
            assert image_service.validate(payload)

    def test_check_image_count_fail(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = [bytes_image, bytes_image, bytes_image, bytes_image]
            with pytest.raises(OutOfAllowedCountException):
                image_service.validate(payload)

    def test_image_service_preprocessing_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            preprocessed_payload = image_service.preprocess(payload)

            assert preprocessed_payload is not None
            assert type(preprocessed_payload) == bytes

    def test_image_service_preprocessing_fail(self, image_service: ImageService):
        with open('app/tests/util/test_image.svg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            with pytest.raises(PreProcessingException):
                image_service.preprocess(payload)
        

    def test_image_service_processing_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            preprocessed_payload = image_service.preprocess(payload)
            processed_payload = image_service.process(preprocessed_payload)

            assert processed_payload is not None
            assert type(processed_payload) == bytes

    def test_image_service_processing_fail(self, image_service: ImageService):
        with open('app/tests/util/test_image.svg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            with pytest.raises(ProcessingException):
                image_service.process(payload)

    def test_image_service_upload_jpg_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            upload_url = image_service.upload(payload)

            assert upload_url is not None
            assert upload_url[-3:] == 'jpg'

    def test_image_service_upload_png_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.png', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            upload_url = image_service.upload(payload)

            assert upload_url is not None
            assert upload_url[-3:] == 'png'

    def test_image_service_upload_svg_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.svg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            upload_url = image_service.upload(payload)

            assert upload_url is not None
            assert upload_url[-3:] == 'svg'

    def test_image_service_upload_fail(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            with pytest.raises(UploadException):
                image_service.upload(payload)

    def test_image_service_save(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            upload_url = image_service.upload(payload)
            
            save_result = image_service.save(upload_url, payload)
            
            assert save_result.id is not None
            assert save_result.original_url == upload_url
            assert save_result.svg_url is None
            assert save_result.status == ImageProcessingType.READY


    def test_image_service_update_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image
            
            # preprocessing
            preprocessed_payload = image_service.preprocess(payload)
            preprocessed_url = image_service.upload(preprocessed_payload)
            # save preprocessed image
            preprocessed_result = image_service.save(preprocessed_url, preprocessed_payload)
            # logging preprocessed image
            log_payload = ProcessingLogInput(original_id=preprocessed_result.id, status=ImageProcessingType.READY, description='test')
            image_service.save_log(log_payload)

            # processing
            log_payload = ProcessingLogInput(original_id=preprocessed_result.id, status=ImageProcessingType.PROCESSING, description='test')
            processed_payload = image_service.process(preprocessed_payload)
            processed_url = image_service.upload(processed_payload)
            # save processed(svg) image
            processed_result = image_service.update(preprocessed_result.id, processed_url)
            # logging processed(svg) image
            log_payload = ProcessingLogInput(original_id=processed_result.id, status=ImageProcessingType.COMPLETED, description='test')
            image_service.save_log(log_payload)

            # check result
            result = image_service.get(preprocessed_result.id)
            assert result.id is not None
            assert result.original_url == preprocessed_url
            assert result.svg_url == processed_url
            assert result.status == ImageProcessingType.COMPLETED

    def test_image_service_get_all(self, image_service: ImageService):
        # 이미지 3개 생성 후 limit 2, offset 0, 1로 각각 조회
        # total 3, limit 2, offset 0 -> 2개 조회
        # total 3, limit 2, offset 1 -> 1개 조회

        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            # 이미지 3개 생성
            for _ in range(3):
                preprocessed_payload = image_service.preprocess(payload)
                preprocessed_url = image_service.upload(preprocessed_payload)
                preprocessed_result = image_service.save(preprocessed_url, preprocessed_payload)
                log_payload = ProcessingLogInput(original_id=preprocessed_result.id, status=ImageProcessingType.READY, description='test')
                image_service.save_log(log_payload)
                processed_payload = image_service.process(preprocessed_payload)
                processed_url = image_service.upload(processed_payload)
                processed_result = image_service.update(preprocessed_result.id, processed_url)
                log_payload = ProcessingLogInput(original_id=processed_result.id, status=ImageProcessingType.COMPLETED, description='test')
                image_service.save_log(log_payload)

            # limit 2, offset 0
            result = image_service.get_all(2, 0)
            assert len(result) == 2

            # limit 2, offset 1
            result = image_service.get_all(2, 1)
            assert len(result) == 1
