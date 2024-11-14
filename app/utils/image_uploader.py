from app.utils.s3_uploder import S3Uploader
from app.utils.exception import ImageUploaderError
        
def upload(bucket_name: str, save_path: str, image: bytes):
    try:
        s3_uploader = S3Uploader()
        return s3_uploader.upload_file(bucket_name, save_path, image)
    except Exception as e:
        raise ImageUploaderError(str(e))