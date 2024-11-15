import pytest

from app.model.image import SVG, Image, ProcessingLog
from app.repository import image_repository, processing_log_repository, svg_repository
from app.schema.dao.image import ImageInput, ProcessingLogInput, SVGInput
from app.schema.enum.image import ImageProcessingType
from app.utils.init_db import create_tables


class TestRepository:
    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        create_tables()
        yield
        image_repository.delete_all()
        svg_repository.delete_all()
        processing_log_repository.delete_all()

    def test_create_image(self):
        new_image = Image(label='test', url='test')
        created_image = image_repository.add(new_image)

        assert created_image.id is not None

    def test_create_svg(self):
        new_image = Image(label='test', url='test')
        new_svg = SVG(url='test2')

        new_image.svg.append(new_svg)

        created_image = image_repository.add(new_image)
        created_svg = svg_repository.add(new_svg)

        retrieved_svg = svg_repository.get(created_svg.id)
        assert retrieved_svg.id == created_svg.id
        assert retrieved_svg.url == 'test2'
        assert retrieved_svg.original_id == created_image.id

    def test_create_processing_log(self):
        new_image = Image(label='test', url='test')
        new_processing_log = ProcessingLog(status='processing', description='test')

        new_image.processing_log.append(new_processing_log)

        created_image = image_repository.add(new_image)
        created_processing_log = processing_log_repository.add(new_processing_log)

        retrieved_processing_log = processing_log_repository.get(created_processing_log.id)

        assert retrieved_processing_log.original_id == created_image.id
        assert retrieved_processing_log.id == created_processing_log.id
        assert retrieved_processing_log.status == 'processing'
        assert retrieved_processing_log.description == 'test'

    def test_list_images(self):
        new_image01 = Image(label='test', url='test')
        new_image02 = Image(label='test2', url='test2')

        image_repository.add(new_image01)
        image_repository.add(new_image02)

        created_images = image_repository.get_all()
        assert len(created_images) == 2
        assert created_images[0].label == 'test'
        assert created_images[0].url == 'test'
        assert created_images[1].label == 'test2'
        assert created_images[1].url == 'test2'

    def test_list_processing_logs(self):
        new_image = Image(label='test', url='test')
        new_processing_log1 = ProcessingLog(status='processing', description='test')
        new_processing_log2 = ProcessingLog(status='processing', description='test2')

        new_image.processing_log.append(new_processing_log1)
        new_image.processing_log.append(new_processing_log2)

        image_repository.add(new_image)
        processing_log_repository.add(new_processing_log1)
        processing_log_repository.add(new_processing_log2)

        processing_logs = image_repository.get_processing_logs(new_image.id)
        assert len(processing_logs) == 2

    def test_update_image(self):
        new_image = Image(label='test', url='test')
        created_image = image_repository.add(new_image)

        update_data = ImageInput(label='test2', url='test3')
        image_repository.update(created_image.id, update_data)

        retrieved_image = image_repository.get(created_image.id)

        assert retrieved_image.label == 'test2'
        assert retrieved_image.url == 'test3'

    def test_update_svg(self):
        new_image = Image(label='test', url='test')
        new_svg = SVG(url='test2')

        new_image.svg.append(new_svg)

        image_repository.add(new_image)
        created_svg = svg_repository.add(new_svg)

        update_data = SVGInput(url='test3', original_id=new_image.id)
        svg_repository.update(created_svg.id, update_data)

        retrieved_svg = svg_repository.get(created_svg.id)
        assert retrieved_svg.url == 'test3'

    def test_update_processing_log(self):
        new_image = Image(label='test', url='test')
        new_processing_log = ProcessingLog(status=ImageProcessingType.FAILED, description='test')

        new_image.processing_log.append(new_processing_log)

        image_repository.add(new_image)
        created_processing_log = processing_log_repository.add(new_processing_log)

        update_data = ProcessingLogInput(status=ImageProcessingType.COMPLETED, description='test')
        processing_log_repository.update(created_processing_log.id, update_data)

        retrieved_processing_log = processing_log_repository.get(created_processing_log.id)
        assert retrieved_processing_log.status == ImageProcessingType.COMPLETED

    def test_delete_image(self):
        new_image = Image(label='test', url='test')

        created_image = image_repository.add(new_image)

        image_repository.delete(created_image.id)

        retrieved_image = image_repository.get(created_image.id)
        assert retrieved_image is None

    def test_delete_svg(self):
        new_image = Image(label='test', url='test')
        new_svg = SVG(url='test2')

        new_image.svg.append(new_svg)

        image_repository.add(new_image)
        created_svg = svg_repository.add(new_svg)

        svg_repository.delete(created_svg.id)

        retrieved_svg = svg_repository.get(created_svg.id)
        assert retrieved_svg is None

    def test_delete_processing_log(self):
        new_image = Image(label='test', url='test')
        new_processing_log = ProcessingLog(status='processing', description='test')

        new_image.processing_log.append(new_processing_log)

        image_repository.add(new_image)
        created_processing_log = processing_log_repository.add(new_processing_log)

        processing_log_repository.delete(created_processing_log.id)
        retrieved_processing_log = processing_log_repository.get(created_processing_log.id)
        assert retrieved_processing_log is None

    def test_delete_image_cascade(self):
        new_image = Image(label='test', url='test')
        new_svg = SVG(url='test2')
        new_processing_log = ProcessingLog(status='processing', description='test')

        new_image.svg.append(new_svg)
        new_image.processing_log.append(new_processing_log)

        created_image = image_repository.add(new_image)
        created_svg = svg_repository.add(new_svg)
        created_processing_log = processing_log_repository.add(new_processing_log)

        image_repository.delete(created_image.id)

        assert image_repository.get(created_image.id) is None
        assert svg_repository.get(created_svg.id) is None
        assert processing_log_repository.get(created_processing_log.id) is None
