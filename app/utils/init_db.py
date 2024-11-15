from app.config.database import engine
from app.model.image import Image, SVG, ProcessingLog

def create_tables():
    for model in [Image, SVG, ProcessingLog]:
        model.metadata.create_all(engine)