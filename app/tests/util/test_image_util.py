from io import BytesIO

import pytest
from PIL import Image

from app.tests.helper import create_test_image, create_test_svg, create_test_text, delete_test_image, delete_test_text
from app.util.image_util import (
    convert_image_to_svg as _image_to_svg,
)
from app.util.image_util import (
    create_save_path,
    get_image_size,
)
from app.util.image_util import (
    is_jpg_or_png as is_image_type_jpg_or_png,
)
from app.util.image_util import (
    preprocess_image as basic_image_preprocessor,
)


class TestImageTools:
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

    def test_image_type_checker(self):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            image_data = f.read()
            assert is_image_type_jpg_or_png(image_data)

        with open('app/tests/util/test_image.png', 'rb') as f:
            image_data = f.read()
            assert is_image_type_jpg_or_png(image_data)

        with open('app/tests/util/test_image.svg', 'rb') as f:
            image_data = f.read()
            assert not is_image_type_jpg_or_png(image_data)

        with open('app/tests/util/test_text.txt', 'rb') as f:
            text_data = f.read()
            assert not is_image_type_jpg_or_png(text_data)

    def test_jpg_image_preprocess(self):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            image_data = f.read()
            # 이미지 데이터의 사이즈를 체크하고, 가로 세로가 // 2로 리사이즈 되었는지 확인합니다.
            width, height = Image.open(BytesIO(image_data)).size
            processed_image = basic_image_preprocessor(image_data)

            after_width, after_height = Image.open(BytesIO(processed_image)).size
            assert processed_image is not None
            assert max(width // 2, 100) == after_width
            assert max(height // 2, 100) == after_height

    def test_png_image_preprocess(self):
        with open('app/tests/util/test_image.png', 'rb') as f:
            image_data = f.read()
            # 이미지 데이터의 사이즈를 체크하고, 가로 세로가 // 2로 리사이즈 되었는지 확인합니다.
            width, height = Image.open(BytesIO(image_data)).size
            processed_image = basic_image_preprocessor(image_data)

            after_width, after_height = Image.open(BytesIO(processed_image)).size
            assert processed_image is not None
            assert max(width // 2, 100) == after_width
            assert max(height // 2, 100) == after_height

    def test_jpg_image_to_svg(self):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            image_data = f.read()
            svg = _image_to_svg(image_data)
            assert not is_image_type_jpg_or_png(svg)

    def test_png_image_to_svg(self):
        with open('app/tests/util/test_image.png', 'rb') as f:
            image_data = f.read()
            svg = _image_to_svg(image_data)
            assert not is_image_type_jpg_or_png(svg)

    def test_image_size_checker(self):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            image_data = f.read()
            image_size = get_image_size(image_data)
            assert image_size < 5 * 1024 * 1024

    def test_create_save_path(self):
        jpg_path = create_save_path('jpg')
        jpeg_path = create_save_path('jpeg')
        png_path = create_save_path('png')
        svg_path = create_save_path('svg')

        assert jpg_path.startswith('JPG')
        assert jpeg_path.startswith('JPEG')
        assert png_path.startswith('PNG')
        assert svg_path.startswith('SVG')

        assert jpg_path.endswith('.jpg')
        assert jpeg_path.endswith('.jpeg')
        assert png_path.endswith('.png')
        assert svg_path.endswith('.svg')
