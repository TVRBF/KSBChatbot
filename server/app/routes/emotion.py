from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.emotion import TextEmotionRequest, VoiceEmotionResult
from app.services.emotion_text import detect_text_emotion
from app.services.emotion_voice import detect_voice_emotion  # optional heuristic

router = APIRouter(prefix="/emotion", tags=["emotion"])

@router.post("/text")
def emotion_text(req: TextEmotionRequest):
    try:
        result = detect_text_emotion(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text emotion error: {str(e)}")

@router.post("/voice", response_model=VoiceEmotionResult)
async def emotion_voice(file: UploadFile = File(...)):
    # Accepts an audio file (wav/mp3). We run a lightweight heuristic for demo.
    try:
        contents = await file.read()
        label, confidence = detect_voice_emotion(contents, file.content_type)
        return VoiceEmotionResult(label=label, confidence=confidence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice emotion error: {str(e)}")
