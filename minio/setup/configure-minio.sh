#!/bin/bash

echo "- MinIO configuaration..."
docker exec -i minio-scraper sh -c '
    sleep 10
    mc alias set minio http://localhost:9000 admin password

    echo "* Creating bucket..."
    mc mb minio/accounting/escobar --ignore-existing
    mc policy set public minio/accounting/escobar
    mc admin config set minio notify_webhook endpoint=http://python-service:5000/api/v0/webhook

    echo "* Creating bucket..."
    mc mb minio/intake --ignore-existing
    mc policy set public minio/intake
    mc admin config set minio notify_webhook endpoint=http://python-service:5000/api/v0/intake

    '

echo "- Reboting MinIO container..."
docker restart minio-scraper

echo "- Waiting MinIO starting..."
sleep 10

echo "- Now...Start events configuration..."
docker exec -i minio-scraper sh -c '
    mc alias set minio http://localhost:9000 admin password

    echo "* Events configuration:"
    mc event add minio/accounting/escobar arn:minio:sqs:eu-central-1:escobar:webhook --event put
    mc event list minio/accounting/escobar

    echo "* Events configuration:"
    mc event add minio/intake arn:minio:sqs:eu-central-1:intake:webhook --event put
    mc event list minio/intake

    '
