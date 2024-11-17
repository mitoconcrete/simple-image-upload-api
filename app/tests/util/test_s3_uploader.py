import pytest

from app.tests.helper import create_test_image, delete_test_bucket, delete_test_image
from app.util.s3_uploder import S3Uploader


class TestS3Uploader:
    @pytest.fixture(scope='class', autouse=True)
    def bucket_name(self) -> str:
        return 'th.kim.test.bucket'

    @pytest.fixture(scope='class', autouse=True)
    def s3_uploader(self) -> S3Uploader:
        return S3Uploader()

    @pytest.fixture(scope='class', autouse=True)
    def setup_and_teardown(self, bucket_name: str):
        create_test_image('app/tests/util/test_image.jpg', 'JPEG')
        yield
        # 테스트 이미지 파일 삭제
        delete_test_image('app/tests/util/test_image.jpg')
        delete_test_bucket(bucket_name)

    def test_create_bucket(self, s3_uploader: S3Uploader, bucket_name: str):
        s3_uploader.create_bucket(bucket_name)

        assert s3_uploader._has_bucket(bucket_name)

    def test_delete_bucket(self, s3_uploader: S3Uploader):
        delete_bucket_name = 'th.kim-delete-bucket'

        s3_uploader.create_bucket(delete_bucket_name)
        s3_uploader.delete_bucket(delete_bucket_name)

        assert not s3_uploader._has_bucket(delete_bucket_name)

    def test_upload_image(self, s3_uploader: S3Uploader, bucket_name: str):
        image_key = 'test_image.jpg'
        with open(f'app/tests/util/{image_key}', 'rb') as f:
            image_data = f.read()

            image_url = s3_uploader.upload_file(bucket_name, image_key, image_data)
            image_data = s3_uploader.download_file(bucket_name, image_key)

            assert image_url is not None
            assert image_data is not None

    def test_delete_image(self, s3_uploader: S3Uploader, bucket_name: str):
        image_key = 'test_image.jpg'

        s3_uploader.delete_file(bucket_name, image_key)

        assert not s3_uploader._has_file(bucket_name, image_key)
