from app.utils.exception import ImageUploaderError
from app.utils.s3_uploder import S3Uploader


def upload(bucket_name: str, save_path: str, image: bytes):
    try:
        s3_uploader = S3Uploader()
        s3_uploader.create_bucket(bucket_name)
        return s3_uploader.upload_file(bucket_name, save_path, image)
    except Exception as e:
        raise ImageUploaderError(str(e))
