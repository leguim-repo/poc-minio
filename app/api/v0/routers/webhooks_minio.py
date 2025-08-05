import json
import subprocess
from urllib.parse import unquote

from fastapi import APIRouter, HTTPException

from app.api.v0.models.models import WebhookRequest, WebhookResponse
from app.shared.the_logger import THE_LOGGER

webhooks_minio_router = APIRouter(
    prefix="/api/v0",
    tags=["webhooks"],
    responses={404: {"description": "No found"}}
)


@webhooks_minio_router.post("/webhook", response_model=WebhookResponse)
async def handle_webhook(data: WebhookRequest):
    try:
        event = json.dumps(data.dict(), indent=2)
        THE_LOGGER.info(f"Webhook /webhook received: {event}")

        for record in data.Records:
            bucket_name = unquote(record.s3.bucket.name)
            object_name = unquote(record.s3.object.key)

            if 'ObjectCreated' in record.eventName:
                THE_LOGGER.info(f"New file created: {bucket_name}/{object_name}")

                try:
                    subprocess.run([
                        'python',
                        '/app/scripts/process_file.py',
                        bucket_name,
                        object_name
                    ], check=True)
                    THE_LOGGER.info(f"Processing completed for {object_name}")
                except subprocess.CalledProcessError as e:
                    THE_LOGGER.error(f"Error processing file: {e}")
                    raise HTTPException(status_code=500, detail=str(e))

        return WebhookResponse(status="success")

    except Exception as e:
        THE_LOGGER.error(f"Webhook error /webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@webhooks_minio_router.post("/intake", response_model=WebhookResponse)
async def handle_webhook(data: WebhookRequest):
    try:
        event = json.dumps(data.dict(), indent=2)
        THE_LOGGER.info(f"Webhook /intake received: {event}")

        return WebhookResponse(status="success")

    except Exception as e:
        THE_LOGGER.error(f"Webhook error /intake: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@webhooks_minio_router.post("/myfunction", response_model=WebhookResponse)
async def handle_webhook(data: WebhookRequest):
    try:
        event = json.dumps(data.dict(), indent=2)
        THE_LOGGER.info(f"webhook /myfunction received: {event}")

        return WebhookResponse(status="success")

    except Exception as e:
        THE_LOGGER.error(f"Webhook error /myfunction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
