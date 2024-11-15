import pytest

from app.schemas.request_dto import ImageUploadServiceRequestDto
from app.services.image_service import _is_allowed_image_size, _is_allowed_image_type
from app.tests.helper import create_test_image, create_test_svg, create_test_text, delete_test_image, delete_test_text


class TestImageService:
    @pytest.fixture(scope='class', autouse=True)
    def setup_and_teardown(self):
        # 테스트 파일 생성
        create_test_image('app/tests/utils/test_image.jpg', 'JPEG')
        create_test_image('app/tests/utils/test_big_image.jpg', 'JPEG', 80_000, 80_000)
        create_test_svg('app/tests/utils/test_image.svg')
        create_test_text('app/tests/utils/test_text.txt')
        yield
        # 테스트 파일 삭제
        delete_test_image('app/tests/utils/test_image.jpg')
        delete_test_image('app/tests/utils/test_big_image.jpg')
        delete_test_image('app/tests/utils/test_image.svg')
        delete_test_text('app/tests/utils/test_text.txt')


    def test_check_image_type_success(self):
        with open('app/tests/utils/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            dto = ImageUploadServiceRequestDto(
                image=bytes_image,
                label='',
            )
            assert _is_allowed_image_type(dto)

    def test_check_image_type_fail(self):
        with open('app/tests/utils/test_text.txt', 'rb') as f:
            bytes_image = f.read()
            dto = ImageUploadServiceRequestDto(
                image=bytes_image,
                label='',
            )
            assert not _is_allowed_image_type(dto)

    def test_check_image_size_success(self):
        with open('app/tests/utils/test_image.jpg', 'rb') as f:
            bytes_image = f.read()
            dto = ImageUploadServiceRequestDto(
                image=bytes_image,
                label='',
            )
            assert _is_allowed_image_size(dto)

    def test_check_image_size_fail(self):
        with open('app/tests/utils/test_big_image.jpg', 'rb') as f:
            bytes_image = f.read()
            dto = ImageUploadServiceRequestDto(
                image=bytes_image,
                label='',
            )
            assert not _is_allowed_image_size(dto)

    def test_check_image_count_success(self):
        pass

    def test_check_image_count_fail(self):
        pass
    
    def test_upload_image_service(self):
        pass

    def test_upload_svg_image_service(self):
        pass

    def test_tracking_image_ready_status(self):
        pass

    def test_tracking_image_success_status(self):
        pass

    def test_tracking_image_processing_status(self):
        pass

    def test_tracking_image_fail_status(self):
        pass

    def test_get_image_list(self):
        pass