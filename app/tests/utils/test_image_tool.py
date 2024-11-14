import pytest

from PIL import Image
from io import BytesIO

from app.utils.image_tool import basic_image_preprocessor, is_image_type_jpg_or_png, _svg_optimizer, _image_to_svg
from app.tests.helper import create_test_image, create_test_svg, create_test_text, delete_test_image, delete_test_text

class TestImageTools:
    @pytest.fixture(scope='class', autouse=True)
    def setup_and_teardown(self):
        # 테스트 파일 생성
        create_test_image('app/tests/utils/test_image.jpg', 'JPEG')
        create_test_image('app/tests/utils/test_image.png', 'PNG')
        create_test_svg('app/tests/utils/test_image.svg')
        create_test_text('app/tests/utils/test_text.txt')
        yield
        # 테스트 파일 삭제
        delete_test_image('app/tests/utils/test_image.jpg')
        delete_test_image('app/tests/utils/test_image.png')
        delete_test_image('app/tests/utils/test_image.svg')
        delete_test_text('app/tests/utils/test_text.txt')

    def test_image_type_checker(self):
        with open('app/tests/utils/test_image.jpg', 'rb') as f:
            image_data = f.read()
            assert is_image_type_jpg_or_png(image_data) == True

        with open('app/tests/utils/test_image.png', 'rb') as f:
            image_data = f.read()
            assert is_image_type_jpg_or_png(image_data) == True

        with open('app/tests/utils/test_image.svg', 'rb') as f:
            image_data = f.read()
            assert is_image_type_jpg_or_png(image_data) == False

        with open('app/tests/utils/test_text.txt', 'rb') as f:
            text_data = f.read()
            assert is_image_type_jpg_or_png(text_data) == False

    def test_jpg_image_preprocess(self):
        with open('app/tests/utils/test_image.jpg', 'rb') as f:
            image_data = f.read()
            # 이미지 데이터의 사이즈를 체크하고, 가로 세로가 // 2로 리사이즈 되었는지 확인합니다.
            width, height = Image.open(BytesIO(image_data)).size
            processed_image = basic_image_preprocessor(image_data)
             
            after_width, after_height = Image.open(BytesIO(processed_image)).size
            assert processed_image is not None
            assert max(width // 2, 100) == after_width
            assert max(height // 2, 100) == after_height


    def test_png_image_preprocess(self):
        with open('app/tests/utils/test_image.png', 'rb') as f:
            image_data = f.read()
            # 이미지 데이터의 사이즈를 체크하고, 가로 세로가 // 2로 리사이즈 되었는지 확인합니다.
            width, height = Image.open(BytesIO(image_data)).size
            processed_image = basic_image_preprocessor(image_data)
             
            after_width, after_height = Image.open(BytesIO(processed_image)).size
            assert processed_image is not None
            assert max(width // 2, 100) == after_width
            assert max(height // 2, 100) == after_height

    def test_jpg_image_to_svg(self):
        with open('app/tests/utils/test_image.jpg', 'rb') as f:
            image_data = f.read()
            svg_image = _image_to_svg(image_data)
            assert is_image_type_jpg_or_png(svg_image) == False
    
    def test_png_image_to_svg(self):
        with open('app/tests/utils/test_image.png', 'rb') as f:
            image_data = f.read()
            svg_image = _image_to_svg(image_data)
            assert is_image_type_jpg_or_png(svg_image) == False

    def test_svg_optimizer(self):
        with open('app/tests/utils/test_image.svg', 'rb') as f:
            image_data = f.read()
            optimized_image = _svg_optimizer(image_data)
            assert optimized_image is not None

