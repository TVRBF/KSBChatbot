from pydantic import BaseModel

class TextEmotionRequest(BaseModel):
    text: str

class VoiceEmotionResult(BaseModel):
    label: str
    confidence: float
