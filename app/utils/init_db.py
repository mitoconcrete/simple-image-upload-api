from app.config.database import engine
from app.model.image import SVG, Image, ProcessingLog


def create_tables():
    for model in [Image, SVG, ProcessingLog]:
        model.metadata.create_all(engine)
