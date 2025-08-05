import os

from minio import Minio

MINIO_CLIENT = Minio(
    os.getenv('MINIO_ENDPOINT', 'minio:9000'),
    access_key=os.getenv('MINIO_ACCESS_KEY', 'admin'),
    secret_key=os.getenv('MINIO_SECRET_KEY', 'password'),
    region=os.getenv('MINIO_REGION', 'eu-central-1'),
    secure=False
)
