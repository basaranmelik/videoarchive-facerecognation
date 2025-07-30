from fastapi import APIRouter, UploadFile, File, HTTPException, status
from src.service.recognition_service import RecognitionService

router = APIRouter(
    prefix="/recognition",
    tags=["Face Recognition"]
)

@router.post("/video")
async def recognize_faces_in_video(video: UploadFile = File(...)):
    if not video.content_type.startswith('video/'):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Please upload a video."
        )
    
    try:
        recognition_service = RecognitionService()
        video_bytes = await video.read()
        results = recognition_service.process_video(video_bytes)
        return {"filename": video.filename, "results": results}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )