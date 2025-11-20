import os
import aiohttp
import asyncio

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"

async def detect_text_emotion(text: str):
    if not text.strip():
        return {"label": "neutral", "scores": {"neutral": 1.0}}

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": text}

    async with aiohttp.ClientSession() as session:
        async with session.post(MODEL_URL, json=payload, headers=headers) as resp:
            if resp.status != 200:
                detail = await resp.text()
                raise Exception(f"HuggingFace API error: {detail}")
            data = await resp.json()

    # HuggingFace returns list of dicts with labels and scores
    # Example: [[{"label":"joy","score":0.98}, {"label":"sadness","score":0.01}, ...]]
    emotions = data[0]
    scores = {emo["label"]: emo["score"] for emo in emotions}
    top_label = max(scores, key=scores.get)
    return {"label": top_label, "scores": scores}
