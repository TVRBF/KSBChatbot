from fastapi import APIRouter, HTTPException
from app.models.emotion import TextEmotionRequest
from app.services.emotion_text import detect_text_emotion

router = APIRouter(prefix="/emotion", tags=["emotion"])

@router.post("/text")
async def emotion_text(req: TextEmotionRequest):
    try:
        result = await detect_text_emotion(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text emotion error: {str(e)}")
