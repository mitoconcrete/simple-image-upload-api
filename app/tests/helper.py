import logging
import os
from typing import Optional

from PIL import Image

from app.utils.s3_uploder import S3Uploader


# 테스트 이미지 파일(jpg, png) 생성
def create_test_image(image_path: str, image_format: str, width: Optional[int] = None, height: Optional[int] = None):
    width = width or 1000
    height = height or 1000
    image = Image.new('RGB', (width, height))
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
