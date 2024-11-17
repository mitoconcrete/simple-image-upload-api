import uuid

import pytest
from fastapi.testclient import TestClient

from app.schema.enum.exception import ErrorType
from app.tests.helper import create_test_image, create_test_text, delete_test_image, delete_test_text


class TestImageRouter:
    @pytest.fixture(scope='class', autouse=True)
    def setup_and_teardown(self):
        create_test_image('app/tests/util/test_image.jpg', 'JPEG')
        create_test_text('app/tests/util/test_text.txt')
        yield
        # 테스트 파일 삭제
        delete_test_image('app/tests/util/test_image.jpg')
        delete_test_text('app/tests/util/test_text.txt')

    def test_get_image(self, client: TestClient):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            image_data = f.read()
            files = [('files', ('test_image.jpg', image_data, 'image/jpeg'))]
            post_response = client.post('/api/v1/images', files=files).json()
            get_response = client.get(f'/api/v1/images/{post_response[0]["id"]}')

            assert get_response.status_code == 200
            assert set(get_response.json().keys()) == {'id', 'original_url', 'svg_url', 'status', 'created_at'}

    def test_get_image_fail_not_found(self, client: TestClient):
        response = client.get(f'/api/v1/images/{uuid.uuid4()}')
        assert response.status_code == 404
        assert response.json()['error_code'] == ErrorType.CONTENTS_NOT_FOUND.value[0]
        assert response.json()['message'] == ErrorType.CONTENTS_NOT_FOUND.value[1]

    def test_get_images(self, client: TestClient):
        # 3개의 이미지를 multipart/form-data로 한번에 전송합니다.
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            image_data = f.read()
            files = [
                ('files', ('test_image01.jpg', image_data, 'image/jpeg')),
                ('files', ('test_image02.jpg', image_data, 'image/jpeg')),
                ('files', ('test_image03.jpg', image_data, 'image/jpeg')),
            ]
            client.post('/api/v1/images', files=files)

            # page, limit을 이용하여 페이징을 테스트합니다.
            page1_response = client.get('/api/v1/images?page=0&limit=2')
            assert page1_response.status_code == 200
            assert page1_response.json()['total'] == 3
            assert len(page1_response.json()['items']) == 2

            page2_response = client.get('/api/v1/images?page=1&limit=2')
            assert page2_response.status_code == 200
            assert page1_response.json()['total'] == 3
            assert len(page2_response.json()['items']) == 1

            page3_response = client.get('/api/v1/images?page=2&limit=2')
            assert page3_response.status_code == 200
            assert page1_response.json()['total'] == 3
            assert len(page3_response.json()['items']) == 0

    def test_post_image(self, client: TestClient):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            image_data = f.read()
            files = [('files', ('test_image.jpg', image_data, 'image/jpeg'))]

            response = client.post('/api/v1/images', files=files)
            assert response.status_code == 200
            assert set(response.json()[0].keys()) == {'id', 'original_url', 'status'}

    def test_post_image_fail_invalid_image_type(self, client: TestClient):
        # 텍스트 파일을 전송하여 이미지 타입이 아닌 경우를 테스트합니다.
        with open('app/tests/util/test_text.txt', 'rb') as f:
            text_data = f.read()
            files = [('files', ('test_text.txt', text_data, 'text/plain'))]

            response = client.post('/api/v1/images', files=files)
            assert response.status_code == 400
            assert response.json()['error_code'] == ErrorType.INVALID_IMAGE_TYPE.value[0]
            assert response.json()['message'] == ErrorType.INVALID_IMAGE_TYPE.value[1]

    def test_post_image_fail_invalid_image_size(self, client: TestClient, monkeypatch):
        monkeypatch.setattr('app.service.image.MAXIMUM_IMAGE_SIZE', 1024)
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            image_data = f.read()
            # 10MB 이상의 이미지를 전송하여 이미지 사이즈가 초과된 경우를 테스트합니다.
            files = [('files', ('test_image.jpg', image_data, 'image/jpeg'))]

            response = client.post('/api/v1/images', files=files)
            assert response.status_code == 400
            assert response.json()['error_code'] == ErrorType.INVALID_IMAGE_SIZE.value[0]
            assert response.json()['message'] == ErrorType.INVALID_IMAGE_SIZE.value[1]

    def test_post_image_fail_invalid_image_count(self, client: TestClient):
        with open('app/tests/util/test_image.jpg', 'rb') as f:
            image_data = f.read()
            # 4개의 이미지를 전송하여 이미지 개수가 초과된 경우를 테스트합니다.
            files = [
                ('files', ('test_image01.jpg', image_data, 'image/jpeg')),
                ('files', ('test_image02.jpg', image_data, 'image/jpeg')),
                ('files', ('test_image03.jpg', image_data, 'image/jpeg')),
                ('files', ('test_image04.jpg', image_data, 'image/jpeg')),
            ]

            response = client.post('/api/v1/images', files=files)
            assert response.status_code == 400
            assert response.json()['error_code'] == ErrorType.OUT_OF_ALLOWED_MAXIMUM_COUNT.value[0]
            assert response.json()['message'] == ErrorType.OUT_OF_ALLOWED_MAXIMUM_COUNT.value[1]
