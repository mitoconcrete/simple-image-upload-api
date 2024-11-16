import pytest

from app.tests.helper import create_test_image, create_test_svg, create_test_text, delete_test_image, delete_test_text


class ImageServiceTest:
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

    # def test_
