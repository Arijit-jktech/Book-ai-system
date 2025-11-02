import httpx
from app.core.config import settings

async def generate_summary_from_text(text: str, max_tokens: int = 256) -> str:
    payload = {
        "model": "llama3",
        "input": f"Summarize the following text:\n\n{text}",
        "max_tokens": max_tokens,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(settings.LLAMA_ENDPOINT, json=payload)
        r.raise_for_status()
        data = r.json()
        if "text" in data:
            return data["text"]
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0].get("text", "")
        return str(data)
