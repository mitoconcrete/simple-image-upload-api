import uuid

import pytest

from app.db.models import Image, ProcessingLog, SVG
from app.db.repositories import image_repository, processing_log_repository, svg_repository


class TestRepository:
    # 매 함수가 종료될 때마다 새로운 데이터베이스를 생성하고 삭제
    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        image_repository.delete_all(Image)
        svg_repository.delete_all(SVG)
        processing_log_repository.delete_all(ProcessingLog)
        yield
        image_repository.delete_all(Image)
        svg_repository.delete_all(SVG)
        processing_log_repository.delete_all(ProcessingLog)

    def test_create_image(self):
        image = Image(label='test', url='test')
        image_id = image_repository.add(image)

        assert image_id is not None

    def test_create_svg(self):
        new_image = Image(label='test', url='test')
        new_svg = SVG(url='test2')

        new_image.svg.append(new_svg)

        created_image_id = image_repository.add(new_image)
        created_svg_id = svg_repository.add(new_svg)

        svg = svg_repository.get(SVG, created_svg_id)
        assert svg.image.id == created_image_id
        assert svg.id == created_svg_id
        assert svg.url == 'test2'
        assert svg.original_id == created_image_id

    def test_create_processing_log(self):
        image = Image(label='test', url='test')
        processing_log = ProcessingLog(
            status='processing', description='test'
        )

        image.processing_log.append(processing_log)

        image_id = image_repository.add(image)
        processing_log_id = processing_log_repository.add(processing_log)

        processing_log = processing_log_repository.get(ProcessingLog, processing_log_id)

        assert processing_log.original_id == image_id
        assert processing_log.id == processing_log_id
        assert processing_log.status == 'processing'
        assert processing_log.description == 'test'

    def test_list_images(self):
        image = Image(label='test', url='test')
        image2 = Image(label='test2', url='test2')

        image_repository.add(image)
        image_repository.add(image2)

        images = image_repository.list(Image)
        assert len(images) == 2
        assert images[0].label == 'test'
        assert images[0].url == 'test'
        assert images[1].label == 'test2'
        assert images[1].url == 'test2'

    def test_list_processing_logs(self):
        image = Image(label='test', url='test')
        processing_log = ProcessingLog(
            status='processing', description='test'
        )
        processing_log2 = ProcessingLog(
            status='processing', description='test2'
        )

        image.processing_log.append(processing_log)
        image.processing_log.append(processing_log2)

        image_repository.add(image)
        processing_log_repository.add(processing_log)
        processing_log_repository.add(processing_log2)

        processing_logs = image_repository.get_processing_logs(Image, image.id)
        assert len(processing_logs) == 2
        assert processing_logs[0].description == 'test'
        assert processing_logs[1].description == 'test2'

    def test_update_image(self):
        image = Image(label='test', url='test')
        image_id = image_repository.add(image)

        image.label = 'test2'
        image.url = 'test3'
        image_repository.update(image)

        image = image_repository.get(Image, image_id)
        assert image.label == 'test2'
        assert image.url == 'test3'

    def test_update_svg(self):
        image = Image(label='test', url='test')
        svg = SVG(url='test2')
        
        image.svg.append(svg)
        
        image_repository.add(image)
        svg_id = svg_repository.add(svg)

        svg.url = 'test3'
        svg_repository.update(svg)

        svg = svg_repository.get(SVG, svg_id)
        assert svg.url == 'test3'

    def test_update_processing_log(self):
        image = Image(label='test', url='test')
        processing_log = ProcessingLog(
            status='processing', description='test'
        )

        image.processing_log.append(processing_log)

        image_repository.add(image)
        processing_log_id = processing_log_repository.add(processing_log)
        processing_log.status = 'done'
        processing_log_repository.update(processing_log)

        processing_log = processing_log_repository.get(ProcessingLog, processing_log_id)
        assert processing_log.status == 'done'

    def test_delete_image(self):
        image = Image(label='test', url='test')

        image_id = image_repository.add(image)
        
        image_repository.delete(image)
        
        image = image_repository.get(Image, image_id)
        assert image is None

    def test_delete_svg(self):
        image = Image(label='test', url='test')
        svg = SVG(url='test2')
        
        image.svg.append(svg)
         
        image_repository.add(image)
        svg_id = svg_repository.add(svg)

        svg_repository.delete(svg)

        svg = svg_repository.get(SVG, svg_id)
        assert svg is None

    def test_delete_processing_log(self):
        image = Image(label='test', url='test')
        processing_log = ProcessingLog(status='processing', description='test')

        image.processing_log.append(processing_log)

        image_repository.add(image)
        processing_log_id = processing_log_repository.add(processing_log)

        processing_log_repository.delete(processing_log)
        processing_log = processing_log_repository.get(ProcessingLog, processing_log_id)
        assert processing_log is None

    def test_delete_image_cascade(self):
        image = Image(label='test', url='test')
        svg = SVG(url='test2')
        processing_log = ProcessingLog(status='processing', description='test')

        image.svg.append(svg)
        image.processing_log.append(processing_log)

        image_id = image_repository.add(image)
        svg_id = svg_repository.add(image)
        processing_log_id = processing_log_repository.add(image)

        image_repository.delete(image)

        assert image_repository.get(Image, image_id) is None
        assert svg_repository.get(SVG, svg_id) is None
        assert processing_log_repository.get(ProcessingLog, processing_log_id) is None