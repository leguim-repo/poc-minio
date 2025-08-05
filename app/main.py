import uvicorn
from fastapi import FastAPI

from app.api.v0.routers.api import api_router
from app.api.v0.routers.webhooks_minio import webhooks_minio_router

app = FastAPI(title="Python Service API", version="1.0.0")

app.include_router(webhooks_minio_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
