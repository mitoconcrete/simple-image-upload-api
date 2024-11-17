import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.config.database import get_db
from app.main import app
from app.model.image import Image, ProcessingLog
from app.repository.image import ImageRepository, ProcessingLogRepository
from app.schema.dao.image import ImageOutput, ProcessingLogOutput
from app.service.image import ImageService


@pytest.fixture
def test_db():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    for model in [Image, ProcessingLog]:
        model.metadata.create_all(engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.rollback()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def image_repository(test_db) -> ImageRepository:
    return ImageRepository(test_db, Image, ImageOutput)


@pytest.fixture
def processing_log_repository(test_db) -> ProcessingLogRepository:
    return ProcessingLogRepository(test_db, ProcessingLog, ProcessingLogOutput)


@pytest.fixture
def image_service(image_repository, processing_log_repository) -> ImageService:
    return ImageService(image_repository, processing_log_repository)
