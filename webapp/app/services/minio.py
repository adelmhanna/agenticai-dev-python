import boto3
from botocore.client import Config
import os
import logging
from app.utils.retry import retry

logger = logging.getLogger(__name__)

class MinIOService:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=f"http://{os.getenv('MINIO_HOST')}:9000",
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            config=Config(signature_version='s3v4')
        )
        self.bucket_name = "test-bucket"

    @retry(max_retries=5, delay=5)
    async def initialize_bucket(self):
        try:
            self.client.create_bucket(Bucket=self.bucket_name)
            sample_data = b"Sample data for MinIO"
            self.client.put_object(Bucket=self.bucket_name, Key="sample.txt", Body=sample_data)
            logger.info(f"Created MinIO bucket: {self.bucket_name}")
        except (self.client.exceptions.BucketAlreadyExists, self.client.exceptions.BucketAlreadyOwnedByYou):
            logger.info(f"MinIO bucket {self.bucket_name} already exists")
        except Exception as e:
            logger.error(f"Failed to create MinIO bucket: {str(e)}")
            raise

    @retry(max_retries=5, delay=5)
    async def test_list_buckets(self):
        try:
            buckets = self.client.list_buckets().get("Buckets", [])
            return [bucket["Name"] for bucket in buckets]
        except Exception as e:
            logger.error(f"Failed to list MinIO buckets: {str(e)}")
            raise