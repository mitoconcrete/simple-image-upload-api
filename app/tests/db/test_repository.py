import uuid

import pytest

from app.db.models import Image, ProcessingLog, SVGImage
from app.db.repositories import image_repository, processing_log_repository, svg_image_repository


class TestRepository:
    #매 함수가 종료될 때마다 새로운 데이터베이스를 생성하고 삭제
    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        image_repository.delete_all(Image)
        svg_image_repository.delete_all(SVGImage)
        processing_log_repository.delete_all(ProcessingLog)
        yield
        image_repository.delete_all(Image)
        svg_image_repository.delete_all(SVGImage)
        processing_log_repository.delete_all(ProcessingLog)

    def test_create_image(self):
        id = uuid.uuid4()
        simple_image = Image(id=id, label='test', url='test')
        image_repository.add(simple_image)
        image = image_repository.get(Image, id)

        assert image.label == 'test'
        assert image.url == 'test'        

    def test_create_svg_image(self):
        image_id = uuid.uuid4()
        svg_image_id = uuid.uuid4()

        image = Image(id=image_id, label='test', url='test')
        image_repository.add(image)

        svg_image = SVGImage(id=svg_image_id, original_id=image_id, url="test2")
        svg_image_repository.add(svg_image)

        svg_image = svg_image_repository.get(SVGImage, svg_image_id)
        
        assert svg_image.image.id == image_id
        assert svg_image.id == svg_image_id
        assert svg_image.url == "test2"
        assert svg_image.original_id == image_id


    def test_create_processing_log(self):
        image_id = uuid.uuid4()
        svg_image_id = uuid.uuid4()
        processing_log_id = uuid.uuid4()

        image = Image(id=image_id, label='test', url='test')
        image_repository.add(image)

        svg_image = SVGImage(id=svg_image_id, original_id=image_id, url="test2")
        svg_image_repository.add(svg_image)

        processing_log = ProcessingLog(id=processing_log_id, image_id=svg_image_id, status='processing', description='test')
        processing_log_repository.add(processing_log)

        processing_log = processing_log_repository.get(ProcessingLog, processing_log_id)

        assert processing_log.image_id == svg_image_id
        assert processing_log.id == processing_log_id
        assert processing_log.status == 'processing'
        assert processing_log.description == 'test'

    def test_list_images(self):        
        image_id = uuid.uuid4()
        image = Image(id=image_id, label='test', url='test')
        image2 = Image(id=uuid.uuid4(), label='test2', url='test2')
        image_repository.add(image)
        image_repository.add(image2)

        images = image_repository.list(Image)
        assert len(images) == 2
        assert images[0].label == 'test'
        assert images[0].url == 'test'
        assert images[1].label == 'test2'
        assert images[1].url == 'test2'

    def test_list_svg_images(self):
        image_id = uuid.uuid4()
        svg_image_id = uuid.uuid4()

        image = Image(id=image_id, label='test', url='test')
        image_repository.add(image)

        svg_image = SVGImage(id=svg_image_id, original_id=image_id, url="test2")
        svg_image2 = SVGImage(id=uuid.uuid4(), original_id=image_id, url="test3")
        svg_image_repository.add(svg_image)
        svg_image_repository.add(svg_image2)

        svg_images = svg_image_repository.list(SVGImage)
        assert len(svg_images) == 2
        assert svg_images[0].url == 'test2'
        assert svg_images[1].url == 'test3'

    def test_list_processing_logs(self):
        image_id = uuid.uuid4()
        svg_image_id = uuid.uuid4()
        processing_log_id = uuid.uuid4()

        image = Image(id=image_id, label='test', url='test')
        image_repository.add(image)

        svg_image = SVGImage(id=svg_image_id, original_id=image_id, url="test2")
        svg_image_repository.add(svg_image)

        processing_log = ProcessingLog(id=processing_log_id, image_id=svg_image_id, status='processing', description='test')
        processing_log2 = ProcessingLog(id=uuid.uuid4(), image_id=svg_image_id, status='processing', description='test2')
        processing_log_repository.add(processing_log)
        processing_log_repository.add(processing_log2)

        processing_logs = svg_image_repository.get_processing_logs(SVGImage, svg_image_id)
        assert len(processing_logs) == 2
        assert processing_logs[0].description == 'test'
        assert processing_logs[1].description == 'test2'
    
    def test_update_image(self):
        image_id = uuid.uuid4()
        image = Image(id=image_id, label='test', url='test')
        image_repository.add(image)

        image.label = 'test2'
        image.url = 'test3'
        image_repository.update(image)

        image = image_repository.get(Image, image_id)
        assert image.label == 'test2'
        assert image.url == 'test3'

    def test_update_svg_image(self):
        image_id = uuid.uuid4()
        svg_image_id = uuid.uuid4()

        image = Image(id=image_id, label='test', url='test')
        image_repository.add(image)

        svg_image = SVGImage(id=svg_image_id, original_id=image_id, url="test2")
        svg_image_repository.add(svg_image)

        svg_image.url = 'test3'
        svg_image_repository.update(svg_image)

        svg_image = svg_image_repository.get(SVGImage, svg_image_id)
        assert svg_image.url == 'test3'

    def test_update_processing_log(self):
        image_id = uuid.uuid4()
        svg_image_id = uuid.uuid4()
        processing_log_id = uuid.uuid4()

        image = Image(id=image_id, label='test', url='test')
        image_repository.add(image)

        svg_image = SVGImage(id=svg_image_id, original_id=image_id, url="test2")
        svg_image_repository.add(svg_image)

        processing_log = ProcessingLog(id=processing_log_id, image_id=svg_image_id, status='processing', description='test')
        processing_log_repository.add(processing_log)

        processing_log.status = 'done'
        processing_log_repository.update(processing_log)

        processing_log = processing_log_repository.get(ProcessingLog, processing_log_id)
        assert processing_log.status == 'done'

    def test_delete_image(self):
        image_id = uuid.uuid4()
        image = Image(id=image_id, label='test', url='test')
        image_repository.add(image)

        image_repository.delete(image)
        image = image_repository.get(Image, image_id)
        assert image is None

    def test_delete_svg_image(self):
        image_id = uuid.uuid4()
        svg_image_id = uuid.uuid4()

        image = Image(id=image_id, label='test', url='test')
        image_repository.add(image)

        svg_image = SVGImage(id=svg_image_id, original_id=image_id, url="test2")
        svg_image_repository.add(svg_image)

        svg_image_repository.delete(svg_image)
        svg_image = svg_image_repository.get(SVGImage, svg_image_id)
        assert svg_image is None

    def test_delete_processing_log(self):
        image_id = uuid.uuid4()
        svg_image_id = uuid.uuid4()
        processing_log_id = uuid.uuid4()

        image = Image(id=image_id, label='test', url='test')
        image_repository.add(image)

        svg_image = SVGImage(id=svg_image_id, original_id=image_id, url="test2")
        svg_image_repository.add(svg_image)

        processing_log = ProcessingLog(id=processing_log_id, image_id=svg_image_id, status='processing', description='test')
        processing_log_repository.add(processing_log)

        processing_log_repository.delete(processing_log)
        processing_log = processing_log_repository.get(ProcessingLog, processing_log_id)
        assert processing_log is None

    def test_delete_image_cascade(self):
        image_id = uuid.uuid4()
        svg_image_id = uuid.uuid4()
        processing_log_id = uuid.uuid4()

        image = Image(id=image_id, label='test', url='test')
        image_repository.add(image)

        svg_image = SVGImage(id=svg_image_id, original_id=image_id, url="test2")
        svg_image_repository.add(svg_image)

        processing_log = ProcessingLog(id=processing_log_id, image_id=svg_image_id, status='processing', description='test')
        processing_log_repository.add(processing_log)

        # when
        image_repository.delete(image)

        image = image_repository.get(Image, image_id)
        svg_image = svg_image_repository.get(SVGImage, svg_image_id)
        processing_log = processing_log_repository.get(ProcessingLog, processing_log_id)

        # then
        assert image is None
        assert svg_image is None
        assert processing_log is None