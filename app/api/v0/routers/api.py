import glob

from fastapi import HTTPException, APIRouter

from app.api.v0.models.models import StatusResponse

api_router = APIRouter(
    prefix="/api/v0",
    tags=["additional"],
    responses={404: {"description": "No found"}}
)


@api_router.get("/status", response_model=StatusResponse)
async def get_status():
    try:
        log_files = glob.glob('/app/logs/summary_*.txt')
        processed_files = []

        for log_file in sorted(log_files, reverse=True)[:5]:
            with open(log_file, 'r') as f:
                processed_files.append(f.read())

        return StatusResponse(
            status="active",
            processed_files=processed_files
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
