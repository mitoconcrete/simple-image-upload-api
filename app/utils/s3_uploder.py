import logging

import boto3
from app.configs.setting import setting


class S3Uploader:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=setting.AWS_ACCESS_KEY_ID, 
            aws_secret_access_key=setting.AWS_SECRET_ACCESS_KEY,
            region_name=setting.AWS_DEFAULT_REGION
        )

    def _has_bucket(self, bucket_name: str) -> bool:
        return any([bucket['Name'] == bucket_name for bucket in self.s3.list_buckets()['Buckets']])
    
    def _has_file(self, bucket_name: str, file_name: str) -> bool:
        try:
            self.s3.head_object(Bucket=bucket_name, Key=file_name)
            return True
        except self.s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise e

    def _create_bucket(self, bucket_name: str) -> None:
        # check existing bucket name
        if self._has_bucket(bucket_name):
            logging.info(f'{bucket_name} already exists')
            return bucket_name

        # create bucket
        self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
        logging.info(f'{bucket_name} is created')
        return bucket_name

    def _delete_bucket(self, bucket_name: str) -> None:
        self.s3.delete_bucket(Bucket=bucket_name)
        logging.info(f'{bucket_name} is deleted')

    def upload_file(self, bucket_name: str, file_name: str, file_data: bytes) -> str:
        self.s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_data)
        return f'https://{bucket_name}.s3.{setting.AWS_DEFAULT_REGION}.amazonaws.com/{file_name}'

    def delete_file(self, bucket_name: str, file_name: str) -> None:
        self.s3.delete_object(Bucket=bucket_name, Key=file_name)

    def download_file(self, bucket_name: str, file_name: str) -> bytes:
        response = self.s3.get_object(Bucket=bucket_name, Key=file_name)
        return response['Body'].read()
