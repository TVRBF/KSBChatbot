from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

from app.models.chat import ChatMessage, TranslateRequest
from app.services.gemini import gemini_chat, gemini_translate
from app.auth.utils import decode_token

router = APIRouter(prefix="/chat", tags=["chat"])

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client.ksm
history = db.history

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.post("/send")
async def send_message(msg: ChatMessage, user=Depends(get_current_user)):
    reply = await gemini_chat(msg.message)
    entry = {
        "user_id": user["sub"],
        "message": msg.message,
        "reply": reply,
        "timestamp": datetime.utcnow(),
    }
    await history.insert_one(entry)
    return {"reply": reply}

@router.get("/history")
async def get_history(user=Depends(get_current_user)):
    cursor = history.find({"user_id": user["sub"]}).sort("timestamp", 1)
    chats = []
    async for doc in cursor:
        chats.append({
            "message": doc["message"],
            "reply": doc["reply"],
            "timestamp": doc["timestamp"],
        })
    return {"history": chats}

@router.post("/translate")
async def translate(req: TranslateRequest, user=Depends(get_current_user)):
    translation = await gemini_translate(req.text, req.target_lang)
    return {"translation": translation}
