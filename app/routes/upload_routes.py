from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas import UploadResponse
from app.services import UploadService

router = APIRouter(prefix="/api/v1", tags=["Upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        return UploadResponse(**(await UploadService.process_and_save_file(file)))
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc
