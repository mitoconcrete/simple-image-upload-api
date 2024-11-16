from app.config.database import engine
from app.model.image import Image, ProcessingLog


def create_tables():
    for model in [Image, ProcessingLog]:
        model.metadata.create_all(engine)
