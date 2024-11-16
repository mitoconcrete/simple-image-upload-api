import logging
import os

from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.model.image import SVG, ProcessingLog
from app.model.image import Image as ImageModel
from app.util.s3_uploder import S3Uploader


# 테스트 이미지 파일(jpg, png) 생성
def create_test_image(image_path: str, image_format: str):
    image = Image.new('RGB', (1000, 1000))
    image.save(image_path, image_format)


# 테스트 이미지 파일(svg) 생성
def create_test_svg(svg_path: str):
    svg = """<svg width="100" height="100">
    <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
    </svg>"""
    with open(svg_path, 'w') as f:
        f.write(svg)


# 테스트 텍스트 파일 생성
def create_test_text(text_path: str):
    text = 'test text'
    with open(text_path, 'w') as f:
        f.write(text)


# 테스트 이미지 파일 삭제
def delete_test_image(image_path: str):
    os.remove(image_path)


def delete_test_text(text_path: str):
    os.remove(text_path)


# 테스트 버킷 삭제
def delete_test_bucket(bucket_name: str):
    s3_uploader = S3Uploader()
    s3_uploader.delete_bucket(bucket_name)
    logging.info(f'{bucket_name} is deleted')


# 테스트 용 DB session을 생성
def get_test_db():
    # 1. 테스트용 SQLite DB 생성
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
    )

    # 2. 테스트용 SQLite DB session 생성
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    db = SessionLocal()

    # 3. 테스트용 테이블 생성
    for model in [ImageModel, SVG, ProcessingLog]:
        model.metadata.create_all(engine)

    # 4. 테스트용 DB session 반환
    try:
        yield db
    finally:
        db.close()
