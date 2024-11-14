import logging
import os
from PIL import Image

from app.utils.s3_uploder import S3Uploader



# 테스트 이미지 파일(jpg, png) 생성
def create_test_image(image_path: str, image_format: str):
    image = Image.new('RGB', (100, 100))
    image.save(image_path, image_format)


# 테스트 이미지 파일(svg) 생성
def create_test_svg(svg_path: str):
    svg = """<svg width="100" height="100">
    <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
    </svg>"""
    with open(svg_path, 'w') as f:
        f.write(svg)


# 테스트 이미지 파일 삭제
def delete_test_image(image_path: str):
    os.remove(image_path)


# 테스트 버킷 삭제
def delete_test_bucket(bucket_name: str):
    s3_uploader = S3Uploader()
    s3_uploader._delete_bucket(bucket_name)
    logging.info(f'{bucket_name} is deleted')
