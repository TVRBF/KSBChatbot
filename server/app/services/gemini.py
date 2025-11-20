import os
import aiohttp

# Load API key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def gemini_chat(message: str) -> str:
    """
    Sends a user message to Gemini 2.5 and returns the AI-generated reply.
    Uses the free-tier API key from .env.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    
    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json"
    }

    # Gemini expects "contents" with conversation parts
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": message}
                ]
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            # Raise error if request fails
            resp.raise_for_status()
            data = await resp.json()

            # Parse the reply
            candidates = data.get("candidates", [])
            if not candidates:
                return "Sorry, I didn't understand that."

            parts = candidates[0].get("content", {}).get("parts", [])
            reply = "".join([part.get("text", "") for part in parts])
            return reply

# Optional placeholder for translation (keeps imports consistent)
async def gemini_translate(text: str, target_lang: str) -> str:
    """
    Placeholder translation function.
    Currently returns a simple formatted string.
    """
    return f"Translated({target_lang}): {text}"
