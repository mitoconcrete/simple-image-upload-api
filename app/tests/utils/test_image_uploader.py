import uuid

import pytest

from app.tests.helper import create_test_image, create_test_svg, delete_test_bucket, delete_test_image
from app.utils import image_uploader


class TestImageUploader:
    @pytest.fixture(scope='class', autouse=True)
    def bucket_name(self) -> str:
        return 'th.kim-test-bucket'

    @pytest.fixture(scope='class', autouse=True)
    def setup_and_teardown(self):
        # 테스트 이미지 파일 생성
        create_test_image('app/tests/utils/test_image.jpg', 'JPEG')
        create_test_image('app/tests/utils/test_image.png', 'PNG')
        create_test_svg('app/tests/utils/test_image.svg')
        yield
        # 테스트 이미지 파일 삭제
        delete_test_image('app/tests/utils/test_image.jpg')
        delete_test_image('app/tests/utils/test_image.png')
        delete_test_image('app/tests/utils/test_image.svg')
        delete_test_bucket('th.kim-test-bucket')

    def test_upload_jpg_image(self, bucket_name):
        image_key = f'{uuid.uuid4()}.jpg'
        with open('app/tests/utils/test_image.jpg', 'rb') as f:
            image_data = f.read()
        image_url = image_uploader.upload(bucket_name, image_key, image_data)
        assert image_url is not None

    def test_upload_png_image(self, bucket_name):
        image_key = f'{uuid.uuid4()}.png'
        with open('app/tests/utils/test_image.png', 'rb') as f:
            image_data = f.read()
        image_url = image_uploader.upload(bucket_name, image_key, image_data)
        assert image_url is not None

    def test_upload_svg(self, bucket_name):
        image_key = f'{uuid.uuid4()}.svg'
        with open('app/tests/utils/test_image.svg', 'rb') as f:
            image_data = f.read()
        image_url = image_uploader.upload(bucket_name, image_key, image_data)
        assert image_url is not None
