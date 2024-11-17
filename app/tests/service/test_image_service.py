import pytest

from app.exception.image import (
    NotSupportedTypeException,
    OutOfAllowedCountException,
    OutOfAllowedSizeException,
    PreProcessImageException,
    ProcessImageException,
    SaveException,
    UploadException,
)
from app.schema.dto.image import ImageServiceOutput, SaveLogInput
from app.schema.enum.image import ImageProcessingType
from app.service.image import ImageService
from app.tests.helper import (
    create_test_image,
    create_test_svg,
    create_test_text,
    delete_test_image,
    delete_test_text,
)
from app.util.image_util import create_save_path, get_image_format


class TestImageService:
    @pytest.fixture(scope='class', autouse=True)
    def setup_and_teardown(self):
        # 테스트 파일 생성
        create_test_image('app/tests/util/test_image.jpg', 'JPEG')
        create_test_image('app/tests/util/test_image.png', 'PNG')
        create_test_svg('app/tests/util/test_image.svg')
        create_test_text('app/tests/util/test_text.txt')
        yield
        # 테스트 파일 삭제
        delete_test_image('app/tests/util/test_image.jpg')
        delete_test_image('app/tests/util/test_image.png')
        delete_test_image('app/tests/util/test_image.svg')
        delete_test_text('app/tests/util/test_text.txt')

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
            assert type(preprocessed_payload) is bytes

    def test_image_service_preprocessing_fail(self, image_service: ImageService):
        with open('app/tests/util/test_image.svg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            with pytest.raises(PreProcessImageException):
                image_service.preprocess(payload)

    def test_image_service_processing_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            preprocessed_payload = image_service.preprocess(payload)
            processed_payload = image_service.process(preprocessed_payload)

            assert processed_payload is not None
            assert type(processed_payload) is bytes
            assert processed_payload[:4] == b'<svg'

    def test_image_service_processing_fail(self, image_service: ImageService):
        with open('app/tests/util/test_image.svg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            with pytest.raises(ProcessImageException):
                image_service.process(payload)

    def test_image_service_upload_jpg_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            image_type = get_image_format(payload)
            file_name = create_save_path(image_type)
            upload_url = image_service.upload(file_name, payload)

            assert upload_url is not None
            assert type(upload_url) is str
            assert upload_url[-4:] == 'jpeg'

    def test_image_service_upload_png_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.png', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            image_type = get_image_format(payload)
            file_name = create_save_path(image_type)
            upload_url = image_service.upload(file_name, payload)

            assert upload_url is not None
            assert type(upload_url) is str
            assert upload_url[-3:] == 'png'

    def test_image_service_upload_svg_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.svg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            file_name = create_save_path('svg')
            upload_url = image_service.upload(file_name, payload)

            assert upload_url is not None
            assert type(upload_url) is str
            assert upload_url[-3:] == 'svg'

    def test_image_service_upload_fail(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            with pytest.raises(UploadException):
                # 함수 중간에서 억지로 예외를 발생시키기 위해 file_name을 None으로 설정
                image_service.upload(payload)

    def test_image_service_save(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            payload_type = get_image_format(payload)
            name = create_save_path(payload_type)
            upload_url = image_service.upload(name, payload)

            save_result = image_service.save(upload_url)
            image_service.save_log(SaveLogInput(original_id=save_result.id, status=ImageProcessingType.READY))

            retrived_result = image_service.get(save_result.id)
            assert isinstance(save_result, ImageServiceOutput)
            assert retrived_result.id is not None
            assert retrived_result.original_url == upload_url
            assert retrived_result.svg_url is None
            assert retrived_result.status == ImageProcessingType.READY

    def test_image_service_save_fail(self, image_service: ImageService):
        with pytest.raises(SaveException):
            image_service.save(None)

    def test_image_service_save_log_fail(self, image_service: ImageService):
        with pytest.raises(SaveException):
            image_service.save_log(None)

    def test_image_service_update_success(self, image_service: ImageService):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            payload = bytes_image

            # preprocessing
            preprocessed_payload = image_service.preprocess(payload)
            preprocessed_payload_type = get_image_format(preprocessed_payload)
            preprocessed_url = create_save_path(preprocessed_payload_type)
            # save preprocessed image
            preprocessed_result = image_service.save(preprocessed_url)
            # logging preprocessed image
            log_payload = SaveLogInput(original_id=preprocessed_result.id, status=ImageProcessingType.READY)
            image_service.save_log(log_payload)

            # processing
            log_payload = SaveLogInput(original_id=preprocessed_result.id, status=ImageProcessingType.PROCESSING)
            processed_url = create_save_path('svg')
            # save processed(svg) image
            processed_result = image_service.update(preprocessed_result.id, processed_url)
            # logging processed(svg) image
            log_payload = SaveLogInput(original_id=processed_result.id, status=ImageProcessingType.COMPLETED)
            image_service.save_log(log_payload)

            # check result
            result = image_service.get(preprocessed_result.id)
            assert isinstance(result, ImageServiceOutput)
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
                preprocessed_payload_type = get_image_format(preprocessed_payload)
                preprocessed_url = create_save_path(preprocessed_payload_type)
                preprocessed_result = image_service.save(preprocessed_url)
                log_payload = SaveLogInput(original_id=preprocessed_result.id, status=ImageProcessingType.READY)

                image_service.save_log(log_payload)

                processed_url = create_save_path('svg')
                processed_result = image_service.update(preprocessed_result.id, processed_url)

                log_payload = SaveLogInput(original_id=processed_result.id, status=ImageProcessingType.COMPLETED)
                image_service.save_log(log_payload)

            # limit 2, offset 0
            result = image_service.get_all(2, 0)
            assert result.total == 3
            assert result.page == 0
            assert len(result.items) == 2

            # limit 2, offset 1
            result = image_service.get_all(2, 1)
            assert result.total == 3
            assert result.page == 1
            assert len(result.items) == 1

            # limit 2, offset 2
            result = image_service.get_all(2, 2)
            assert result.total == 3
            assert result.page == 2
            assert len(result.items) == 0
