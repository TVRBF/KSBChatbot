from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, chat, emotion, stt

app = FastAPI(title="KSM Chatbot API", version="0.1.0")

# Include STT router first (optional order)
app.include_router(stt.router)

# ==============================
# CORS FOR PRODUCTION
# ==============================

origins = [
    "https://ksbchatbot.netlify.app",  # your frontend URL (NO SLASH)
    "http://127.0.0.1:5500",           # local development
    "http://localhost:5500"            # local development fallback
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Include other routers
# ==============================

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(emotion.router)

@app.get("/")
def read_root():
    return {"message": "KSM Chatbot API is running", "status": "ok"}
