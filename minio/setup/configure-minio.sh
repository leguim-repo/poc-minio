#!/bin/bash

echo "Configurando MinIO..."
docker exec -i minio-scraper sh -c '
    sleep 10
    mc alias set minio http://localhost:9000 admin password

    mc mb minio/accounting/escobar --ignore-existing
    mc policy set public minio/accounting/escobar
    mc admin config set minio notify_webhook endpoint=http://python-service:5000/api/v0/webhook

    mc mb minio/intake --ignore-existing
    mc policy set public minio/intake
    mc admin config set minio notify_webhook endpoint=http://python-service:5000/api/v0/intake

'

echo "Reiniciando contenedor de MinIO..."
docker restart minio-scraper

echo "Esperando a que MinIO se reinicie..."
sleep 10

echo "Configurando eventos..."
docker exec -i minio-scraper sh -c '
    mc alias set minio http://localhost:9000 admin password

    echo "Configuración de eventos:"
    mc event add minio/accounting/escobar arn:minio:sqs:eu-central-1:escobar:webhook --event put
    mc event list minio/accounting/escobar

    echo "Configuración de eventos:"
    mc event add minio/intake arn:minio:sqs:eu-central-1:intake:webhook --event put
    mc event list minio/intake

'
